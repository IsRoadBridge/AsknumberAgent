from typing import Optional

from langchain_huggingface import HuggingFaceEndpointEmbeddings

from app.conf.app_conf import app_config,EmbeddingConfig


class EmbeddingClient:
    def __init__(self, config: EmbeddingConfig):
        self.client: Optional[HuggingFaceEndpointEmbeddings] = None
        self.config = config

    def _get_url(self):
        return f"http://{self.config.host}:{self.config.port}"

    def init(self):
        self.client = HuggingFaceEndpointEmbeddings(model=self._get_url())



embedding_client = EmbeddingClient(app_config.embedding)