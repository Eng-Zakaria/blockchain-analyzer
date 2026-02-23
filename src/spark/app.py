from pyspark.sql import SparkSession
from src.core.spark_session import create_spark_session

def create_spark_app():
    """Main Spark application entry point"""
    spark = create_spark_session("BlockchainETL")
    return spark