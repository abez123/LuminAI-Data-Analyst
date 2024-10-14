from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.language_models import BaseLLM
from app.langgraph.prompt_templates.analyst_prompts import (
    get_schema_insights_prompt,
    generate_sql_query_prompt,
    fix_sql_query_prompt,
    format_results_prompt,
    get_visualization_prompt
)
from app.langgraph.prompt_templates.graph_prompts import get_prompt
from app.config.logging_config import get_logger

logger = get_logger(__name__)


class SQLAgent:
    def __init__(self, llm: BaseLLM):
        self.str_parser = StrOutputParser()
        self.json_parser = JsonOutputParser()
        self.llm = llm

    def get_parse_question(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("======= get_parse_question =======")
        # Check for required keys in the state
        required_keys = ["schema", "question"]
        missing_keys = [key for key in required_keys if key not in state]

        if missing_keys:
            raise ValueError(
                f"Missing required keys in state: {', '.join(missing_keys)}")

        question = state['question']
        schema = state['schema']
        # Ensure chain components are properly initialized
        if not self.llm or not self.json_parser:
            raise ValueError("LLM or JSON Parser is not initialized.")
        # Execute the chain
        chain = get_schema_insights_prompt | self.llm | self.json_parser
        response = chain.invoke({"schema": schema, "question": question})
        return {"parsed_question": response}

    def generate_sql_query(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("======= generate_sql_query =======")
        # Check for required keys in the state
        required_keys = ["schema", "question", "parsed_question"]
        missing_keys = [key for key in required_keys if key not in state]

        if missing_keys:
            raise ValueError(
                f"Missing required keys in state: {', '.join(missing_keys)}")

        schema = state["schema"]
        question = state["question"]
        parsed_question = state["parsed_question"]
        # Ensure chain components are properly initialized
        if not self.llm or not self.str_parser:
            raise ValueError("LLM or String Parser is not initialized.")

        chain = generate_sql_query_prompt | self.llm | self.str_parser
        response = chain.invoke(
            {"schema": schema, "question": question, "relevant_table_column": parsed_question})
        clean_sql_query = response.strip('`').replace('sql\n', '', 1).strip()
        if response.strip() == "NOT_ENOUGH_INFO":
            return {"sql_query": "NOT_RELEVANT"}
        else:
            return {"sql_query": clean_sql_query}

    def validate_and_fix_sql(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("========= validate_and_fix_sql ========")
        required_keys = ["schema", "sql_query"]
        missing_keys = [key for key in required_keys if key not in state]

        if missing_keys:
            raise ValueError(
                f"Missing required keys in state: {', '.join(missing_keys)}")

        sql_query = state['sql_query']
        schema = state['schema']

        # Ensure chain components are properly initialized
        if not self.llm or not self.json_parser:
            raise ValueError("LLM or JSON Parser is not initialized.")

        chain = fix_sql_query_prompt | self.llm | self.json_parser
        response = chain.invoke({"schema": schema, "sql_query": sql_query})

        if response["valid"] and response["issues"] is None:
            return {"sql_query": sql_query, "sql_valid": True}
        else:
            return {
                "sql_query": response["corrected_query"],
                "sql_valid": response["valid"],
                "sql_issues": response["issues"]
            }

    def format_results(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("========= format_results ========")
        required_keys = ["schema", "query_result"]
        missing_keys = [key for key in required_keys if key not in state]

        if missing_keys:
            raise ValueError(
                f"Missing required keys in state: {', '.join(missing_keys)}")

        question = state['question']
        results = state['query_result']

        if results == "NOT_RELEVANT":
            return {"answer": "Sorry, I can only give answers relevant to the database."}

        if not self.llm or not self.str_parser:
            raise ValueError("LLM or String Parser is not initialized.")

        chain = format_results_prompt | self.llm | self.str_parser
        response = chain.invoke({"question": question, "results": results})
        return {"answer": response}

    def choose_visualization(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("========= choose_visualization ========")
        required_keys = ["question", "query_result", "sql_query"]
        missing_keys = [key for key in required_keys if key not in state]
        if missing_keys:
            raise ValueError(
                f"Missing required keys in state: {', '.join(missing_keys)}")

        question = state['question']
        results = state['query_result']
        sql_query = state['sql_query']

        if results == "NOT_RELEVANT":
            return {"visualization": "none", "visualization_reasoning": "No visualization needed for irrelevant questions."}

        chain = get_visualization_prompt | self.llm | self.json_parser

        response = chain.invoke(
            {"question": question, "sql_query": sql_query, "results": results})

        return {
            "recommended_visualization": response["recommended_visualization"],
            "reason": response["reason"]
        }

    def format_visualization_data(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("========= format_visualization_data ========")
        question = state['question']
        results = state['query_result']
        recommended_visualization = state['recommended_visualization']
        pass


# class BaseFormatter(ABC):
#     def __init__(self, llm: BaseLLM):
#         self.llm = llm
#         self.str_parser = StrOutputParser()

#     @abstractmethod
#     def format(self, results: List[Union[List, Dict]], question: str) -> Dict[str, Any]:
#         # get_prompt
#         """Formats data for visualization."""
#         pass

#     def get_axis_label(self, query_result: List[Any], question: str, axis: str) -> str:
#         """Get axis label using the LLM."""
#         prompt = ChatPromptTemplate.from_messages([
#             ("system",
#              "You are a data labeling expert. Given a question and some data, provide a concise and relevant label for the {axis}-axis."),
#             ("human",
#              "Question: {question}\nData: {data}\n\nProvide a concise label for the {axis}-axis."),
#         ])
#         chain = prompt | self.llm | self.str_parser
#         return chain.invoke({"question": question, "data": str(query_result), "axis": axis})


# class LineChartFormatter(BaseFormatter):
#     def format(self, results: List[List[Union[str, float]]], question: str) -> Dict[str, Any]:
#         x_values = [str(row[0]) for row in results]
#         y_values = [float(row[1]) for row in results]
#         y_axis_label = self.get_axis_label(results[:2], question, "y")
#         return {
#             "xValues": x_values,
#             "yValues": [{"data": y_values, "label": y_axis_label.strip()}],
#         }


# class ScatterPlotFormatter(BaseFormatter):
#     def format(self, results: List[List[float]], question: str) -> Dict[str, Any]:
#         series = [{"x": float(x), "y": float(y), "id": i + 1}
#                   for i, (x, y) in enumerate(results)]
#         return {"series": [{"data": series, "label": "Data Points"}]}


# class BarChartFormatter(BaseFormatter):
#     def format(self, results: List[List[Union[str, float]]], question: str) -> Dict[str, Any]:
#         labels = [str(row[0]) for row in results]
#         data = [float(row[1]) for row in results]
#         y_axis_label = self.get_axis_label(results[:2], question, "y")
#         return {
#             "labels": labels,
#             "values": [{"data": data, "label": y_axis_label.strip()}]
#         }

# # Factory for creating formatters


# class FormatterRegistry:
#     def __init__(self, llm_manager):
#         self.formatters = {
#             "line": LineChartFormatter(llm_manager),
#             "scatter": ScatterPlotFormatter(llm_manager),
#             "bar": BarChartFormatter(llm_manager),
#             # Add other visualizers like "horizontal_bar", "pie", etc.
#         }

#     def get_formatter(self, visualization):
#         print("Selector method triggered")
#         return self.formatters.get(visualization, None)


# class DataFormatter:
#     def __init__(self, llm):
#         self.llm_manager = llm
#         self.registry = FormatterRegistry(self.llm_manager)

#     def format_data_for_visualization(self, state: dict) -> dict:
#         print("========= Main method to format data for visualization. ========")
#         """Main method to format data for visualization."""
#         print(state)
#         visualization = state['recommended_visualization']
#         results = state['query_result']
#         question = state['question']

#         formatter = self.registry.get_formatter(visualization)

#         if formatter is not None:
#             try:
#                 return {"formatted_data_for_visualization": formatter.format(results, question)}
#             except Exception as e:
#                 return {"error": str(e)}

#         return {"formatted_data_for_visualization": None}
