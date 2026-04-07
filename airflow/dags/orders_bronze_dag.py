# from ecommerce_analytics.common.logger import logger
import logging
from datetime import datetime

from airflow.providers.standard.operators.python import PythonOperator
from airflow.utils.log.logging_mixin import LoggingMixin

from airflow import DAG
from ecommerce_analytics.ingestion.api.orders_extractor import OrdersExtractor

logger = LoggingMixin().log


def run_orders_ingestion():
    logger.info("Dag started")

    extractor = OrdersExtractor(env="dev")
    logger.info("Extractor object is created")

    orders = extractor.fetch_orders()
    logger.info(f"Here are the orders : {orders}")

    extractor.save_to_s3(orders)
    logger.info("Saved to S3 bucket.")


with DAG(
    dag_id="orders_bronze_pipeline",
    start_date=datetime(2026, 6, 6),
    schedule="*/3 * * * *",
    catchup=False,
    tags=["ecommerce", "bronze"],
) as dag:

    ingest_task = PythonOperator(
        task_id="ingest_orders_to_s3", python_callable=run_orders_ingestion
    )

    ingest_task
