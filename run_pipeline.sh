#!/bin/bash
# ============================================================
# FILE: run_pipeline.sh
# PURPOSE: Master script - runs the full batch pipeline
# ============================================================

echo "========================================"
echo "  E-COMMERCE BIG DATA PIPELINE RUNNER"
echo "========================================"

echo "[1/5] Setting up storage..."
bash storage/setup_storage.sh

echo "[2/5] Running Sqoop ingestion..."
bash ingestion/sqoop/import_orders.sh

echo "[3/5] Running CSV bulk import..."
python3 ingestion/csv/bulk_csv_import.py

echo "[4/5] Running data quality checks..."
python3 quality/data_quality_checks.py

echo "[5/5] Running Hive batch jobs..."
hive -f processing/batch/hive_batch_jobs.hql

echo "========================================"
echo "  PIPELINE COMPLETE!"
echo "========================================"
echo ""
echo "For streaming, run separately:"
echo "  flume-ng agent --conf-file ingestion/flume/weblog_flume.conf --name weblog_agent"
echo "  flume-ng agent --conf-file ingestion/flume/clickstream_flume.conf --name clickstream_agent"
echo "  spark-submit processing/streaming/clickstream_streaming.py"
echo "  python3 analytics/fraud_detection.py"
echo "  python3 analytics/solr_search_indexing.py"