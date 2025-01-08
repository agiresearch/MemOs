from typing import Dict, Any
from ..memos.core.memos import Memos
from ..memos.core.config import MemoryConfig

async def handle_memory_syscall(operation: str, **kwargs) -> Dict[str, Any]:
    """Handle memory-related system calls"""
    # Get or create Memos instance
    config = MemoryConfig()  # You'll need to load this from your config system
    memos = Memos(config)
    
    if operation == "add":
        text = kwargs.get("text")
        metadata = kwargs.get("metadata")
        if not text:
            raise ValueError("Text is required for add operation")
        
        memory_item = memos.add(text, metadata)
        return {
            "status": "success",
            "memory_item": memory_item.dict()
        }
        
    elif operation == "search":
        query = kwargs.get("query")
        limit = kwargs.get("limit", 5)
        if not query:
            raise ValueError("Query is required for search operation")
            
        results = memos.search(query, limit)
        return {
            "status": "success",
            "results": [item.dict() for item in results]
        }
        
    elif operation == "delete":
        memory_id = kwargs.get("memory_id")
        if not memory_id:
            raise ValueError("Memory ID is required for delete operation")
            
        success = memos.delete(memory_id)
        return {
            "status": "success" if success else "error",
            "message": f"Memory {memory_id} {'deleted' if success else 'not found'}"
        }
        
    else:
        raise ValueError(f"Unsupported memory operation: {operation}")
