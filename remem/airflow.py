  
import datetime as dt
import json
import os
import uuid
from time import sleep

# AIRFLOW IMPORTS
import requests
from airflow import DAG
from airflow.models import Variable
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator

from preprocessing import record_audio_operator, speaker_activity_detection_operator, transcribe_audio_operator

default_args = {
    'owner': 'remem',
    'start_date': dt.datetime(2018, 10, 3, 15, 58, 00),
    'concurrency': 1,
    'retries': 0
}

with DAG('remem_preprocessing',
         catchup=False,
         default_args=default_args,
         schedule_interval="*/1 * * * *",
         ) as dag:

    ## DECLARE OPERATORS
    opr_record_audio = PythonOperator(
            task_id='record_audio_operator',
            python_callable=record_audio_operator, 
            provide_context=True)

    opr_sad = PythonOperator(
            task_id='speaker_activity_detection_operator',
            python_callable=speaker_activity_detection_operator, 
            provide_context=True)

    opr_asr = PythonOperator(
            task_id='transcribe_audio_operator',
            python_callable=transcribe_audio_operator, 
            provide_context=True)

opr_record_audio >> opr_sad >> opr_asr