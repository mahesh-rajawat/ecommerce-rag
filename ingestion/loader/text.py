from ingestion.ingestion_request import IngestRequest

def load_text(req: IngestRequest) -> str:
    text = req.text
    return text.strip()