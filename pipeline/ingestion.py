from preprocess.cleaner import clean_text
from preprocess.chunker import chunker
from index.store import Store
import os

class IngestionPipeline:
    def __init__(self, company, domain):
        self.company = company
        self.domain = domain
        self.store = Store(company, domain)
    
    def run(self, raw):
   
        cleaned = clean_text(raw)
        chunks = chunker(cleaned)
        
        self.store.save(chunks)

        return {
            "company": self.company,
            "chunks": len(chunks),
            "status": "success"
        }

