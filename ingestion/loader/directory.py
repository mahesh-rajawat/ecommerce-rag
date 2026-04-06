import os
from app.ingestion.loader.file import load_file 
from app.ingestion.ingestion_request import IngestRequest

def load_directory(req: IngestRequest):
    texts = []
    for file in os.listdir(req.dir_path):
        if file.endswith(".txt"):
            text = load_file(os.path.join(req.dir_path, file))
            texts.append(text)

    return "\n".join(texts)