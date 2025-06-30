from fastapi import APIRouter
from pydantic import BaseModel
from app.services.intent_classifier import classify_intent
from app.services.sql_handler import handle_sql_query
from app.services.kb_handler import handle_kb_query
from app.services.utils import log_info, get_db_config

router = APIRouter()

class QueryRequest(BaseModel):
    user_id: str
    query: str

@router.post("/ask")
async def ask_question(request: QueryRequest):
    query = request.query
    user_id = request.user_id

    log_info(f"User [{user_id}] asked: {query}")

    # Split query by 'and', 'then' — you can improve this later using NLP
    sub_queries = [q.strip() for q in query.split(" and ") if q.strip()]
    responses = []

    for sub_query in sub_queries:
        intent = classify_intent(sub_query)
        log_info(f"Sub-query: [{sub_query}] → Intent: {intent}")

        if intent == "sql":
            result = handle_sql_query(sub_query, get_db_config())
            responses.append({"type": "sql", "query": sub_query, "result": result})

        elif intent == "kb":
            answer = handle_kb_query(sub_query)
            responses.append({"type": "kb", "query": sub_query, "answer": answer})

        else:
            responses.append({
                "type": "other",
                "query": sub_query,
                "answer": "I'm trained only to assist with database and knowledge base queries."
            })

    return {"responses": responses}
