from typing import List, Any, Annotated, Dict
from typing_extensions import TypedDict
import operator
from langchain_core.language_models import BaseLLM
from langgraph.graph import START, END, StateGraph
from app.langgraph.agents.sql_agent import SQLAgent
from app.config.db_config import DB


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
        result = self.db.execute_query(query)
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

        # Define edges
        workflow.add_edge(START, "parse_question")
        workflow.add_edge("parse_question", "generate_sql")
        workflow.add_edge("generate_sql", "validate_and_fix_sql")
        workflow.add_edge("validate_and_fix_sql", "execute_sql")
        workflow.add_edge("execute_sql", "format_results")
        workflow.add_edge("execute_sql", "choose_visualization")
        workflow.add_edge("choose_visualization",
                          "format_data_for_visualization")
        workflow.add_edge("format_data_for_visualization", END)
        workflow.add_edge("format_results", END)

        return workflow

    def returnGraph(self):
        return self.create_workflow().compile()

    def run_sql_agent(self, question: str, schema: List[Dict]) -> dict:
        """Run the SQL agent workflow and return the formatted answer and visualization recommendation."""
        app = self.create_workflow().compile()
        for event in app.stream({"question": question, "schema": schema}):
            for value in event.values():
                print(value)
