from aios.core.syscall import Syscall
from aios.memos.core.memos import Memos
from aios.memos.core.models import MemoryItem
from aios.memos.core.config import MemoryConfig
from typing import List, Optional, Dict, Any


class MemorySyscall(Syscall):
    def __init__(self, agent_name, query):
        super().__init__(agent_name, query)
        # Create config from query parameters
        config = MemoryConfig(
            vector_store=query.get("vector_store", {}),
            llm=query.get("llm", {}),
            embedder=query.get("embedder", {})
        )
        self.memos = Memos(config)
        
    def add_memory(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> MemoryItem:
        """Add a new memory item"""
        return self.memos.add(text, metadata)
        
    def search_memory(self, query: str, limit: int = 5) -> List[MemoryItem]:
        """Search for memory items"""
        return self.memos.search(query, limit)
        
    def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory item"""
        return self.memos.delete(memory_id)
        
    def run(self):
        """Execute the memory syscall"""
        self.set_pid(self.native_id)
        
        try:
            # Parse the query to determine operation type
            operation = self.query.get("operation")
            
            if operation == "add":
                result = self.add_memory(
                    self.query.get("text"),
                    self.query.get("metadata")
                )
            elif operation == "search":
                result = self.search_memory(
                    self.query.get("query"),
                    self.query.get("limit", 5)
                )
            elif operation == "delete":
                result = self.delete_memory(self.query.get("memory_id"))
            else:
                raise ValueError(f"Unknown operation: {operation}")
                
            self.set_response(result)
            self.set_status("done")
            
        except Exception as e:
            self.set_response(str(e))
            self.set_status("error")
            
        finally:
            self.event.set()