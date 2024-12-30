from typing import List
import openai
import numpy as np
from ..core.config import BaseEmbedderConfig

class OpenAIEmbedding:
    def __init__(self, config: BaseEmbedderConfig):
        self.config = config
        if config.api_key:
            openai.api_key = config.api_key
            
    def embed(self, text: str) -> List[float]:
        response = openai.Embedding.create(
            model=self.config.model,
            input=text
        )
        return response.data[0].embedding 