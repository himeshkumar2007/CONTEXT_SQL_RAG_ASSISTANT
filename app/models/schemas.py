from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    user_id: Optional[str] = None  # optional, if you want user context
    query: str

class SQLResult(BaseModel):
    columns: List[str]
    rows: List[List]  # each row is a list of values

class AnswerResult(BaseModel):
    type: str  # 'sql', 'kb', or 'other'
    answer: str
    sql: Optional[str] = None  # if type == 'sql', this holds generated SQL
    sql_result: Optional[SQLResult] = None  # actual SQL query results

class ChatResponse(BaseModel):
    results: List[AnswerResult]
