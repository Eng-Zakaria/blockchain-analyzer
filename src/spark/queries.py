# # src/spark/queries.py
# def optimized_path_query(graph, source, target, max_path_length=5):
#     """Find shortest path between two wallets"""
#     return graph.bfs(
#         fromExpr=f"id = '{source}'",
#         toExpr=f"id = '{target}'",
#         maxPathLength=max_path_length
#     )


# src/spark/queries.py
from pyspark.sql import functions as F

def find_high_volume_wallets(graph, threshold=1000):
    return graph.degrees.filter(F.col("degree") > threshold)