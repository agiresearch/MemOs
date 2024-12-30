from ..utils.class_loader import load_class
from .config import BaseLlmConfig, BaseEmbedderConfig

class LlmFactory:
    provider_to_class = {
        "ollama": "aios.memos.llms.ollama.OllamaLLM",
        "openai": "aios.memos.llms.openai.OpenAILLM",
        "anthropic": "aios.memos.llms.anthropic.AnthropicLLM",
    }

    @classmethod
    def create(cls, provider_name, config):
        class_type = cls.provider_to_class.get(provider_name)
        if class_type:
            llm_instance = load_class(class_type)
            base_config = BaseLlmConfig(**config)
            return llm_instance(base_config)
        else:
            raise ValueError(f"Unsupported Llm provider: {provider_name}")

class EmbedderFactory:
    provider_to_class = {
        "openai": "aios.memos.embeddings.openai.OpenAIEmbedding",
        "ollama": "aios.memos.embeddings.ollama.OllamaEmbedding",
    }

    @classmethod
    def create(cls, provider_name, config):
        class_type = cls.provider_to_class.get(provider_name)
        if class_type:
            embedder_instance = load_class(class_type)
            base_config = BaseEmbedderConfig(**config)
            return embedder_instance(base_config)
        else:
            raise ValueError(f"Unsupported Embedder provider: {provider_name}")

class VectorStoreFactory:
    provider_to_class = {
        "qdrant": "aios.memos.vector_stores.qdrant.Qdrant",
        "chroma": "aios.memos.vector_stores.chroma.ChromaDB",
    }

    @classmethod
    def create(cls, provider_name, config):
        class_type = cls.provider_to_class.get(provider_name)
        if class_type:
            if not isinstance(config, dict):
                config = config.model_dump()
            vector_store_instance = load_class(class_type)
            return vector_store_instance(**config)
        else:
            raise ValueError(f"Unsupported VectorStore provider: {provider_name}") 