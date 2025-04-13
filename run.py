from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
# Read silver transactions
tx_df = spark.read.parquet("etl/silver/transactions")
# 1.1 Schema verification
tx_df.printSchema()
# Verify all expected columns exist (block_number, from_address, value, etc.)

# 1.2 Null check for critical fields
from pyspark.sql.functions import col, count, when

null_check = tx_df.select(
    count(when(col("block_number").isNull(), "block_number")).alias("null_blocks"),
    count(when(col("from_address").isNull(), "from_address")).alias("null_senders"),
    count(when(col("value").isNull(), "value")).alias("null_values")
).show()

# 1.3 Duplicate transactions
dup_count = tx_df.groupBy("transaction_hash").count().filter("count > 1").count()
print(f"Duplicate transactions: {dup_count}")

