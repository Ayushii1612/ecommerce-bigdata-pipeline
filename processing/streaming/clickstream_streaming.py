from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import count

spark = SparkSession.builder \
    .appName("EcommerceClickstreamProcessing") \
    .master("local[2]") \
    .config("spark.python.worker.reuse", "false") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

schema = StructType([
    StructField("event_id",    StringType(), True),
    StructField("session_id",  StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("page",        StringType(), True),
    StructField("action",      StringType(), True),
])

data = [
    ("E001", "S001", "C001", "/product/P001", "view"),
    ("E002", "S001", "C001", "/product/P002", "view"),
    ("E003", "S001", "C001", "/cart",         "add"),
    ("E004", "S002", "C002", "/product/P001", "view"),
    ("E005", "S002", "C002", "/checkout",     "purchase"),
    ("E006", "S003", "C003", "/product/P003", "view"),
    ("E007", "S003", "C003", "/product/P003", "view"),
    ("E008", "S004", "C004", "/product/P004", "view"),
    ("E009", "S004", "C004", "/cart",         "add"),
    ("E010", "S004", "C004", "/checkout",     "purchase"),
]

df = spark.createDataFrame(data, schema)

print("\n==== CLICKSTREAM DATA ====")
df.show()

print("\n==== SESSION STATISTICS ====")
df.groupBy("session_id", "customer_id") \
  .agg(count("event_id").alias("total_clicks")) \
  .show()

print("\n==== ACTION SUMMARY ====")
df.groupBy("action").count().orderBy("count", ascending=False).show()

print("\n==== TOP PAGES ====")
df.groupBy("page").count().orderBy("count", ascending=False).show()

print("Clickstream processing completed successfully!")
spark.stop()
