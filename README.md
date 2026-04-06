### The Project: E-Commerce Analytics Platform

Build a complete, production-grade data platform.

**Tech Stack:**
- **Cloud:** AWS (or GCP/Azure)
- **Storage:** S3 + Delta Lake
- **Compute:** AWS Glue for ETL
- **Warehouse:** Snowflake or Redshift
- **Transformation:** dbt
- **Orchestration:** Airflow
- **IaC:** Terraform
- **Monitoring:** CloudWatch + custom dashboard

**Data Sources:**
1. Orders API (REST, paginated, 100K orders/day)
2. Customer database (PostgreSQL with CDC)
3. Product catalog (CSV in S3, daily)
4. Clickstream events (simulated Kafka stream)

**Architecture:**

**Bronze Layer (Raw):**
- Glue job: ingest Orders API → S3 as JSON
- Glue job: CDC from Postgres → S3 as Parquet
- Glue job: copy Product CSV → S3
- (Bonus: Kafka → Kinesis → S3)

**Silver Layer (Cleaned):**
- Glue job: dedupe, validate, standardize → Delta Lake format
- Schema validation
- Data quality checks

**Gold Layer (Aggregated):**
- Load Silver data to Snowflake
- dbt transformations:
- Staging: clean column names, cast types
- Intermediate: join orders + customers + products
- Marts: daily revenue, customer LTV, product affinity

**Orchestration:**
- Airflow DAG: Bronze → Silver → Gold pipeline
- Run daily at 2 AM UTC
- Parallel processing where possible
- Retries: 3 attempts with exponential backoff

**Data Quality:**
- Great Expectations checks in Silver layer
- dbt tests in Gold layer
- Alert if critical tests fail

**Monitoring:**
- Pipeline duration, row counts, error rates
- Data freshness (warn if > 6 hours old)
- Cost tracking per job

**Infrastructure:**
- All resources defined in Terraform
- Separate dev/prod environments
- Git-based deployment

**Deliverables:**
1. Working end-to-end pipeline
2. dbt documentation site
3. Monitoring dashboard
4. Architecture diagram
5. README with design decisions