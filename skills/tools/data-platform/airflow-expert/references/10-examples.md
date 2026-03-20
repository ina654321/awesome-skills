# Examples

## 10.1 Basic DAG

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'my_first_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:
    
    start = BashOperator(
        task_id='start',
        bash_command='echo "Starting pipeline"',
    )
    
    process = BashOperator(
        task_id='process',
        bash_command='echo "Processing data"',
    )
    
    end = BashOperator(
        task_id='end',
        bash_command='echo "Pipeline complete"',
    )
    
    start >> process >> end
```

## 10.2 Task Dependencies

```python
# Sequential
task1 >> task2 >> task3

# Parallel
[task1, task2] >> task3

# Branching
task1 >> BranchPythonOperator(
    task_id='branch',
    python_callable=lambda: 'task_a' if True else 'task_b'
)
```

## 10.3 PythonOperator

```python
from airflow.operators.python import PythonOperator

def process_data(**context):
    data = context['task_instance'].xcom_pull(task_ids='extract')
    processed = [x.upper() for x in data]
    return processed

extract = PythonOperator(
    task_id='extract',
    python_callable=lambda: ['a', 'b', 'c'],
    provide_context=True,
)

transform = PythonOperator(
    task_id='transform',
    python_callable=process_data,
    provide_context=True,
)

extract >> transform
```

## 10.4 Sensor

```python
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.base import BaseSensorOperator

# File sensor
wait_for_file = FileSensor(
    task_id='wait_for_file',
    poke_interval=60,
    timeout=3600,
    filepath='/data/input.csv',
)

# Custom sensor
class MySensor(BaseSensorOperator):
    def poke(self, context):
        return check_condition()
```

## 10.5 Variables and XCom

```python
from airflow.models import Variable
from airflow.operators.python import PythonOperator

# Get variable
api_key = Variable.get('api_key')

# Set variable
Variable.set('my_var', 'my_value')

# XCom push
def push_data(**context):
    context['task_instance'].xcom_push(key='data', value={'key': 'value'})

# XCom pull
def pull_data(**context):
    data = context['task_instance'].xcom_pull(task_ids='push_task', key='data')
```

## 10.6 Connections

```python
from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.http_hook import HttpHook

# Use hook
pg_hook = PostgresHook(postgres_conn_id='my_postgres')
conn = pg_hook.get_conn()
df = pg_hook.get_pandas_df('SELECT * FROM table')

# HTTP hook
http_hook = HttpHook(method='GET', http_conn_id='my_api')
response = http_hook.run('/endpoint')
```

## 10.7 BigQuery Integration

```python
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryInsertJobOperator,
    BigQueryCheckOperator
)

run_query = BigQueryInsertJobOperator(
    task_id='run_query',
    project_id='my-project',
    configuration={
        'query': {
            'query': 'SELECT * FROM dataset.table',
            'useLegacySql': False
        }
    }
)

check_data = BigQueryCheckOperator(
    task_id='check_data',
    sql='SELECT COUNT(*) FROM dataset.table',
    pass_value=1,
    useLegacySql=False,
)
```

## 10.8 Kubernetes Operator

```python
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

run_pod = KubernetesPodOperator(
    task_id='run_pod',
    name='my-pod',
    namespace='default',
    image='python:3.9',
    cmds=['python', '-c', 'print("Hello")'],
    get_logs=True,
    dag=dag,
)
```

## 10.9 Trigger Rules

```python
from airflow.utils.trigger_rule import TriggerRule

# Default: all upstream succeeded
task1 >> task2

# Custom trigger rules
task2.trigger_rule = TriggerRule.ALL_FAILED
task3.trigger_rule = TriggerRule.ALL_DONE
task4.trigger_rule = TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
```

## 10.10 Callbacks

```python
def on_failure(context):
    print(f"DAG failed: {context['dag_run'].dag_id}")
    send_alert(context)

def on_retry(context):
    print(f"Task retry: {context['task_instance'].task_id}")

default_args = {
    'on_failure_callback': on_failure,
    'on_retry_callback': on_retry,
}
```