import json
from datetime import datetime
from pathlib import Path
from typing import List

from ecommerce_analytics.common.config import load_config
from ecommerce_analytics.common.constants import BRONZE_PREFIX
from ecommerce_analytics.common.logger import logger
from ecommerce_analytics.common.s3 import S3Client
from ecommerce_analytics.ingestion.api.client import APIClient
from ecommerce_analytics.ingestion.api.schema import Order


class OrdersExtractor:
    def __init__(self, env: str = "dev"):
        self.config = load_config(env)
        self.client = APIClient(
            base_url=self.config.api.orders_url, timeout=self.config.api.timeout
        )

    def fetch_orders(self) -> List[Order]:
        all_orders = []
        page = 1
        max_pages = 1000

        while True:
            if page > max_pages:
                logger.error("Max page limit reached, stopping execution")
                break

            logger.info(f"Fetching page {page}")

            response = self.client.get(params={"page": page})

            if not isinstance(response, dict):
                logger.error("Invalid response type")
                break

            data = response.get("data", [])
            total_pages = response.get("total_pages")

            if not data:
                logger.warning("No data returned, stopping")
                break

            for item in data:
                try:
                    order = Order(**item)
                    all_orders.append(order)
                except Exception as e:
                    logger.error(f"Schema validation failed: {e}")

            if total_pages and page >= total_pages:
                logger.info("Reached last page")
                break

            page += 1

        logger.info(f"Total orders fetched: {len(all_orders)}")
        return all_orders

    def save_locally(self, orders: List[Order]):
        today = datetime.now().strftime("%Y-%m-%d")

        output_dir = Path("data/raw/orders") / today
        output_dir.mkdir(parents=True, exist_ok=True)

        file_path = output_dir / "orders.json"

        with open(file_path, "w") as f:
            json.dump([o.model_dump() for o in orders], f, default=str, indent=4)

        logger.info(f"Saved data to {file_path}")

    def save_to_s3(self, orders):
        s3_client = S3Client(env=self.config.env)
        if not orders:
            logger.warning("No order to upload")
            return
        data = [o.model_dump() for o in orders]

        s3_client.upload_json(data, prefix=BRONZE_PREFIX)
