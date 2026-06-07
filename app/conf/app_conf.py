from dataclasses import dataclass
from pathlib import Path

from omegaconf import OmegaConf


@dataclass
class LoggerFile:
    enable: bool
    level: str
    path: str
    rotation: str
    retention: str

@dataclass
class Console:
    enable: bool
    level: str

@dataclass
class Logger:
    file: LoggerFile
    console: Console

@dataclass
class DBMeta:
    host: str
    port: int
    user: str
    password: str
    database: str

@dataclass
class DBDw:
    host: str
    port: int
    user: str
    password: str
    database: str

@dataclass
class QDrant:
    host: str
    port: int
    embedding_size: int

@dataclass
class Embedding:
    host: str
    port: int
    model: str

@dataclass
class ES:
    host: str
    port: int
    index_name: str

@dataclass
class LLM:
    model_name: str
    api_key: str
    base_url: str

@dataclass
class AppConf:
    logging: Logger
    db_meta: DBMeta
    db_dw: DBDw
    qdrant: QDrant
    embedding: Embedding
    es: ES
    llm: LLM

# Path(__file__)获取当前文件所在目录（不是工作目录）
#path = Path(__file__).parents[2]/"conf/app_config.yaml"
config_file = Path(__file__).parents[2] / 'conf' / 'app_config.yaml'
context = OmegaConf.load(config_file)
schema = OmegaConf.structured(AppConf)
#merged = OmegaConf.merge(schema, conf)
#app = OmegaConf.to_object(merged)
# 提供一个全局的app_config，且是单例模式
app_config: AppConf = OmegaConf.to_object(OmegaConf.merge(schema, context))
print(app_config)