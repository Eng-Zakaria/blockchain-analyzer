# from pyspark.sql import functions as F
# from config.settings import SUSPICIOUS_THRESHOLDS

# def detect_smurfing(transactions_df):
#     """Identify many small transactions below thresholds"""
#     pass


# src/detection/smurfing.py
from pyspark.sql import functions as F

def detect(transactions_df, count_threshold=50, amount_threshold=1):
    return transactions_df.groupBy("from_address").agg(
        F.count("*").alias("tx_count"),
        F.sum("value").alias("total_amount")
    ).filter(
        (F.col("tx_count") > count_threshold) & 
        (F.col("total_amount") < amount_threshold)
    )