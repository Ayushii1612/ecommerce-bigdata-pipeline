import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

# Simple in-memory store instead of Solr (no installation needed)
product_index = []


def index_products(products: list):
    """Store products in memory index."""
    for product in products:
        product_index.append(product)
    log.info(f"Indexed {len(products)} products successfully.")


def search_products(query: str, category: str = None, max_price: float = None):
    """
    Search products by name or description.
    Optionally filter by category and max price.
    """
    results = []
    query_lower = query.lower()

    for product in product_index:
        # Check name or description match
        name_match = query_lower in product["product_name"].lower()
        desc_match = query_lower in product["description"].lower()

        if not (name_match or desc_match):
            continue

        # Apply category filter
        if category and product["category"] != category:
            continue

        # Apply price filter
        if max_price and product["price"] > max_price:
            continue

        results.append(product)

    log.info(f"Search '{query}': {len(results)} results found.")
    return results


# Sample products
sample_products = [
    {
        "product_id":   "P001",
        "product_name": "Wireless Bluetooth Headphones",
        "category":     "Electronics",
        "description":  "High-quality noise-cancelling headphones with 30hr battery",
        "price":        79.99,
        "avg_rating":   4.5,
        "review_count": 1200,
        "in_stock":     True
    },
    {
        "product_id":   "P002",
        "product_name": "Running Shoes Ultra Boost",
        "category":     "Sports",
        "description":  "Lightweight breathable running shoes for marathon training",
        "price":        129.99,
        "avg_rating":   4.7,
        "review_count": 850,
        "in_stock":     True
    },
    {
        "product_id":   "P003",
        "product_name": "Stainless Steel Water Bottle",
        "category":     "Kitchen",
        "description":  "Insulated 32oz bottle keeps drinks cold for 24 hours",
        "price":        24.99,
        "avg_rating":   4.3,
        "review_count": 3200,
        "in_stock":     False
    },
    {
        "product_id":   "P004",
        "product_name": "Bluetooth Speaker Portable",
        "category":     "Electronics",
        "description":  "Waterproof portable speaker with 360 degree sound",
        "price":        49.99,
        "avg_rating":   4.4,
        "review_count": 980,
        "in_stock":     True
    },
]

# Index all products
index_products(sample_products)

print("\n" + "="*50)
print("TEST 1: Search 'bluetooth'")
print("="*50)
results = search_products("bluetooth")
for r in results:
    print(f"  - {r['product_name']} | ${r['price']} | Rating: {r['avg_rating']}")

print("\n" + "="*50)
print("TEST 2: Search 'headphones' in Electronics")
print("="*50)
results = search_products("headphones", category="Electronics")
for r in results:
    print(f"  - {r['product_name']} | ${r['price']} | In Stock: {r['in_stock']}")

print("\n" + "="*50)
print("TEST 3: Search 'running' with max price $100")
print("="*50)
results = search_products("running", max_price=100.0)
for r in results:
    print(f"  - {r['product_name']} | ${r['price']}")

print("\n" + "="*50)
print("TEST 4: Search 'bottle' in Kitchen")
print("="*50)
results = search_products("bottle", category="Kitchen")
for r in results:
    print(f"  - {r['product_name']} | Rating: {r['avg_rating']} | Reviews: {r['review_count']}")