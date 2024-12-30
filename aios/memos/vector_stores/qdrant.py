from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from ..core.models import MemoryItem

class Qdrant:
    def __init__(self, collection_name: str, host: str = "localhost", port: int = 6333):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        
    def initialize(self, dimension: int):
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=dimension, distance=Distance.COSINE)
        )
        
    def add(self, id: str, vector: List[float], metadata: Optional[Dict[str, Any]] = None):
        self.client.upsert(
            collection_name=self.collection_name,
            points=[{
                "id": id,
                "vector": vector,
                "payload": metadata or {}
            }]
        )
        
    def search(self, query_vector: List[float], limit: int = 5) -> List[MemoryItem]:
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )
        return [
            MemoryItem(
                id=str(r.id),
                memory=r.payload.get("text", ""),
                metadata=r.payload,
                score=r.score
            ) for r in results
        ]
        
    def delete(self, id: str) -> bool:
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=[id]
        )
        return True
        
    def clear(self) -> bool:
        self.client.delete_collection(self.collection_name)
        return True 