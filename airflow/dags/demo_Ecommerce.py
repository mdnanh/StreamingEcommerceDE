from datetime import datetime
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
import pandas as pd
import random
import time
import json
from kafka import KafkaProducer
from kafka.errors import KafkaError

product_list= pd.read_csv("./data/data_ncds_full.csv")
city= pd.read_csv("./data/city.csv", index_col= False)

KAFKA_HOST_IP="kafka"
TOPIC = 'Ecommerce'
PRODUCT_LIST= product_list.to_dict(orient='records')
CITY_LIST=city.to_dict(orient='records')
STATUS_LIST= ["FAILED", "COMPLETED"]
WEIGHTS = [0.2, 0.8]

# Messages will be serialized as JSON 
def serializer(message):
    return json.dumps(message).encode('utf-8')

kafka_p = KafkaProducer(
    bootstrap_servers = [f'{KAFKA_HOST_IP}:29092'],  
    value_serializer=serializer
)


def generate_purchase_id():
    timestamp = int(time.time() * 1000)  # Lấy timestamp hiện tại (milliseconds)
    random_number = random.randint(1000, 9999)  # Số ngẫu nhiên 4 chữ số
    return f"P{timestamp}{random_number}"

def genMessage() -> dict:
    product= random.choice(PRODUCT_LIST)
    product['purchase_id']= generate_purchase_id()
    product['quantity'] = random.randint(1,5)
    product['total_price']= product['price']*product['quantity']
    province= random.choice(CITY_LIST)
    product['city'] = province.get('city')
    product['code_city']= province.get('code')
    product['status']= random.choices(STATUS_LIST, weights= WEIGHTS)[0]
    product['create_at']= datetime.now().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
    return product

def send_message():
    dummy_message = genMessage()
    print(f'Producing message @ {datetime.now()} | Message = {str(dummy_message)}')
    try:
        future = kafka_p.send(TOPIC, dummy_message)
        future.get(timeout=10)  # Đợi kết quả với timeout
        print("Message sent successfully")
    except KafkaError as e:
        print(f"Failed to send message: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


dag =  DAG(
    dag_id='DemoEcommerce',
    description="This DAG runs a full workflow for Demo druid and superset.",
    # schedule_interval=None,
    schedule_interval='* * * * *',
    start_date= datetime(2024, 10, 6),
    tags=['Ecommerce'],)

    
    
producer_task = PythonOperator(
    task_id="producer",
    provide_context=True,
    python_callable=send_message,
    dag= dag
)

producer_task