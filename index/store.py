import numpy as np
import faiss
import json
from utils.paths import get_company_dir
from ingestion.loader import load_company_data_and_index
from index.embedder import Embedder
DIM = 768

class Store:
    def __init__(self, company):
        self.company = company
        self.embedder = Embedder()
        get_company_dir(company)

    def save(self, chunks):
        vectors = self.embedder.embed_chunks(chunks)
        vecs = np.array(vectors).astype("float32")
        self.validate_np_array(vecs)
        index, documents = load_company_data_and_index(self.company)

        index.add(vecs)
        for i, c in enumerate(chunks):
            documents.append({
                'id': i,
                "text": c,
                "company": self.company,
                "document": "sales_and_delivery_terms",
                "source": "api"
            })
        self.save_all(index, documents)
        return True

    def validate_np_array(self, np_array):
        if np_array.ndim != 2 or np_array.shape[1] != DIM:
            raise ValueError("Invalid embedding dimension")


    def save_all(self, index, documents):
        path = get_company_dir(self.company)
        faiss.write_index(index, f"{path}/rag.index")
        with open(f"{path}/docs.json", "w") as f:
            json.dump(documents, f, ensure_ascii=False, indent=2)
