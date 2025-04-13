# # src/visualization/neo4j_loader.py
# from pyspark.sql import SparkSession
# from config import settings

# def load_graph(graph):
#     (graph.vertices.write.format("org.neo4j.spark.DataSource")
#         .option("url", settings.NEO4J_URI)
#         .option("authentication.type", "basic")
#         .option("authentication.basic.username", settings.NEO4J_USER)
#         .option("authentication.basic.password", settings.NEO4J_PASSWORD)
#         .option("labels", "Wallet")
#         .save())

#     (graph.edges.write.format("org.neo4j.spark.DataSource")
#         .option("url", settings.NEO4J_URI)
#         .option("relationship", "SENT")
#         .option("relationship.source.labels", "Wallet")
#         .option("relationship.target.labels", "Wallet")
#         .save())
    


# src/visualization/neo4j_loader.py
from pyspark.sql import SparkSession
from config.settings import Config

def load_graph(graph):
    (graph.vertices.write.format("org.neo4j.spark.DataSource")
        .option("url", Config.NEO4J_URI)
        .option("labels", ":Wallet")
        .save())
    
    (graph.edges.write.format("org.neo4j.spark.DataSource")
        .option("relationship", "SENT")
        .save())