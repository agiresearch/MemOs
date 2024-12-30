from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class MemoryItem(BaseModel):
    id: str = Field(..., description="The unique identifier for the text data")
    memory: str = Field(..., description="The memory content")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    score: Optional[float] = Field(None, description="The score associated with the memory")
    created_at: Optional[str] = Field(None, description="Creation timestamp")
    updated_at: Optional[str] = Field(None, description="Update timestamp") 