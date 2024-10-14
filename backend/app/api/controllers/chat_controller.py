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
        schema = db.get_schemas(table_names=["users"])

        # print("SCHEMA : ", schema)
        state = {
            "question": "What is the total userbase ?",
            "schema": schema
        }
        parse_question = agent.get_parse_question(state)
        state["parsed_question"] = parse_question["parsed_question"]
        sql_query = agent.generate_sql_query(state)
        state["sql_query"] = sql_query["sql_query"]
        res = agent.validate_and_fix_sql(state)

        # agent.format_results()
        # agent.choose_visualization()

        return {"system": res}

    except Exception as e:
        # Catch all other errors and raise HTTP exception
        return JSONResponse(status_code=500, content={
            "message": "Something went wrong",
            "error": str(e)
        })
