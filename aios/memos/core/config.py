from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class VectorStoreConfig(BaseModel):
    provider: str = Field(default="qdrant", description="Vector store provider name")
    collection_name: str = Field(default="memories", description="Collection name in vector store")
    config: Dict[str, Any] = Field(default_factory=dict, description="Provider-specific config")

class LlmConfig(BaseModel):
    provider: str = Field(default="openai", description="LLM provider name")
    config: Dict[str, Any] = Field(default_factory=dict, description="Provider-specific config")

class EmbedderConfig(BaseModel):
    provider: str = Field(default="openai", description="Embedding provider name")
    config: Dict[str, Any] = Field(default_factory=dict, description="Provider-specific config")
    embedding_dims: int = Field(default=1536, description="Embedding dimensions")

class BaseLlmConfig(BaseModel):
    model: str = Field(default="gpt-3.5-turbo", description="Model name")
    temperature: float = Field(default=0.0, description="Model temperature")
    max_tokens: Optional[int] = Field(default=None, description="Max tokens")
    api_key: Optional[str] = Field(default=None, description="API key")

class BaseEmbedderConfig(BaseModel):
    model: str = Field(default="text-embedding-ada-002", description="Model name")
    api_key: Optional[str] = Field(default=None, description="API key")
    embedding_dims: int = Field(default=1536, description="Embedding dimensions")

class MemoryConfig(BaseModel):
    vector_store: VectorStoreConfig = Field(
        description="Configuration for the vector store",
        default_factory=VectorStoreConfig,
    )
    llm: LlmConfig = Field(
        description="Configuration for the language model",
        default_factory=LlmConfig,
    )
    embedder: EmbedderConfig = Field(
        description="Configuration for the embedding model",
        default_factory=EmbedderConfig,
    )
    custom_prompt: Optional[str] = Field(
        description="Custom prompt for the memory",
        default=None,
    ) 