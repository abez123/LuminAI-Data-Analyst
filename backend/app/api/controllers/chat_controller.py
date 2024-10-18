from app.config.llm_config import LLM
from app.config.db_config import DB
from app.langgraph.workflows.sql_workflow import WorkflowManager
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse

llm_instance = LLM()


def ask_question(question: str):
    try:
        db = DB(db_url="sqlite:///./lumin.db")
        llm = llm_instance.groq("gemma2-9b-it")
        schema = db.get_schemas(table_names=[
                                'olist_products_dataset', "olist_orders_dataset", "olist_customers_dataset", "olist_order_items_dataset"])

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

    except Exception as e:
        # Catch all other errors and raise HTTP exception
        return JSONResponse(status_code=500, content={
            "message": "Something went wrong",
            "error": str(e)
        })


def get_convesactions():
    pass


def get_conversaction_history():
    pass
