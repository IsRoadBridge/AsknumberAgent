import asyncio
from typing import Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from app.conf.app_conf import app_config, DBConfig


class MysqlClient:
    def __init__(self, dbconfig: DBConfig):
        self.dbConfig = dbconfig
        self.engine: Optional[AsyncEngine] = None
        self.session_factory = None

    def get_url(self) -> str:
        # DATABASE_URL = "mysql+asyncmy://user:password@localhost:3306/mydb?charset=utf8mb4"
        return f"mysql+asyncmy://{self.dbConfig.user}:{self.dbConfig.password}+@{self.dbConfig.host}:{self.dbConfig.port}/{self.dbConfig.database}?charset=utf8mb4"

    def init(self):
        # 1. 创建异步引擎
        self.engine: AsyncEngine = create_async_engine(
            self.get_url(),
            pool_size=10,  # 连接池大小
            max_overflow=20,  # 超出 pool_size 时最多额外创建的连接数
            pool_recycle=3600,  # 连接回收时间（秒），对 MySQL 很重要，避免 8 小时断开
            pool_pre_ping=True,  # 使用前检测连接有效性
            pool_timeout=30,  # 获取连接的超时时间
            echo=False  # 是否打印 SQL 日志
        )

        # 2. 创建 async_sessionmaker 会话工厂
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,  # 提交后不自动过期对象（常用配置）
            autoflush=True,  # 可选的，按需设置自动 flush
            autobegin=True
        )

    async def close(self):
        if self.engine is not None:
            await self.engine.dispose()


dw_mysql_client = MysqlClient(app_config.db_dw)
meta_mysql_client = MysqlClient(app_config.db_meta)

if __name__ == '__main__':
    dw_mysql_client.init()

    async def test():
        async with dw_mysql_client.session_factory() as session:
            result = await session.execute(text("select * from table_info"))
            rows = result.fetchall()
            print(rows)

    asyncio.run(test())