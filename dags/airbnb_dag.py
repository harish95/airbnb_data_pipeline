import configparser
import datetime
import os
from crawler.airbnb_crawler import get_listing_data
from etl.airbnb_etl import clean_data
from etl.s3_upload_etl import upload_file_to_s3
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.dates import days_ago
from airflow.operators.empty import EmptyOperator


parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__),'../config/config.conf'))

city = parser.get('crawl_parameters','city')
state = parser.get('crawl_parameters','state')
country = parser.get('crawl_parameters','country')


aws_parser = configparser.ConfigParser()

aws_parser.read('/opt/airflow/config/config.conf')

aws_access_key = aws_parser.get("aws_parameters","AWS_ACCESS_KEY")
aws_secret_key = aws_parser.get("aws_parameters","AWS_SECRET_KEY")




# Fetch HTML content
url = "https://insideairbnb.com/get-the-data/"

# get latest date and check for data
#date = get_dates(url)
#date = "2024-09-05"
today = datetime.datetime.today().date()
print(today)
date = today
# status = get_listing_data(today,city,state,country)
#
# if status:
#     clean_data(status)
# else:
#     print("Data not updated!!!!")


with DAG(
    dag_id="airbnb_data_pipeline",
    default_args={'owner':'airflow'},
    schedule_interval='@daily',
    start_date=days_ago(1),
    ) as dag :

    data_status = BranchPythonOperator(
        task_id="check_and_download_data",
        python_callable=get_listing_data,
        op_kwargs= { 'date' : str(date) ,
                     'city': city,
                     'state': state,
                     'country': country},
    )


    clean_data_task = PythonOperator(
        task_id="clean_data",
        python_callable=clean_data,
        op_kwargs= {'data_name': f"/opt/airflow/data/input/{city}_{date}_listings.csv"},
    )

    data_not_updated = EmptyOperator(
        task_id="data_not_updated"
    )

    s3_upload = PythonOperator(
        task_id="Upload_To_S3",
        python_callable=upload_file_to_s3,
        op_kwargs={'file_name':f"/opt/airflow/data/output/{city}_{date}_listings.csv",
                   'bucket_name':'hbx-airbnb',
                   'object_name':f"airbnb_landing/{city}_{date}_listings.csv",
                   'aws_access_key_id':aws_access_key,
                    'aws_secret_access_key':aws_secret_key}
    )


    data_status >> [clean_data_task,data_not_updated]
    clean_data_task >> s3_upload


