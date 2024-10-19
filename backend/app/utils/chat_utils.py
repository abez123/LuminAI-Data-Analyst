from app.langgraph.workflows.sql_workflow import WorkflowManager
from app.config.llm_config import LLM
from app.config.db_config import DB, VectorDB
from fastapi.responses import StreamingResponse, JSONResponse
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from typing import List, Optional
from app.config.logging_config import get_logger


logger = get_logger(__name__)
llm_instance = LLM()
vectorDB_instance = VectorDB()


def execute_workflow(question: str, table_list: List[str], db: Optional[DB] = None, db_url: Optional[str] = None):

    if not db:
        db = DB(db_url)

    llm = llm_instance.groq("gemma2-9b-it")
    schema = db.get_schemas(table_names=table_list)

    workflow = WorkflowManager(llm, db)
    app = workflow.create_workflow().compile()

    # Define a generator to stream the data from LangGraph
    def event_stream():
        for event in app.stream({"question": question, "schema": schema}):
            for value in event.values():
                # Yield the streamed data to the client
                yield f"data: {value}\n\n"

    # Return the streaming response using event_stream generator
    return StreamingResponse(event_stream(), media_type="text/event-stream")


def serialize_document(doc):
    """Helper function to serialize a Document object"""
    return {
        "page_content": doc.page_content,
        "metadata": doc.metadata
    }


def execute_document_chat(question: str, embedding_model: str, table_name: str):
    try:
        # Initialize embedding
        vectorDB_instance.initialize_embedding(embedding_model)

        # Get vector store
        vector_store = vectorDB_instance.get_vector_store(table_name)

        # Initialize LLM
        llm = llm_instance.groq("gemma2-9b-it")

        # Create a prompt template
        prompt_template = """You are Lumin, an advanced data analysis assistant, analyze the following context to answer the question. Follow these guidelines:

        1. Use only the information provided in the context.
        2. If the context doesn't contain enough information, state that clearly.
        3. Provide data-driven insights when possible.
        4. Be concise but comprehensive in your response.
        5. If applicable, mention any trends, patterns, or anomalies in the data.

        Context:
        {context}

        Question: {question}

        Analysis:
        """

        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        # Create a RetrievalQA chain
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )

        # Execute the chain
        result = qa({"query": question})

        # Serialize the source documents
        serialized_docs = [serialize_document(
            doc) for doc in result.get('source_documents', [])]

        return JSONResponse(status_code=200, content={
            "answer": result['result'],
            "source_documents": serialized_docs
        })

    except Exception as e:
        print(f"Error in simple_document_chat: {str(e)}")
        raise ValueError(f"Failed to execute document chat: {str(e)}")
