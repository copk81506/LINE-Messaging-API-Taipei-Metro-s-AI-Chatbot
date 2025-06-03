from fastapi import FastAPI
from pydantic import BaseModel
from data_res import query,res,res_ans


app = FastAPI(title="RAG API")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    ans : str

@app.post("/query", response_model=QueryResponse)
def rag_query(request: QueryRequest):
    docs = query(request.question)
    res1,res2 = res(docs)
    ans = res_ans(res1,res2)
    return {"ans": ans,"code":200}
