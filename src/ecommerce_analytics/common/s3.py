import json
from datetime import datetime

import boto3

from ecommerce_analytics.common.config import load_config
from ecommerce_analytics.common.logger import logger


class S3Client:
    def __init__(self, env: str = "dev"):
        config = load_config(env)
        self.bucket = config.s3.bronze_bucket
        self.s3 = boto3.client("s3")

    def _build_key(self, prefix: str) -> str:
        date_str = datetime.now().strftime("%Y-%m-%d")
        return f"{prefix}/date={date_str}/data.json"

    def upload_json(self, data: list, prefix: str):
        key = self._build_key(prefix)

        logger.info(f"Uploading to s3://{self.bucket}/{key}")

        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=json.dumps(data, default=str),
            ContentType="application/json",
        )

        logger.info("Upload complete")
