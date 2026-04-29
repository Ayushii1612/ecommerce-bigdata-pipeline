import os
import csv
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

# Local folder instead of HDFS (no Hadoop needed)
LOCAL_RAW_ZONE = "data/raw"


# ============================================================
# STEP 1: Simulate uploading to local raw zone
# ============================================================
def upload_to_local(local_path: str, dest_path: str):
    """Copy file to local raw zone (simulates HDFS upload)."""
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Read source and write to destination
    with open(local_path, "r", encoding="utf-8") as f:
        content = f.read()
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)

    log.info(f"Uploaded {local_path} -> {dest_path}")


# ============================================================
# STEP 2: Convert reviews CSV to JSON (NDJSON format)
# ============================================================
def csv_to_json_reviews(csv_path: str, json_output: str):
    """Convert product reviews CSV to JSON format."""
    reviews = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            review = {
                "review_id":   row["review_id"],
                "customer_id": row["customer_id"],
                "product_id":  row["product_id"],
                "rating":      float(row["rating"]),
                "review_text": row["review_text"],
                "review_date": row["review_date"],
                "sentiment":   None
            }
            reviews.append(review)

    os.makedirs(os.path.dirname(json_output), exist_ok=True)
    with open(json_output, "w", encoding="utf-8") as f:
        for r in reviews:
            f.write(json.dumps(r) + "\n")

    log.info(f"Converted {len(reviews)} reviews to JSON -> {json_output}")
    return reviews


# ============================================================
# STEP 3: Generate HBase load script from customers CSV
# ============================================================
def generate_hbase_script(csv_path: str, script_output: str):
    """Generate HBase shell commands from customers CSV."""
    lines = ["# HBase bulk load script", "# Run with: hbase shell < load_customers.sh", ""]

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = row["customer_id"]
            lines.append(f"put 'customer_profiles', '{cid}', 'info:name', '{row['name']}'")
            lines.append(f"put 'customer_profiles', '{cid}', 'info:email', '{row['email']}'")
            lines.append(f"put 'customer_profiles', '{cid}', 'info:city', '{row.get('city', '')}'")

    os.makedirs(os.path.dirname(script_output), exist_ok=True)
    with open(script_output, "w") as f:
        f.write("\n".join(lines))

    log.info(f"HBase script generated -> {script_output}")


# ============================================================
# CREATE SAMPLE DATA FILES (so we can test without real data)
# ============================================================
def create_sample_data():
    """Create sample CSV files for testing."""
    os.makedirs("data", exist_ok=True)

    # Sample reviews CSV
    reviews_data = """review_id,customer_id,product_id,rating,review_text,review_date
R001,C001,P001,5.0,Amazing headphones great sound quality,2024-01-10
R002,C002,P002,4.0,Good running shoes very comfortable,2024-01-11
R003,C003,P003,3.5,Decent water bottle but lid leaks,2024-01-12
R004,C004,P001,4.5,Excellent noise cancellation worth the price,2024-01-13
R005,C005,P004,5.0,Best bluetooth speaker I have ever owned,2024-01-14"""

    with open("data/reviews.csv", "w") as f:
        f.write(reviews_data)
    log.info("Sample reviews.csv created.")

    # Sample customers CSV
    customers_data = """customer_id,name,email,city,signup_date
C001,Alice Johnson,alice@example.com,Mumbai,2023-01-15
C002,Bob Smith,bob@example.com,Delhi,2023-02-20
C003,Charlie Brown,charlie@example.com,Bangalore,2023-03-10
C004,Diana Prince,diana@example.com,Chennai,2023-04-05
C005,Evan Peters,evan@example.com,Hyderabad,2023-05-18"""

    with open("data/customers.csv", "w") as f:
        f.write(customers_data)
    log.info("Sample customers.csv created.")


# ============================================================
# MAIN PIPELINE
# ============================================================
if __name__ == "__main__":

    log.info("=" * 50)
    log.info("STARTING CSV BULK IMPORT PIPELINE")
    log.info("=" * 50)

    # Create sample data
    create_sample_data()

    # Import reviews
    upload_to_local(
        local_path="data/reviews.csv",
        dest_path=f"{LOCAL_RAW_ZONE}/reviews/reviews.csv"
    )
    csv_to_json_reviews(
        csv_path="data/reviews.csv",
        json_output="data/processed/reviews.ndjson"
    )

    # Import customers
    upload_to_local(
        local_path="data/customers.csv",
        dest_path=f"{LOCAL_RAW_ZONE}/customers/customers.csv"
    )
    generate_hbase_script(
        csv_path="data/customers.csv",
        script_output="data/processed/load_customers_hbase.sh"
    )

    log.info("=" * 50)
    log.info("ALL CSV IMPORTS COMPLETED SUCCESSFULLY!")
    log.info("=" * 50)

    # Show what was created
    print("\nFiles created:")
    for root, dirs, files in os.walk("data"):
        for file in files:
            filepath = os.path.join(root, file)
            size = os.path.getsize(filepath)
            print(f"  {filepath}  ({size} bytes)")