# src/detection/scoring.py
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans

def cluster_suspicious_wallets(wallet_features):
    assembler = VectorAssembler(
        inputCols=["degree", "avg_amount", "tx_frequency"],
        outputCol="features")
    kmeans = KMeans(k=3, seed=42)
    model = kmeans.fit(assembler.transform(wallet_features))
    return model.transform(wallet_features)