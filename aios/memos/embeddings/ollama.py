from typing import List
import requests
import numpy as np
from ..core.config import BaseEmbedderConfig

class OllamaEmbedding:
    def __init__(self, config: BaseEmbedderConfig):
        self.config = config
        self.base_url = "http://localhost:11434"
        
    def embed(self, text: str) -> List[float]:
        response = requests.post(
            f"{self.base_url}/api/embeddings",
            json={
                "model": self.config.model,
                "prompt": text
            }
        )
        return response.json()["embedding"] 