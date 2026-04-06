from app.ingestion.ingestion_request import IngestRequest

def load_file(req: IngestRequest) -> str:
    with open(req.file_path, "r", encoding="utf-8") as f:
        return f.read()