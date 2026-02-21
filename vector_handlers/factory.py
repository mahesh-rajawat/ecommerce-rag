from vector_handlers.faiss import FaissVectorHandler
from config.settings import VECTOR_HANDLER

def get_vector_handler():
    if VECTOR_HANDLER == 'faiss':
        return FaissVectorHandler()