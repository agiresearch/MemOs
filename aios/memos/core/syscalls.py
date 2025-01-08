from typing import Dict, Any, Optional, List
from .memos import Memos
from .config import MemoryConfig

class MemorySystemCalls:
    def __init__(self, memos: Memos):
        self.memos = memos

    async def handle_memory_syscall(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Handle memory-related system calls"""
        if operation == "add":
            return await self._handle_add_memory(**kwargs)
        elif operation == "search":
            return await self._handle_search_memory(**kwargs)
        elif operation == "delete":
            return await self._handle_delete_memory(**kwargs)
        else:
            raise ValueError(f"Unsupported memory operation: {operation}")

    async def _handle_add_memory(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Handle adding new memory"""
        memory_item = self.memos.add(text, metadata)
        return {
            "status": "success",
            "memory_item": memory_item.dict()
        }

    async def _handle_search_memory(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """Handle memory search"""
        results = self.memos.search(query, limit)
        return {
            "status": "success",
            "results": [item.dict() for item in results]
        }

    async def _handle_delete_memory(self, memory_id: str) -> Dict[str, Any]:
        """Handle memory deletion"""
        success = self.memos.delete(memory_id)
        return {
            "status": "success" if success else "error",
            "message": f"Memory {memory_id} {'deleted' if success else 'not found'}"
        }
