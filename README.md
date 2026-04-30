# E-Commerce Big Data Pipeline

This project is a complete end-to-end Big Data Pipeline inspired by how large-scale e-commerce platforms like Amazon handle massive, high-velocity data. Traditional systems like MySQL are not designed to efficiently process the volume, variety, and real-time nature of such data, so this project builds a scalable, distributed, and fault-tolerant architecture using the Hadoop ecosystem.

The pipeline ingests structured data from MySQL using Sqoop, real-time logs and clickstream events via Flume, and bulk CSV datasets through Python scripts. All incoming data is stored in an HDFS-based data lake, organized into raw and ORC-formatted analytics zones to support efficient querying and storage optimization.

Batch processing is performed using Apache Hive, generating insights such as customer behavior analysis, revenue trends, sales reports, and product recommendation datasets. For real-time analytics, Apache Spark Structured Streaming processes clickstream data to compute live session metrics, user activity patterns, and engagement statistics.

To ensure reliability, the system includes automated data quality checks that remove duplicates, validate formats (such as emails), and handle missing values. A Python-based fraud detection engine evaluates every transaction using multiple rule-based signals (e.g., abnormal order value, rapid repeat purchases, suspicious locations) and assigns a risk score from 0–100 to flag potentially fraudulent orders in real time.

The architecture also integrates Apache Solr for fast full-text product search with filtering capabilities, Redis for real-time session caching, and HBase for low-latency access to customer profiles and transaction history. The entire pipeline is built using Python, HiveQL, and Bash scripts on an Ubuntu (WSL) environment, demonstrating polyglot storage, distributed computing, and real-time + batch (Lambda-style) processing.

Overall, this project simulates a production-grade data engineering system capable of handling millions of records efficiently, making it ideal for learning and demonstrating scalable data pipelines, big data tools integration, and real-world analytics workflows.

# Features
1. Multi-source Data Ingestion — Sqoop for MySQL, Flume for logs and clickstream, Python for CSV bulk import
2. Distributed Data Lake — HDFS with raw zone and ORC analytics zone for efficient storage
3. Automated Data Quality — Duplicate removal, invalid email filtering, and missing value detection
4. Real-time Fraud Detection — Rule-based risk scoring (LOW / MEDIUM / HIGH) for every order
5. Batch Analytics — Hive jobs for customer behavior, RFM analysis, and daily revenue reports
6. Stream Processing — Spark Structured Streaming for real-time clickstream and session analytics
7. Product Search Engine — Apache Solr indexing with full-text search and category/price filters
8. Session Caching — Redis for real-time active session storage with auto-expiry
9. Customer Profiles — HBase for low-latency customer profile lookups

# Tech Stack
1. Languages — Python 3, HiveQL, Bash Shell Script
2. Ingestion — Apache Sqoop 1.4.x, Apache Flume 1.11.0
3. Storage — Apache Hadoop HDFS 3.3.6, Apache HBase, Redis, AsterixDB, Vertica
4. Processing — Apache Hive 3.1.3, Apache Spark 3.5.1
5. Analytics — Apache Solr 9.x
6. Operating System — Ubuntu 24.04 (WSL2 on Windows)
7. Java — OpenJDK 8
8. IDE — Visual Studio Code

# Project Structure
```
ecommerce-bigdata-pipeline/
│
├── ingestion/
│   ├── sqoop/
│   │   └── import_orders.sh          ← MySQL to HDFS batch import
│   ├── flume/
│   │   ├── weblog_flume.conf         ← Web server logs to HDFS
│   │   └── clickstream_flume.conf    ← Kafka clickstream to HDFS
│   └── csv/
│       └── bulk_csv_import.py        ← CSV bulk import to HDFS
│
├── storage/
│   └── setup_storage.sh              ← HDFS zones, HBase, Redis setup
│
├── processing/
│   ├── batch/
│   │   └── hive_batch_jobs.hql       ← Hive analytics batch jobs
│   └── streaming/
│       └── clickstream_streaming.py  ← Spark real-time processing
│
├── analytics/
│   ├── fraud_detection.py            ← Rule-based fraud scoring
│   └── solr_search_indexing.py       ← Product search indexing
│
├── quality/
│   └── data_quality_checks.py        ← Data cleaning and validation
│
├── data/
│   ├── raw/                          ← Raw ingested CSV files
│   └── processed/                    ← Cleaned and converted files
│
└── run_pipeline.sh                   ← Master pipeline runner
```

# Conclusion
This project successfully demonstrates a production-grade Big Data Pipeline that solves the core challenges of modern e-commerce data management. By combining batch and real-time processing, automated data quality enforcement, fraud detection, and fast product search into one unified system, it replicates the kind of data infrastructure used by large-scale platforms like Amazon. The pipeline is fully functional on a local Ubuntu environment and is ready to be deployed on cloud platforms like AWS EMR or Google Dataproc for production-scale workloads.
