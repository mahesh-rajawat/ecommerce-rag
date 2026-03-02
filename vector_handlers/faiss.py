from .base import BaseVectorHnadler
import os
import json
import faiss
from config.settings import DIM
import numpy as np

_INDEX_CACHE = {}

class FaissVectorHandler(BaseVectorHnadler):
    def __init__(self):
        super().__init__()
    
    def create_index(self):
        pass
    
    def write_index(self, path, index, embeddings):
        embeddings_np = self.normalize_embeddings(embeddings)
        index.add(embeddings_np)
        
        if not os.path.exists(path):
            os.makedirs(path)

        np.save(f"{path}/embeddings.npy", embeddings)
        faiss.write_index(index, f"{path}/rag.index")

    def read_index(self, path):
         index = faiss.read_index(path)
         return index

    def load_company_data_and_index(self, path):
        if path in _INDEX_CACHE:
            return _INDEX_CACHE[path]['index'], _INDEX_CACHE[path]['docs'], _INDEX_CACHE[path]['embeddings']
        
        if not os.path.exists(f"{path}/rag.index"):
            return faiss.IndexFlatL2(DIM), [], np.array([])
        
        index = self.read_index(f"{path}/rag.index")

        with open(f"{path}/docs.json") as f:
            documents = json.load(f)
        
        embeddings = np.load(f"{path}/embeddings.npy")

        _INDEX_CACHE[path] = {'index': index, 'docs': documents, 'embeddings': embeddings}
        return index, documents, embeddings
    
    def validate_np_array(self, np_array):
        if np_array.ndim != 2 or np_array.shape[1] != DIM:
            raise ValueError("Invalid embedding dimension")
        
    def normalize_embeddings(self, vectors):
        self.validate_np_array(vectors)
        faiss.normalize_L2(vectors)
        return vectors