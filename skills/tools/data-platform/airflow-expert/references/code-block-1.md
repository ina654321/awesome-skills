# python Example

```
from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.s3 import S3CopyOperator

default_args = {
    'owner': 'data-engineer',
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(minutes=30),
}

with DAG(
    'etl_pipeline',
    default_args=default_args,
    schedule_interval='0 2 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    doc_md="""
    # ETL Pipeline DAG

    ## Overview
    Extracts data from API, transforms, and loads to warehouse.

    ## Schedule
    Runs daily at 2 AM UTC.
    """,
) as dag:

    @task
    def extract(**context):
        """Extract from API and push to XCom."""
        data = api.fetch_orders(date=context['logical_date'])
        return data  # Auto-XCom if small

    @task
    def transform(data):
        """Transform extracted data."""
        return transform_orders(data)

    @task
    def load(transformed_data):
        """Load to warehouse."""
        warehouse.insert(transformed_data)

    @task
    def notify_success(**context):
        """Send notification on success."""
        dag_run = context['dag_run']
        print(f"DAG {dag_run.dag_id} completed at {dag_run.end_date}")

    extract() >> transform() >> load() >> notify_success()
```
