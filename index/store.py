import numpy as np
import faiss
import json
from utils.paths import get_company_dir
from vector_handlers.factory import get_vector_handler
from index.embedder import Embedder
DIM = 768

class Store:
    def __init__(self, company, domain):
        self.company = company
        self.domain = domain
        self.embedder = Embedder()
        self.vector_handler = get_vector_handler()
        get_company_dir(company)

    def save(self, chunks):
        path = f"{get_company_dir(self.company)}/{self.domain}"
        vectors = self.embedder.embed_chunks(chunks)
        vecs = np.array(vectors).astype("float32")
        self.validate_np_array(vecs)
        index, documents = self.vector_handler.load_company_data_and_index(path)
        start_id = len(documents)
        index.add(vecs)
        for i, c in enumerate(chunks):
            doc_id = start_id + i
            
            documents.append({
                'id': doc_id,
                "text": c,
                "company": self.company,
                "document": self.domain,
                "embedding": vectors[i],
                "source": "api"
            })
        
        self.save_all(path, index, documents)
        return True

    def validate_np_array(self, np_array):
        if np_array.ndim != 2 or np_array.shape[1] != DIM:
            raise ValueError("Invalid embedding dimension")


    def save_all(self, path, index, documents):
        self.vector_handler.write_index(
            path,
            index
        )
        with open(f"{path}/docs.json", "w") as f:
            json.dump(documents, f, ensure_ascii=False, indent=2)
