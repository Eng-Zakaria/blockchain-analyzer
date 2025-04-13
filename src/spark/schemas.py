from pyspark.sql.types import *

tx_schema = StructType([
    StructField("hash", StringType()),
    StructField("blockNumber", LongType()),
    StructField("from", StringType()),
    StructField("to", StringType()),
    StructField("value", StringType()),  # Preserve precision
    StructField("gasUsed", LongType()),
    StructField("gasPrice", LongType()),
    StructField("input", StringType()),
    StructField("receipt", StructType([
        StructField("status", IntegerType()),
        StructField("logs", ArrayType(StringType()))
    ])),
    StructField("block_datetime", TimestampType())
])