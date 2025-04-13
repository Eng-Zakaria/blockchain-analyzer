# spark/gold.py
def process_gold():
    tx = spark.read.parquet("etl/silver/transactions")
    transfers = spark.read.parquet("etl/silver/token_transfers")
    
    # Top wallets by ETH volume
    tx.groupBy("from") \
      .agg(sum("value_eth").alias("total_eth")) \
      .write.parquet("etl/gold/top_wallets")
    
    # Transaction heatmap by hour
    tx.withColumn("hour", hour("block_datetime")) \
      .groupBy("hour") \
      .count() \
      .write.parquet("etl/gold/tx_heatmap")