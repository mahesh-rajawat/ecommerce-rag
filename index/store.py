import numpy as np
import faiss
import json
from utils.paths import get_company_dir
from vector_handlers.factory import get_vector_handler
from index.embedder import Embedder
from preprocess.metadata_generator import MetaGenerator
DIM = 768

class Store:
    def __init__(self, company, domain):
        self.company = company
        self.domain = domain
        self.embedder = Embedder()
        self.vector_handler = get_vector_handler()
        self.meta_generator = MetaGenerator()
        get_company_dir(company)

    def save(self, chunks):
        path = f"{get_company_dir(self.company)}/{self.domain}"
        vectors = self.embedder.embed(chunks)
        # vecs = np.array(vectors).astype("float32")
        # self.validate_np_array(vecs)
        index, documents, empty_nmpy = self.vector_handler.load_company_data_and_index(path)
        start_id = len(documents)
        # index.add(vecs)
        for i, c in enumerate(chunks):
            doc_id = start_id + i
            metadata = self.meta_generator.generate_metadata(c, self.company, self.domain, "api")
            documents.append({
                'id': doc_id,
                "text": c,
                "metadata": metadata,
                "company": self.company,
                "document": self.domain,
                "source": "api"
            })
        
        self.save_all(path, index, documents, vectors)
        return True


    def save_all(self, path, index, documents, vectors):
        self.vector_handler.write_index(
            path,
            index,
            vectors
        )
        with open(f"{path}/docs.json", "w") as f:
            json.dump(documents, f, ensure_ascii=False, indent=2)
