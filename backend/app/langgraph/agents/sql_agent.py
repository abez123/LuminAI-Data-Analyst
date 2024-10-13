from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.language_models import BaseLLM
from app.langgraph.prompt_templates.graph_prompts import get_prompt

class SQLAgent:
    def __init__(self, llm: BaseLLM):
        self.str_parser = StrOutputParser()
        self.json_parser = JsonOutputParser()
        self.llm = llm

    def get_parse_question(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation here
        pass

    def get_unique_nouns(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation here
        pass

    def generate_sql_query(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation here
        pass

    def validate_and_fix_sql(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation here
        pass

    def format_results(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation here
        pass

    def choose_visualization(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation here
        pass

class BaseFormatter(ABC):
    def __init__(self, llm: BaseLLM):
        self.llm = llm
        self.str_parser = StrOutputParser()

    @abstractmethod
    def format(self, results: List[Union[List, Dict]], question: str) -> Dict[str, Any]:
        """Formats data for visualization."""
        pass

    def get_axis_label(self, query_result: List[Any], question: str, axis: str) -> str:
        """Get axis label using the LLM."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a data labeling expert. Given a question and some data, provide a concise and relevant label for the {axis}-axis."),
            ("human", "Question: {question}\nData: {data}\n\nProvide a concise label for the {axis}-axis."),
        ])
        chain = prompt | self.llm | self.str_parser
        return chain.invoke({"question": question, "data": str(query_result), "axis": axis})

class LineChartFormatter(BaseFormatter):
    def format(self, results: List[List[Union[str, float]]], question: str) -> Dict[str, Any]:
        x_values = [str(row[0]) for row in results]
        y_values = [float(row[1]) for row in results]
        y_axis_label = self.get_axis_label(results[:2], question, "y")
        return {
            "xValues": x_values,
            "yValues": [{"data": y_values, "label": y_axis_label.strip()}],
        }

class ScatterPlotFormatter(BaseFormatter):
    def format(self, results: List[List[float]], question: str) -> Dict[str, Any]:
        series = [{"x": float(x), "y": float(y), "id": i + 1} for i, (x, y) in enumerate(results)]
        return {"series": [{"data": series, "label": "Data Points"}]}

class BarChartFormatter(BaseFormatter):
    def format(self, results: List[List[Union[str, float]]], question: str) -> Dict[str, Any]:
        labels = [str(row[0]) for row in results]
        data = [float(row[1]) for row in results]
        y_axis_label = self.get_axis_label(results[:2], question, "y")
        return {
            "labels": labels,
            "values": [{"data": data, "label": y_axis_label.strip()}]
        }

# Factory for creating formatters
class FormatterRegistry:
    def __init__(self, llm_manager):
        self.formatters = {
            "line": LineChartFormatter(llm_manager),
            "scatter": ScatterPlotFormatter(llm_manager),
            "bar": BarChartFormatter(llm_manager),
            # Add other visualizers like "horizontal_bar", "pie", etc.
        }

    def get_formatter(self, visualization):
        print("Selector method triggered")
        return self.formatters.get(visualization, None)

class DataFormatter:
    def __init__(self,llm):
        self.llm_manager = llm
        self.registry = FormatterRegistry(self.llm_manager)

    def format_data_for_visualization(self, state: dict) -> dict:
        print("========= Main method to format data for visualization. ========")
        """Main method to format data for visualization."""
        print(state)
        visualization = state['recommended_visualization']
        results = state['query_result']
        question = state['question']

        formatter = self.registry.get_formatter(visualization)

        if formatter is not None:
            try:
                return {"formatted_data_for_visualization": formatter.format(results, question)}
            except Exception as e:
                return {"error": str(e)}
        
        return {"formatted_data_for_visualization": None}
