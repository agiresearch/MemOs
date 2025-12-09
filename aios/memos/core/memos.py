from typing import List, Optional, Dict, Any
from .models import MemoryItem
from .config import MemoryConfig
from .factories import LlmFactory, EmbedderFactory, VectorStoreFactory
import uuid
from datetime import datetime

class Memos:
    def __init__(self, config: MemoryConfig):
        self.config = config
        # Merge collection_name into the config dict for the factory
        vs_config = config.vector_store.config.copy()
        if "collection_name" not in vs_config:
            vs_config["collection_name"] = config.vector_store.collection_name

        self.vector_store = VectorStoreFactory.create(
            config.vector_store.provider, 
            vs_config
        )
        self.llm = LlmFactory.create(
            config.llm.provider, 
            config.llm.config
        )
        self.embedder = EmbedderFactory.create(
            config.embedder.provider, 
            config.embedder.config
        )

    def add(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> MemoryItem:
        # Create memory item
        memory_item = MemoryItem(
            id=str(uuid.uuid4()),
            memory=text,
            metadata=metadata,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        # Get embeddings
        embeddings = self.embedder.embed(text)
        
        # Store in vector store
        # Ensure text is in metadata for retrieval
        store_metadata = metadata.copy() if metadata else {}
        store_metadata["text"] = text
        self.vector_store.add(memory_item.id, embeddings, store_metadata)
        
        return memory_item

    def search(self, query: str, limit: int = 5) -> List[MemoryItem]:
        # Get query embeddings
        query_embedding = self.embedder.embed(query)
        
        # Search vector store
        results = self.vector_store.search(query_embedding, limit=limit)
        
        return results

    def delete(self, memory_id: str) -> bool:
        return self.vector_store.delete(memory_id)

    def clear(self) -> bool:
        return self.vector_store.clear() 