from ecommerce_analytics.common.config import config
from ecommerce_analytics.common.logger import logger

# config = load_config("dev")

logger.info(f"Environment: {config.env}")
logger.info(f"S3 Bronze Bucket: {config.s3.bronze_bucket}")
logger.info(f"Orders API: {config.api.orders_url}")
