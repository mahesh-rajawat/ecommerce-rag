from preprocess.cleaner import clean_text
from preprocess.chunker import chunker
from index.store import Store
from ingestion.loader import load_from_api, load_from_file
import os

class IngestionPipeline:
    def __init__(self, company, text=None, path = None):
        self.company = company
        self.__text = text
        self.__path = path
        self.store = Store(company)

    def _load(self):
        if self.__text:
            return load_from_api(self.__text)

        if self.__path and os.path.exists(self.__path):
            return load_from_file(self.__path)
        
        raise ValueError("No valid input provided (text or path required)")
    
    def run(self):
        docs = self._load()

        cleaned = [
            clean_text(d)
            for d in docs
        ]

        chunks = []
        for text in cleaned:
            parts = chunker(text)
            chunks.extend(parts)
            
        self.store.save(chunks)

        return {
            "company": self.company,
            "documents": len(docs),
            "chunks": len(chunks),
            "status": "success"
        }

