  
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
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator

from preprocessing import record_audio_operator, speaker_activity_detection_operator, transcribe_audio_operator, delete_audio_operator
from preprocessing import NOT_TRANSCRIBE_AUDIO_OPERATOR_ID, TRANSCRIBE_AUDIO_OPERATOR_ID, DELETE_AUDIO_OPERATOR_ID, RECORD_AUDIO_OPERATOR_ID, SPEAKER_ACTIVITY_DETECTION_OPERATOR_ID

default_args = {
    'owner': 'remem',
    'start_date': dt.datetime(2018, 10, 3, 15, 58, 00),
    'concurrency': 1,
    'retries': 0
}

with DAG('remem_preprocessing',
         catchup=False,
         default_args=default_args,
         schedule_interval="*/1 10-23 * * *",
         ) as dag:

    ## DECLARE OPERATORS
    opr_rec= PythonOperator(
            task_id=RECORD_AUDIO_OPERATOR_ID,
            python_callable=record_audio_operator, 
            provide_context=True)

    opr_sad = BranchPythonOperator(
            task_id=SPEAKER_ACTIVITY_DETECTION_OPERATOR_ID,
            python_callable=speaker_activity_detection_operator, 
            provide_context=True)

    opr_asr = PythonOperator(
            task_id=TRANSCRIBE_AUDIO_OPERATOR_ID,
            python_callable=transcribe_audio_operator, 
            provide_context=True)

    opr_not_asr = DummyOperator(
            task_id=NOT_TRANSCRIBE_AUDIO_OPERATOR_ID)

    opr_del = PythonOperator(
            task_id=DELETE_AUDIO_OPERATOR_ID,
            python_callable=delete_audio_operator,
            provide_context=True,
            trigger_rule='none_failed_or_skipped')


opr_rec >> opr_sad 
opr_sad >> opr_asr >> opr_del
opr_sad >> opr_not_asr >> opr_del