# StreamingEcommerceDE

## Description
This project focuses on building a real-time e-commerce data streaming pipeline using [Apache Kafka](https://kafka.apache.org/quickstart), [Apache Druid](https://github.com/apache/druid), and [MinIO](https://github.com/minio/minio), all deployed via [Docker](https://docs.docker.com/). The system captures real-time data streams from an e-commerce platform, stores and processes metadata in Druid for fast querying and analysis, while using MinIO as deep storage for long-term data retention. Apache Superset is used to visualize the data, providing real-time insights and dashboards for better decision-making. This setup ensures scalability, performance, and efficiency in handling and analyzing large volumes of streaming data.
## Architecture
![alt text](https://github.com/mdnanh/StreamingEcommerceDE/blob/main/images/architecture.png)

## Init
### 1. Installation
This project is built with docker compose, so make sure you have docker and docker-compose installed. Follow the steps instructed in [Docker](https://docs.docker.com/get-started/get-docker/) to install it. 
Then, pull this repo and start the journey.

### 2. Start services
```sh
cd StreamingEcommerceDE
```
* For the first time, start the MiniO service first to initialize the deepstorage containing the streaming data. Change two param `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` by yourself in file `docker-compose.yml` at the block `minio` service. Then, run command:
```sh
docker-compose up -d minio
```
* Follow this [step-by-step to run Druid with deepstorage Minio](https://blog.min.io/how-to-druid-superset-minio/) to clearly. 
Now, Minio server is running on port `localhost:9001`, login to the server and create a `druidbucket` to store segments and indexing_logs, create a service account (under the Identity menu), edit the user policy to only allow access to `druidbucket` and in the Druid configuration (`./druid/environment`) below use the service account’s `access key` and `secret key`

* Then, run all the services with command:
```sh
docker-compose up -d
```
* The `USER` and `PASSWORD` of some services are configured in `docker-compose.yml`, Apache Airflow's password is provided in `airflow/standalone_admin_password.txt`

### 3. Streaming data to Druid
* The file `KafkaProducerEcomm.py` sent a message demo data to Kafka `Ecommerce` topic every second with fake transaction data, the structure of data message as below:
```python
{
      'id': 274992707,
       'name': 'Hộp Cơm 3 Tầng Lunch Box Kèm Muỗng Đũa Và Túi Đựng Tiện Lợi',
       'brand_name': 'PEAFLO',
       'price': 192000,
       'Origin': 'Hàn Quốc / Trung Quốc',
       'category': 'Dụng cụ chứa đựng thực phẩm',
       'original_price': 235000,
       'discount': 43000,
       'discount_rate': 18,
       'purchase_id': 'P17281500820277577',
       'quantity': 5,
       'city': 'Quảng Ninh',
       'code_city': 'VN-13',
       'create_at': '2024-10-06 00:41:22'
}
```
