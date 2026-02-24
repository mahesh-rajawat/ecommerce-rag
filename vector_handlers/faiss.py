from .base import BaseVectorHnadler
import os
import json
import faiss
from config.settings import DIM

class FaissVectorHandler(BaseVectorHnadler):
    def __init__(self):
        super().__init__()
    
    def create_index(self):
        pass
    
    def write_index(self, path, index):
        if not os.path.exists(path):
            os.makedirs(path)

        faiss.write_index(index, f"{path}/rag.index")

    def read_index(self, path):
         index = faiss.read_index(path)
         return index

    def load_company_data_and_index(self, path):
        if not os.path.exists(f"{path}/rag.index"):
            return faiss.IndexFlatL2(DIM), []
        
        index = self.read_index(f"{path}/rag.index")

        with open(f"{path}/docs.json") as f:
            documents = json.load(f)
        
        return index, documents