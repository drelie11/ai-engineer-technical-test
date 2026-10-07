import numpy as np

class SimpleVectorDB:
    def __init__(self):
        self.vectors = {}
        self.metadata = {}

    def insert(self, doc_id: str, vector: list, meta: dict = None):
        # Convert normal array into numpy array
        self.vectors[doc_id] = np.array(vector)
        if meta:
            self.metadata[doc_id] = meta

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        dot_product = np.sum(vec1 * vec2)
        
        norm_vec1 = np.sqrt(np.sum(vec1 ** 2))
        norm_vec2 = np.sqrt(np.sum(vec2 ** 2))
        
        if norm_vec1 == 0 or norm_vec2 == 0:
            return 0.0
            
        return float(dot_product / (norm_vec1 * norm_vec2))

    def search(self, query_vector: list, top_k: int = 3) -> list:
        query_arr = np.array(query_vector)
        scores = []
        
        for doc_id, stored_vec in self.vectors.items():
            sim_score = self._cosine_similarity(query_arr, stored_vec)
            scores.append({
                "id": doc_id,
                "score": sim_score,
                "metadata": self.metadata.get(doc_id, {})
            })
            
        scores.sort(key=lambda x: x["score"], reverse=True)
        
        return scores[:top_k]

if __name__ == "__main__":
    db = SimpleVectorDB()
    
    # Dummy embedding vectors
    db.insert("prod_1", [0.9, 0.1, 0.05, 0.2], {"name": "Mouse", "category": "Electronics"})
    db.insert("prod_2", [0.65, 0.25, 0.1, 0.35], {"name": "Keyboard", "category": "Electronics"})
    db.insert("prod_3", [0.4, 0.5, 0.3, 0.75], {"name": "Shoes", "category": "Clothing"})
    db.insert("prod_4", [0.0, 0.9, 0.8, 0.1], {"name": "Badminton Racket", "category": "Sports"})

    query = [0.15, 0.8, 0.75, 0.07]
    print(f"Searching for query vector: {query}\n")
    
    results = db.search(query, top_k=2)
    
    for rank, result in enumerate(results, 1):
        print(f"Rank {rank}: {result['metadata']['name']} (ID: {result['id']})")
        print(f"Similarity Score: {result['score']:.4f}\n")