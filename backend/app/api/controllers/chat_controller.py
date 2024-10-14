from app.langgraph.prompt_templates.graph_prompts import get_prompt
from app.langgraph.agents.sql_agent import SQLAgent
from app.config.llm_config import LLM
from app.config.db_config import DB
from fastapi.responses import JSONResponse

llm_instance = LLM()
db = DB(db_url="sqlite:///./lumin.db")


def ask_question():
    try:

        llm = llm_instance.groq("gemma2-9b-it")
        agent = SQLAgent(llm=llm)
        schema = db.get_schemas(table_names=[
                                'olist_products_dataset', "olist_orders_dataset", "olist_customers_dataset", "olist_order_items_dataset"])

        state = {
            "question": "What percentage of orders are in each status?",
            "schema": schema
        }
        parse_question = agent.get_parse_question(state)
        state["parsed_question"] = parse_question["parsed_question"]
        sql_query = agent.generate_sql_query(state)
        state["sql_query"] = sql_query["sql_query"]
        validated_query = agent.validate_and_fix_sql(state)
        print(validated_query["sql_query"])
        query_result = db.execute_query(validated_query["sql_query"])
        state["query_result"] = query_result
        formatted_res = agent.format_results(state)
        print("===== formatted_res ===== :", formatted_res)
        choose_visualization = agent.choose_visualization(state)
        print("===== choose_visualization ===== :", choose_visualization)
        state["recommended_visualization"] = choose_visualization["recommended_visualization"]
        formatted_visualization = agent.format_visualization_data(state)

        return {
            "question": state["question"],
            "answer": formatted_res["answer"],
            "sql_query": validated_query["sql_query"],
            "choose_visualization": choose_visualization["recommended_visualization"],
            "formatted_visualization": formatted_visualization
        }

    except Exception as e:
        # Catch all other errors and raise HTTP exception
        return JSONResponse(status_code=500, content={
            "message": "Something went wrong",
            "error": str(e)
        })
