
# Memos

A flexible and extensible memory management system that supports multiple LLMs, vector stores, and embedding providers.

## Features

- 🧠 Multiple LLM Support (OpenAI, Anthropic, Ollama)
- 🔤 Embedding Providers (OpenAI, Ollama)
- 💾 Vector Store Integrations (Qdrant, ChromaDB)
- ⚙️ Flexible Configuration & Extensible Architecture

## Quick Start

```python
from aios.memos.core import Memos, MemoryConfig, VectorStoreConfig, LlmConfig, EmbedderConfig

# Configure
config = MemoryConfig(
    vector_store=VectorStoreConfig(provider="qdrant"),
    llm=LlmConfig(provider="openai"),
    embedder=EmbedderConfig(provider="openai")
)

# Initialize
memos = Memos(config)

# Add memory
memory = memos.add("The sky was beautiful today", {"tag": "observation"})

# Search
results = memos.search("What about the sky?")
```

## Installation

```bash
pip install aios-memos
```

## License

MIT License
