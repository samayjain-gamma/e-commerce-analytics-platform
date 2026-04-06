from pathlib import Path

import yaml
from pydantic import BaseModel


class AWSConfig(BaseModel):
    region: str


class S3Config(BaseModel):
    bronze_bucket: str
    silver_bucket: str


class APIConfig(BaseModel):
    orders_url: str
    timeout: int


class AppConfig(BaseModel):
    env: str
    aws: AWSConfig
    s3: S3Config
    api: APIConfig


def load_config(env: str = "dev") -> AppConfig:
    config_path = Path("config") / f"{env}.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r") as f:
        data = yaml.safe_load(f)

    return AppConfig(**data)


config = load_config()
