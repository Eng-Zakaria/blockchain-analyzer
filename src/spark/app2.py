# # src/spark/app.py
# from pyspark.sql import SparkSession
# from graphframes import GraphFrame
# from pyspark.sql.functions import col

# def create_transaction_graph(spark, transactions_df):
#     """Convert raw transactions to graph"""
#     nodes = transactions_df.select(
#         col("from_address").alias("id"),
#         col("block_number").alias("first_seen")
#     ).union(
#         transactions_df.select(
#             col("to_address").alias("id"),
#             col("block_number").alias("first_seen")
#         )
#     ).distinct()

#     edges = transactions_df.select(
#         col("from_address").alias("src"),
#         col("to_address").alias("dst"),
#         col("value").alias("amount"),
#         col("block_number").alias("block"),
#         col("block_timestamp").alias("timestamp")
#     )

#     return GraphFrame(nodes, edges)

# if __name__ == "__main__":
#     spark = SparkSession.builder \
#         .appName("BlockchainForensics") \
#         .config("spark.jars.packages", "graphframes:graphframes:0.8.2-spark3.2-s_2.12") \
#         .getOrCreate()

#     # Load sample data (replace with live stream)
#     df = spark.read.json("data/raw/transactions/*.json")
#     graph = create_transaction_graph(spark, df)
    
#     # Run analyses
#     from src.detection import chain_hopping
#     suspicious = chain_hopping.detect(graph)
#     suspicious.show()



# # Update graph with new blocks
# def update_graph(current_graph, new_transactions):
#     new_graph = create_transaction_graph(new_transactions)
#     return GraphFrame(
#         current_graph.vertices.union(new_graph.vertices).distinct(),
#         current_graph.edges.union(new_graph.edges)
#     )



# # src/spark/app.py
# from pyspark.sql import SparkSession
# from graphframes import GraphFrame
# from config.settings import Config

# def create_spark_session():
#     return SparkSession.builder \
#         .appName("BlockchainAnalyzer") \
#         .master(Config.SPARK_MASTER) \
#         .config("spark.jars.packages", "graphframes:graphframes:0.8.2-spark3.2-s_2.12") \
#         .getOrCreate()

# def build_graph(transactions_df):
#     nodes = transactions_df.selectExpr(
#         "from_address as id", 
#         "'wallet' as label"
#     ).union(
#         transactions_df.selectExpr(
#             "to_address as id", 
#             "'wallet' as label"
#         )
#     ).distinct()
    
#     edges = transactions_df.selectExpr(
#         "from_address as src",
#         "to_address as dst",
#         "value as amount",
#         "block_number as block"
#     )
    
#     return GraphFrame(nodes, edges)

