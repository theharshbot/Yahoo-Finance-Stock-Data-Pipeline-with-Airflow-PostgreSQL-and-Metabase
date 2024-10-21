import os
import sys
from datetime import datetime, timedelta
import pandas as pd
import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator



from stock_functions import extract, transform, load




dag=DAG(
    dag_id="Stock_Finance_Data",
    default_args={
        "owner":"airflow",
        "start_date":datetime(2024,1,1)
    },
    schedule_interval=None,
    catchup= False
)



extract_task=PythonOperator(
    task_id="extract_data_from_yahoo_finance_stock_data",
    python_callable=extract,
    op_kwargs={"url":"https://finance.yahoo.com/markets/stocks/most-active/"},
    dag=dag
)


transform_task=PythonOperator(
    task_id="Transform_Stock_Data",
    python_callable=transform,
    dag=dag
)


load_task=PythonOperator(
    task_id="Load_phase",
    python_callable=load,
    dag=dag
)



extract_task >> transform_task >> load_task