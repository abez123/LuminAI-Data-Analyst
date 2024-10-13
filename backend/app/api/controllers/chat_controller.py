from app.langgraph.prompt_templates.graph_prompts import get_prompt

def ask_question():
    question = "What is the sales trend over the last 6 months?"
    data = "Month,Sales\nJan,100\nFeb,120\nMar,110\nApr,130\nMay,140\nJun,160"
    prompt = get_prompt("line", question, data)
    
    print("HUMAN : ",prompt["human"])
    print("SYSTEM : ",prompt["system"])

    return {"system": question}