import os
TOP_K = int(os.getenv("TOP_K", 30))
DISTANCE_THRESHOLD = int(os.getenv("DISTANCE_THRESHOLD", 350))
MAX_CONTEXT = int(os.getenv("MAX_CONTEXT", 3000))
MODEL = os.getenv("MODEL", "llama3.2")
DATA_DIR = os.getenv("DATA_DIR", "./app/data/tenants")
DIM = int(os.getenv("DIM", 768))
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")

MIN_CONFIDENCE = float(os.getenv("MIN_CONFIDENCE", 0.35))
MIN_SOURCES = int(os.getenv("MIN_SOURCES", 2))
VECTOR_HANDLER = os.getenv("VECTOR_HANDLER", "faiss")