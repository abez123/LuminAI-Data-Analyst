from typing import Dict
from string import Template

graph_prompt_templates: Dict[str, Dict[str, str]] = {
    "bar": {
        "system": '''You are a data visualization expert. Given a question and some data, provide a concise and relevant structure for a bar chart.''',
        "human": '''Question: ${question}
        Data: ${data}

        Provide a bar chart structure in the following format:
        {
        labels: string[],
        values: { data: number[], label: string }[]
        }
        Ensure the structure is relevant to the question and data provided.'''
    },
    "horizontal_bar": {
        "system": '''You are a data visualization expert. Given a question and some data, provide a concise and relevant structure for a horizontal bar chart.''',
        "human": '''Question: ${question}
        Data: ${data}

        Provide a horizontal bar chart structure in the following format:
        {
        labels: string[],
        values: { data: number[], label: string }[]
        }
        Ensure the structure is relevant to the question and data provided.'''
    },
    "line": {
        "system": '''You are a data visualization expert. Given a question and some data, provide a concise and relevant structure for a line graph.''',
        "human": '''Question: ${question}
        Data: ${data}

        Provide a line graph structure in the following format:
        {
        xValues: number[] | string[],
        yValues: { data: number[], label: string }[]
        }
        Ensure the structure is relevant to the question and data provided.'''
    },
    "pie": {
        "system": '''You are a data visualization expert. Given a question and some data, provide a concise and relevant structure for a pie chart.''',
        "human": '''Question: ${question}
        Data: ${data}

        Provide a pie chart structure in the following format:
        [
        { label: string, value: number }
        ]
        Ensure the structure is relevant to the question and data provided.'''
    },
    "scatter": {
        "system": '''You are a data visualization expert. Given a question and some data, provide a concise and relevant structure for a scatter plot.''',
        "human": '''Question: ${question}
        Data: ${data}

        Provide a scatter plot structure in the following format:
        {
        series: {
            data: { x: number, y: number, id: number }[],
            label: string
        }[]
        }
        Ensure the structure is relevant to the question and data provided.'''
    }
}

# Usage example:
def get_prompt(graph_type: str, question: str, data: str) -> Dict[str, str]:
    if graph_type not in graph_prompt_templates:
        raise ValueError(f"Unknown graph type: {graph_type}")
    
    template = graph_prompt_templates[graph_type]
    return {
        "system": template["system"],
        "human": Template(template["human"]).substitute(question=question, data=data)
    }
