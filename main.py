from fastapi import FastAPI, HTTPException, Query
from app.ingestion.ingestion_request import IngestRequest
from app.pipeline.ingestion import IngestionPipeline
from app.pipeline.searching import SearchingPipeline
from app.logger.logger import get_logger
from app.ingestion.factory import get_text_loaded


app = FastAPI()

@app.get("/")
def index() -> dict[str, str]:
    return {"message": "hello i am runnning"}

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

    

@app.post("/ingest", status_code=201)
def ingest(req: IngestRequest):
    company = req.company.lower()
    print(company)
    domain = req.domain.lower() if req.domain else "general"
    text_loader = get_text_loaded(req.source_type)
    text = text_loader(req)
    ingestion = IngestionPipeline(company, domain)

    return ingestion.run(text)

logger = get_logger("api_ask")

@app.get("/ask", status_code=200)
def ask(q: str = Query(..., min_length=3), company: str = Query(...)):
    logger.info("Incoming question: %s", q)
    if not q.strip():
        raise HTTPException(status_code=400, detail="Search query required")
    
    if not company.strip():
        raise HTTPException(status_code=400, detail="Company name required")
    
    return SearchingPipeline(q, company).run()