import asyncio
import random
from typing import Optional

from qdrant_client import AsyncQdrantClient, models

from app.conf.app_conf import app_config, QDrantConfig


class QrantClient:
    def __init__(self, qrant_config: QDrantConfig):
        self.qrant_config = qrant_config
        self.client: Optional[AsyncQdrantClient] = None

    def init(self):
        self.client = AsyncQdrantClient(host=self.qrant_config.host, port=self.qrant_config.port)

    async def close(self):
        if self.client is not None:
            await self.client.close()


qdrant_client = QrantClient(app_config.qdrant)

if __name__ == '__main__':
    qdrant_client.init()

    async def test():
        client = qdrant_client.client
        if not await client.collection_exists("my_collection"):
            await client.create_collection(
                collection_name="my_collection",
                vectors_config=models.VectorParams(size=10, distance=models.Distance.COSINE),
            )

        await client.upsert(
            collection_name="my_collection",
            points=[
                models.PointStruct(
                    id=i,
                    vector=[random.random() for _ in range(10)],
                )
                for i in range(100)
            ],
        )

        res = await client.query_points(
            collection_name="my_collection",
            query=[random.random() for _ in range(10)],  # type: ignore
            limit=10,
            score_threshold=0.8
        )

        print(res)

    asyncio.run(test())