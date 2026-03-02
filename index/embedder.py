import ollama
import numpy as np

class Embedder:
    def __init__(self):
        pass

    def embed(self, texts:list) -> list:
        embeddings = []
        if isinstance(texts, str):
            texts = [texts]

        for text in texts:
            res = ollama.embeddings(
                model="nomic-embed-text",
                prompt=text
            )
            embeddings.append(res['embedding'])
        
        vectors = np.array(embeddings).astype('float32')

        return vectors
