import pandas as pd
import random
import time
from datetime import datetime
import json
from kafka import KafkaProducer


product_list= pd.read_csv("data_ncds_full.csv")
city= pd.read_csv("city.csv", index_col= False)

KAFKA_HOST_IP="localhost"
TOPIC = 'Ecommerce'
PRODUCT_LIST= product_list.to_dict(orient='records')
CITY_LIST=city.to_dict(orient='records')
STATUS_LIST= ["FAILED", "COMPLETED"]
WEIGHTS = [0.2, 0.8]


# Messages will be serialized as JSON 
def serializer(message):
    return json.dumps(message).encode('utf-8')

kafka_p = KafkaProducer(
    bootstrap_servers = [f'{KAFKA_HOST_IP}:9092'],  
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

def demo_func():
    dummy_message = genMessage()
    print(f'Producing message @ {datetime.now()} | Message = {str(dummy_message)}')
    kafka_p.send(TOPIC, dummy_message)

while True:
    demo_func()
    time.sleep(1)
