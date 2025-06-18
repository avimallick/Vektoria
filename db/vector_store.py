# vector_store.py
import faiss
import numpy as np
import os
import pickle

class VectorStore:
    def __init__(self, dim: int, index_path: str = "faiss.index"):
        self.dim = dim
        self.index_path = index_path

        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        else:
            self.index = faiss.IndexFlatL2(dim)
        
        self.id_map = {}
        self.next_id = 0

    def add(self, vectors: np.ndarray, metadata: list):
        ids = np.arange(self.next_id, self.next_id + len(vectors))
        self.index.add(vectors)
        for i, meta in zip(ids, metadata):
            self.id_map[int(i)] = meta
        self.next_id += len(vectors)
        self.save()

    def search(self, query_vector: np.ndarray, k: int = 5):
        D, I = self.index.search(query_vector, k)
        return [self.id_map.get(int(i), {}) for i in I[0]]

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.index_path + ".meta", "wb") as f:
            pickle.dump(self.id_map, f)

    def load_metadata(self):
        if os.path.exists(self.index_path + ".meta"):
            with open(self.index_path + ".meta", "rb") as f:
                self.id_map = pickle.load(f)
                self.next_id = max(self.id_map.keys(), default=-1) + 1
