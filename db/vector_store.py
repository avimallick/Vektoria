# db/vector_store.py
import faiss
import numpy as np
import os

class VectorStore:
    def __init__(self, dim: int, index_path: str = "models/faiss_index.index"):
        self.dim = dim
        self.index_path = index_path

        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        else:
            self.index = faiss.IndexFlatL2(dim)

    def add(self, vectors: np.ndarray) -> list:
        start_id = self.index.ntotal
        self.index.add(vectors)
        end_id = self.index.ntotal
        self.save()
        return list(range(start_id, end_id))  # Return assigned vector IDs

    def search(self, query_vector: np.ndarray, k: int = 5) -> list:
        D, I = self.index.search(query_vector, k)
        return I[0].tolist()  # Return list of vector IDs

    def save(self):
        faiss.write_index(self.index, self.index_path)

    def load(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
