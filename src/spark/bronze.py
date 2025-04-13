# spark/bronze.py
from pyspark.sql import SparkSession
from schemas import tx_schema

def process_bronze():
    spark = SparkSession.builder \
        .appName("BronzeETL") \
        .config("spark.sql.parquet.compression.codec", "snappy") \
        .getOrCreate()

    # Read raw JSONs
    df = spark.read.schema(tx_schema).json("data/raw/*/*.json")
    
    # Basic cleaning
    clean_df = df.filter("hash is not null") \
                .withColumn("value_eth", col("value") / 1e18) \
                .withColumn("gas_cost", col("gasUsed") * col("gasPrice") / 1e18)
    
    # Partition by date for efficient querying
    clean_df.write.partitionBy("date") \
        .mode("overwrite") \
        .parquet("etl/bronze/transactions")