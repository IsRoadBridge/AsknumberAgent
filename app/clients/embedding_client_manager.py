from typing import Optional

from huggingface_hub import AsyncInferenceClient

from app.conf.app_config import EmbeddingConfig, app_config


class LocalEmbeddingClient:
    """轻量级本地 TEI Embedding 客户端，直接调用本地 TEI 服务的 feature_extraction 接口"""

    def __init__(self, client: AsyncInferenceClient):
        self._client = client

    async def aembed_query(self, text: str) -> list[float]:
        return (await self.aembed_documents([text]))[0]

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        texts = [text.replace("\n", " ") for text in texts]
        responses = await self._client.feature_extraction(text=texts)
        return responses.tolist()


class EmbeddingClientManager:
    def __init__(self, config: EmbeddingConfig):
        self.client: Optional[LocalEmbeddingClient] = None
        self.config = config

    def _get_url(self):
        return f"http://{self.config.host}:{self.config.port}"

    def init(self):
        async_client = AsyncInferenceClient(model=self._get_url())
        self.client = LocalEmbeddingClient(async_client)


embedding_client_manager = EmbeddingClientManager(app_config.embedding)
