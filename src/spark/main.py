# spark/main.py
from pyspark.sql import SparkSession

def run_pipeline():
    spark = SparkSession.builder \
        .appName("BlockchainETL") \
        .config("spark.sql.shuffle.partitions", "200") \
        .getOrCreate()
    
    # Bronze
    bronze_df = spark.read.json("data/raw/*/*.json")
    bronze_df.write.parquet("etl/bronze/transactions")
    
    # Silver 
    silver_df = spark.read.parquet("etl/bronze/transactions")
    silver_df.write.parquet("etl/silver/transactions")
    
    # Gold
    gold_df = spark.read.parquet("etl/silver/transactions")
    gold_df.write.parquet("etl/gold/analytics")

if __name__ == "__main__":
    run_pipeline()