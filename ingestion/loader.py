import os
import json
import faiss
from utils.paths import get_company_dir

from config.settings import DIM

def load_from_api(text:str) -> list:
    return [text.strip()]

def load_from_file(path:str) -> list:
    if not os.path.exists(path):
        raise Exception('File not exists')
    with open(path) as f:
        return [f.read()]
    
def load_documents(path):
    docs = []

    for file in os.listdir(path):
        with open(file) as f:
            docs.append(f.read())

    return docs    

def load_company_data_and_index(company):
    path = get_company_dir(company)
    if not os.path.exists(f"{path}/rag.index"):
        return faiss.IndexFlatL2(DIM), []
    
    index = faiss.read_index(f"{path}/rag.index")

    with open(f"{path}/docs.json") as f:
        documents = json.load(f)
    
    return index, documents