# # src/detection/chain_hopping.py
# from graphframes import GraphFrame
# from pyspark.sql.functions import desc

# def detect(graph, degree_threshold=1000, time_window="1 hour"):
#     """Find wallets with abnormal transaction frequency"""
#     return graph.degrees.filter(f"degree > {degree_threshold}") \
#         .join(graph.vertices, "id") \
#         .orderBy(desc("degree"))


# src/detection/chain_hopping.py
from graphframes import GraphFrame

def detect(graph, threshold=10):
    """Find wallets with rapid multi-hop transactions"""
    return graph.find("(a)-[e1]->(b); (b)-[e2]->(c)") \
        .filter("e1.timestamp < e2.timestamp") \
        .groupBy("a.id") \
        .count() \
        .filter(f"count > {threshold}")