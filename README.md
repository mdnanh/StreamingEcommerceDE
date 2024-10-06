# StreamingEcommerceDE

## Description
This project focuses on building a real-time e-commerce data streaming pipeline using [Apache Kafka](https://kafka.apache.org/quickstart), [Apache Druid](https://github.com/apache/druid), and [MinIO](https://github.com/minio/minio), all deployed via [Docker](https://docs.docker.com/). The system captures real-time data streams from an e-commerce platform, stores and processes metadata in Druid for fast querying and analysis, while using MinIO as deep storage for long-term data retention. Apache Superset is used to visualize the data, providing real-time insights and dashboards for better decision-making. This setup ensures scalability, performance, and efficiency in handling and analyzing large volumes of streaming data.
## Architecture
![alt text](https://github.com/mdnanh/StreamingEcommerceDE/blob/main/images/architecture.png)

## Init
### 1 Installation
This project is built with docker compose, so make sure you have docker and docker-compose installed. Follow the steps instructed in [Docker](https://docs.docker.com/get-started/get-docker/) to install it. 
Then, pull this repo and start the journey.

### 2 Start services
```sh
cd StreamingEcommerceDE
```
