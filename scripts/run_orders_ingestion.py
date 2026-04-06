from ecommerce_analytics.common.logger import logger
from ecommerce_analytics.ingestion.api.orders_extractor import OrdersExtractor

if __name__ == "__main__":
    extractor = OrdersExtractor(env="dev")

    orders = extractor.fetch_orders()
    extractor.save_locally(orders)

    logger.info("Ingestion completed")
