from pyspark.sql import SparkSession
from config.settings import settings

def create_spark_session(app_name: str = "BlockchainAnalyzer") -> SparkSession:
    """Create and configure Spark session without GraphFrames"""
    
    spark = SparkSession.builder \
        .appName(app_name) \
        .master(settings.SPARK_MASTER) \
        .config("spark.sql.shuffle.partitions", "200") \
        .config("spark.executor.memory", "4g") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.cores", "2") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    # Set log level
    spark.sparkContext.setLogLevel("WARN")
    
    return spark
