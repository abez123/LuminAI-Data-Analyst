from typing import List, Any, Annotated, Dict
from typing_extensions import TypedDict
import operator
from langchain_core.language_models import BaseLLM
from langgraph.graph import START, END, StateGraph
from app.langgraph.agents.sql_agent import SQLAgent
from app.config.db_config import DB


def clean_sql_query(query):
    # Remove backticks and newlines
    cleaned = query.replace('`', '').replace('\n', ' ')

    # Remove any extra spaces
    cleaned = ' '.join(cleaned.split())

    # Remove the trailing '```' if present
    cleaned = cleaned.rstrip('`')

    return cleaned


class InputState(TypedDict):
    question: str
    schema: List[Dict]
    parsed_question: dict
    sql_query: str
    sql_valid: bool
    sql_issues: str
    query_result: List[Any]
    recommended_visualization: str
    reason: str
    visualization: Annotated[str, operator.add]
    visualization_reason: Annotated[str, operator.add]
    formatted_data_for_visualization: Dict[str, Any]


class OutputState(TypedDict):
    parsed_question: Dict[str, Any]
    unique_nouns: List[str]
    sql_query: str
    sql_valid: bool
    sql_issues: str
    query_result: List[Any]
    recommended_visualization: str
    reason: str
    results: List[Any]
    answer: Annotated[str, operator.add]
    error: str
    visualization: Annotated[str, operator.add]
    visualization_reason: Annotated[str, operator.add]
    formatted_data_for_visualization: Dict[str, Any]


class WorkflowManager:
    def __init__(self, llm: BaseLLM, db: DB):
        self.llm = llm
        self.db = db
        self.sql_agent = SQLAgent(llm)

    def run_sql_query(self, state: Dict[str, Any]) -> Dict[List, Any]:
        print("========== run_sql_query ==========")
        query = state['sql_query']
        if query == "NOT_RELEVANT":
            return {"query_result": []}
        # Clean query
        cleaned_query = clean_sql_query(query)

        print("SQL QUERY :", cleaned_query)
        result = self.db.execute_query(cleaned_query)
        # Convert RowProxy to dict
        return {"query_result": result}

    def create_workflow(self) -> StateGraph:
        """Create and configure the workflow graph."""
        workflow = StateGraph(input=InputState, output=OutputState)

        # Add nodes to the graph
        workflow.add_node("parse_question", self.sql_agent.get_parse_question)
        workflow.add_node("generate_sql", self.sql_agent.generate_sql_query)
        workflow.add_node("validate_and_fix_sql",
                          self.sql_agent.validate_and_fix_sql)
        workflow.add_node("execute_sql", self.run_sql_query)
        workflow.add_node("format_results", self.sql_agent.format_results)
        workflow.add_node("choose_visualization",
                          self.sql_agent.choose_visualization)
        workflow.add_node("format_data_for_visualization",
                          self.sql_agent.format_visualization_data)

        # Add a node for conversational LLM response if the question is irrelevant
        workflow.add_node("conversational_response",
                          self.sql_agent.conversational_response)

        # Define edges
        workflow.add_edge(START, "parse_question")

        # Add conditional edge to check if the conversation should continue or end
        workflow.add_conditional_edges(
            "parse_question",  # Start after parsing question
            self.should_continue  # Conditional function to determine the next node
        )

        workflow.add_edge("generate_sql", "validate_and_fix_sql")
        workflow.add_edge("validate_and_fix_sql", "execute_sql")
        workflow.add_edge("execute_sql", "format_results")
        workflow.add_edge("execute_sql", "choose_visualization")
        workflow.add_edge("choose_visualization",
                          "format_data_for_visualization")
        workflow.add_edge("format_data_for_visualization", END)
        workflow.add_edge("format_results", END)
        # End the workflow after conversational response
        workflow.add_edge("conversational_response", END)

        return workflow

    def should_continue(self, state: Dict) -> str:
        """Determine the next step based on the relevance of the question."""
        parsed_question = state['parsed_question']

        # If the question is not relevant, switch to the conversational LLM
        if not parsed_question.get("is_relevant", True):
            return "conversational_response"

        # Otherwise, proceed with the SQL generation
        return "generate_sql"

    def returnGraph(self):
        return self.create_workflow().compile()

    def run_sql_agent(self, question: str, schema: List[Dict]) -> dict:
        """Run the SQL agent workflow and return the formatted answer and visualization recommendation."""
        app = self.create_workflow().compile()
        for event in app.stream({"question": question, "schema": schema}):
            for value in event.values():
                print(value)
