import ollama

class Embedder:
    def __init__(self):
        pass

    def embed_chunks(self, chunks:list) -> list:
        embeddings = []
        for text in chunks:
            res = ollama.embeddings(
                model="nomic-embed-text",
                prompt=text
            )
            embeddings.append(res['embedding'])
        return embeddings

    def embed_query(self, query:str):
        res = ollama.embeddings(
            model="nomic-embed-text",
            prompt=query
        )

        return res.embedding