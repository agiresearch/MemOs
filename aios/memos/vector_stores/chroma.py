from typing import List, Dict, Any, Optional
import chromadb
from ..core.models import MemoryItem

class ChromaDB:
    def __init__(self, collection_name: str, path: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(collection_name)
        
    def add(self, id: str, vector: List[float], metadata: Optional[Dict[str, Any]] = None):
        self.collection.add(
            embeddings=[vector],
            ids=[id],
            metadatas=[metadata or {}]
        )
        
    def search(self, query_vector: List[float], limit: int = 5) -> List[MemoryItem]:
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=limit
        )
        
        memories = []
        for i in range(len(results['ids'][0])):
            memories.append(MemoryItem(
                id=results['ids'][0][i],
                memory=results['metadatas'][0][i].get("text", ""),
                metadata=results['metadatas'][0][i],
                score=results['distances'][0][i] if 'distances' in results else None
            ))
        return memories
        
    def delete(self, id: str) -> bool:
        self.collection.delete(ids=[id])
        return True
        
    def clear(self) -> bool:
        self.client.delete_collection(self.collection_name)
        return True 