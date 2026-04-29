#!/bin/bash
# ============================================================
# FILE: ingestion/sqoop/import_orders.sh
# PURPOSE: Import Orders, Customers, Products from MySQL to HDFS
# ============================================================

MYSQL_HOST="localhost"
MYSQL_DB="ecommerce"
MYSQL_USER="root"
MYSQL_PASS="password"
HDFS_RAW_ZONE="/data/raw"

echo ">>> Importing Orders..."
sqoop import \
  --connect jdbc:mysql://${MYSQL_HOST}/${MYSQL_DB} \
  --username ${MYSQL_USER} \
  --password ${MYSQL_PASS} \
  --table orders \
  --target-dir ${HDFS_RAW_ZONE}/orders \
  --as-orcfile \
  --num-mappers 4 \
  --incremental lastmodified \
  --check-column updated_at \
  --last-value "2024-01-01 00:00:00" \
  --delete-target-dir

echo ">>> Importing Customers..."
sqoop import \
  --connect jdbc:mysql://${MYSQL_HOST}/${MYSQL_DB} \
  --username ${MYSQL_USER} \
  --password ${MYSQL_PASS} \
  --table customers \
  --target-dir ${HDFS_RAW_ZONE}/customers \
  --as-orcfile \
  --num-mappers 4 \
  --split-by customer_id

echo ">>> Importing Products..."
sqoop import \
  --connect jdbc:mysql://${MYSQL_HOST}/${MYSQL_DB} \
  --username ${MYSQL_USER} \
  --password ${MYSQL_PASS} \
  --table products \
  --target-dir ${HDFS_RAW_ZONE}/products \
  --as-orcfile \
  --num-mappers 2

echo ">>> All Sqoop imports completed!"