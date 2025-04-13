# spark/silver.py
from pyspark.sql.functions import *

def process_silver():
    df = spark.read.parquet("etl/bronze/transactions")
    
    # Extract token transfers from logs
    token_transfers = df.select(
        "hash",
        explode("receipt.logs").alias("log")
    ).filter(col("log").contains("0xddf252ad"))  # ERC20 transfer signature
    
    # Write enriched data
    token_transfers.write.parquet("etl/silver/token_transfers")
    df.write.parquet("etl/silver/transactions")