#!/bin/bash
# ============================================================
# FILE: storage/setup_storage.sh
# PURPOSE: Setup HDFS, HBase, Redis, AsterixDB, Vertica
# ============================================================

echo "=== STEP 1: Create HDFS Zones ==="
hdfs dfs -mkdir -p /data/raw/orders
hdfs dfs -mkdir -p /data/raw/customers
hdfs dfs -mkdir -p /data/raw/products
hdfs dfs -mkdir -p /data/raw/reviews
hdfs dfs -mkdir -p /data/raw/weblogs
hdfs dfs -mkdir -p /data/raw/clickstream
hdfs dfs -mkdir -p /data/analytics/orders_orc
hdfs dfs -mkdir -p /data/analytics/customers_orc
hdfs dfs -mkdir -p /data/analytics/clickstream_orc
echo "HDFS zones created."

echo "=== STEP 2: Create HBase Tables ==="
hbase shell << EOF
create 'customer_profiles',
  {NAME => 'info',  VERSIONS => 1, COMPRESSION => 'SNAPPY'},
  {NAME => 'stats', VERSIONS => 1, COMPRESSION => 'SNAPPY'}

create 'order_index',
  {NAME => 'order', VERSIONS => 1, COMPRESSION => 'SNAPPY'}
list
EOF
echo "HBase tables created."

echo "=== STEP 3: Redis Config ==="
cat > /etc/redis/session-cache.conf << REDISCONF
port 6379
bind 0.0.0.0
maxmemory 4gb
maxmemory-policy allkeys-lru
save ""
appendonly no
REDISCONF
echo "Redis config written."

echo "=== STEP 4: AsterixDB DDL ==="
cat > storage/asterixdb_reviews.sqlpp << SQLPP
CREATE DATAVERSE ecommerce IF NOT EXISTS;
USE ecommerce;

CREATE TYPE ReviewType AS {
  review_id:   string,
  customer_id: string,
  product_id:  string,
  rating:      double,
  review_text: string,
  review_date: string,
  sentiment:   string?
};

CREATE DATASET ProductReviews(ReviewType) PRIMARY KEY review_id;
CREATE INDEX idx_product  ON ProductReviews (product_id);
CREATE INDEX idx_customer ON ProductReviews (customer_id);
SQLPP
echo "AsterixDB DDL written."

echo "=== STEP 5: Vertica Schema ==="
cat > storage/vertica_schema.sql << SQL
CREATE SCHEMA IF NOT EXISTS ecommerce;

CREATE TABLE ecommerce.fact_orders (
  order_id    BIGINT NOT NULL,
  customer_id BIGINT,
  product_id  BIGINT,
  order_date  DATE,
  amount      DECIMAL(10,2),
  status      VARCHAR(50)
) ORDER BY order_date
  SEGMENTED BY HASH(customer_id) ALL NODES;

CREATE TABLE ecommerce.dim_customers (
  customer_id BIGINT PRIMARY KEY,
  name        VARCHAR(255),
  email       VARCHAR(255),
  city        VARCHAR(100),
  signup_date DATE
);

CREATE TABLE ecommerce.dim_products (
  product_id   BIGINT PRIMARY KEY,
  product_name VARCHAR(500),
  category     VARCHAR(100),
  price        DECIMAL(10,2)
);
SQL
echo "Vertica schema written."
echo "All storage setup complete!"