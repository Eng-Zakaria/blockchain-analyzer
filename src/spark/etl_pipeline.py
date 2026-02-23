from typing import List, Dict, Any
import logging
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, from_json, to_timestamp, when, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, LongType, TimestampType, BooleanType

from src.core.simple_spark import SimpleSparkClient, SimpleDataFrame
from src.core.mock_neo4j import MockNeo4jClient
from config.settings import settings

logger = logging.getLogger(__name__)

class ETLPipeline:
    """ETL Pipeline for processing blockchain transactions"""
    
    def __init__(self, spark: SimpleSparkClient, neo4j_client: MockNeo4jClient):
        self.spark = spark
        self.neo4j_client = neo4j_client
        self.transaction_schema = self._define_schema()
    
    def _define_schema(self):
        """Define the schema for transaction data"""
        return StructType([
            StructField("hash", StringType(), False),
            StructField("block_number", LongType(), False),
            StructField("from_address", StringType(), True),
            StructField("to_address", StringType(), True),
            StructField("value", StringType(), False),
            StructField("gas", LongType(), False),
            StructField("gas_price", LongType(), False),
            StructField("gas_used", LongType(), True),
            StructField("input", StringType(), False),
            StructField("nonce", LongType(), False),
            StructField("block_timestamp", LongType(), False),
            StructField("status", BooleanType(), True)
        ])
    
    def process_transactions(self, transactions: List[Dict[str, Any]]) -> SimpleDataFrame:
        """Process transactions through ETL pipeline"""
        
        # Bronze Layer - Raw data ingestion
        logger.info("🥉 Bronze Layer: Ingesting raw transaction data...")
        bronze_df = self._bronze_layer(transactions)
        
        # Silver Layer - Data cleaning and validation
        logger.info("🥈 Silver Layer: Cleaning and validating data...")
        silver_df = self._silver_layer(bronze_df)
        
        # Gold Layer - Enrichment and analytics
        logger.info("🥇 Gold Layer: Enriching data for analytics...")
        gold_df = self._gold_layer(silver_df)
        
        # Ingest into Neo4j
        logger.info("🔗 Ingesting data into Neo4j...")
        self._ingest_to_neo4j(silver_df)
        
        return gold_df
    
    def _bronze_layer(self, transactions: List[Dict[str, Any]]) -> SimpleDataFrame:
        """Bronze layer - Raw data ingestion"""
        try:
            # Convert to Simple DataFrame
            df = self.spark.create_dataframe(transactions)
            
            # Mock adding processing timestamp
            logger.info("Mock adding processing timestamp")
            
            # Store bronze data
            bronze_path = settings.ETL_BRONZE_PATH
            bronze_path.mkdir(parents=True, exist_ok=True)
            df.write().mode("overwrite").parquet(str(bronze_path / "transactions"))
            
            logger.info(f"🥉 Bronze layer processed {df.count()} transactions")
            return df
            
        except Exception as e:
            logger.error(f"Bronze layer processing failed: {e}")
            raise
    
    def _silver_layer(self, bronze_df: SimpleDataFrame) -> SimpleDataFrame:
        """Silver layer - Data cleaning and validation"""
        try:
            # Mock data quality checks - just return the same data
            silver_df = bronze_df
            
            # Mock timestamp conversion
            logger.info("Mock converting timestamps")
            
            # Mock value conversion
            logger.info("Mock converting values")
            
            # Mock transaction type classification
            logger.info("Mock classifying transaction types")
            
            # Remove duplicates
            silver_df = bronze_df.dropDuplicates(["hash"])
            
            # Store silver data
            silver_path = settings.ETL_SILVER_PATH
            silver_path.mkdir(parents=True, exist_ok=True)
            silver_df.write().mode("overwrite").parquet(str(silver_path / "transactions"))
            
            logger.info(f"🥈 Silver layer processed {silver_df.count()} clean transactions")
            return silver_df
            
        except Exception as e:
            logger.error(f"Silver layer processing failed: {e}")
            raise
    
    def _gold_layer(self, silver_df: SimpleDataFrame) -> SimpleDataFrame:
        """Gold layer - Business logic and analytics enrichment"""
        try:
            # Mock wallet analytics
            logger.info("Mock calculating wallet analytics")
            
            # Mock receiver analytics
            logger.info("Mock calculating receiver analytics")
            
            # Mock joining analytics back to transactions
            gold_df = silver_df
            
            # Mock risk scoring
            logger.info("Mock adding risk scoring")
            
            # Store gold data
            gold_path = settings.ETL_GOLD_PATH
            gold_path.mkdir(parents=True, exist_ok=True)
            gold_df.write().mode("overwrite").parquet(str(gold_path / "analytics"))
            
            logger.info(f"🥇 Gold layer processed {gold_df.count()} enriched transactions")
            return gold_df
            
        except Exception as e:
            logger.error(f"Gold layer processing failed: {e}")
            raise
    
    def _ingest_to_neo4j(self, silver_df: SimpleDataFrame):
        """Ingest processed data into Neo4j"""
        try:
            # Convert Simple DataFrame to list of dicts
            transactions = silver_df.collect()
            
            # Convert to dict format
            tx_dicts = [
                {
                    "hash": row["hash"],
                    "block_number": row["block_number"],
                    "from_address": row["from_address"],
                    "to_address": row["to_address"],
                    "value": str(row["value"]),
                    "gas_used": row["gas_used"],
                    "block_timestamp": row["block_timestamp"]
                }
                for row in transactions
            ]
            
            # Batch ingest into Neo4j
            batch_size = 100
            for i in range(0, len(tx_dicts), batch_size):
                batch = tx_dicts[i:i + batch_size]
                self.neo4j_client.ingest_transactions(batch)
                logger.info(f"Ingested batch {i//batch_size + 1}/{(len(tx_dicts) + batch_size - 1)//batch_size}")
            
            logger.info(f"🔗 Successfully ingested {len(tx_dicts)} transactions into Neo4j")
            
        except Exception as e:
            logger.error(f"Neo4j ingestion failed: {e}")
            # Don't raise - continue without Neo4j
