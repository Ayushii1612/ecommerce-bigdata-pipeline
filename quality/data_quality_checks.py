import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

REQUIRED_ORDER_FIELDS    = ["order_id", "customer_id", "product_id", "amount", "order_date"]
REQUIRED_CUSTOMER_FIELDS = ["customer_id", "name", "email"]


def remove_duplicate_orders(orders):
    seen_ids = set()
    clean_orders = []
    duplicates = 0
    for order in orders:
        oid = order.get("order_id")
        if oid in seen_ids:
            duplicates += 1
            log.warning(f"Duplicate order: {oid} skipped.")
        else:
            seen_ids.add(oid)
            clean_orders.append(order)
    log.info(f"Orders: {len(orders)} total, {len(clean_orders)} unique, {duplicates} duplicates removed")
    return clean_orders


def filter_invalid_emails(customers):
    valid = []
    invalid = []
    for customer in customers:
        email = customer.get("email", "").strip()
        if EMAIL_REGEX.match(email):
            valid.append(customer)
        else:
            customer["quality_issue"] = f"INVALID_EMAIL: {email}"
            invalid.append(customer)
            log.warning(f"Invalid email for customer {customer.get('customer_id')}: {email}")
    log.info(f"Customers: {len(customers)} total, {len(valid)} valid, {len(invalid)} invalid")
    return valid, invalid


def detect_missing_values(records, required_fields, record_type="record"):
    clean = []
    issues = 0
    for record in records:
        missing = [f for f in required_fields if not record.get(f)]
        if missing:
            issues += 1
            log.warning(f"{record_type} missing fields: {missing}")
        else:
            clean.append(record)
    log.info(f"{record_type}: {len(records)} total, {len(clean)} clean, {issues} with missing values")
    return clean


def run_quality_pipeline(orders, customers):
    log.info("=" * 40)
    log.info("STARTING DATA QUALITY PIPELINE")
    log.info("=" * 40)

    orders_deduped = remove_duplicate_orders(orders)
    orders_clean   = detect_missing_values(orders_deduped, REQUIRED_ORDER_FIELDS, "Order")
    customers_valid, _ = filter_invalid_emails(customers)
    customers_clean    = detect_missing_values(customers_valid, REQUIRED_CUSTOMER_FIELDS, "Customer")

    log.info(f"DONE - Clean orders: {len(orders_clean)} | Clean customers: {len(customers_clean)}")
    return orders_clean, customers_clean


sample_orders = [
    {"order_id": "O001", "customer_id": "C1", "product_id": "P1", "amount": 99.99, "order_date": "2024-01-10"},
    {"order_id": "O001", "customer_id": "C1", "product_id": "P1", "amount": 99.99, "order_date": "2024-01-10"},
    {"order_id": "O002", "customer_id": "C2", "product_id": "P2", "amount": None,  "order_date": "2024-01-11"},
    {"order_id": "O003", "customer_id": "C3", "product_id": "P3", "amount": 45.00, "order_date": "2024-01-12"},
]

sample_customers = [
    {"customer_id": "C1", "name": "Alice",  "email": "alice@example.com"},
    {"customer_id": "C2", "name": "Bob",    "email": "not-an-email"},
    {"customer_id": "C3", "name": "",       "email": "charlie@example.com"},
    {"customer_id": "C4", "name": "Diana",  "email": "diana@shop.io"},
]

run_quality_pipeline(sample_orders, sample_customers)