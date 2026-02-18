from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from pipeline.ingestion import IngestionPipeline
from pipeline.searching import SearchingPipeline
from logs.logger import get_logger



app = FastAPI()

@app.get("/")
def index() -> dict[str, str]:
    return {"message": "hello i am runnning"}

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

class UploadRequest(BaseModel):
    text: str
    company: str

@app.post("/upload", status_code=201)
def upload(data:UploadRequest):
    if not data.text:
        raise HTTPException(status_code=404, detail="Empty text")
    company = data.company.lower()
    ingestion = IngestionPipeline(company, text=data.text)
    return ingestion.run()

logger = get_logger("api_ask")

@app.get("/ask", status_code=200)
def ask(q: str = Query(..., min_length=3), company: str = Query(...)):
    logger.info("Incoming question: %s", q)
    if not q.strip():
        raise HTTPException(status_code=400, detail="Search query required")
    
    if not company.strip():
        raise HTTPException(status_code=400, detail="Company name required")
    
    return SearchingPipeline(q, company).run()