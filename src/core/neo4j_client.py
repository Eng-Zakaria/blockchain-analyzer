from neo4j import GraphDatabase
from config.settings import settings
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class Neo4jClient:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
    
    def close(self):
        self.driver.close()
    
    def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict]:
        """Execute a Cypher query and return results"""
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]
    
    def create_wallet_constraints(self):
        """Create uniqueness constraints for wallet addresses"""
        constraints = [
            "CREATE CONSTRAINT wallet_address_unique IF NOT EXISTS FOR (w:Wallet) REQUIRE w.address IS UNIQUE",
            "CREATE CONSTRAINT tx_hash_unique IF NOT EXISTS FOR (t:Transaction) REQUIRE t.hash IS UNIQUE"
        ]
        
        for constraint in constraints:
            try:
                self.execute_query(constraint)
                logger.info(f"Created constraint: {constraint}")
            except Exception as e:
                logger.warning(f"Constraint creation failed: {e}")
    
    def create_indexes(self):
        """Create performance indexes"""
        indexes = [
            "CREATE INDEX wallet_block_index IF NOT EXISTS FOR (w:Wallet) ON (w.first_block)",
            "CREATE INDEX tx_block_index IF NOT EXISTS FOR ()-[r:SENT]->() ON (r.block_number)",
            "CREATE INDEX tx_value_index IF NOT EXISTS FOR ()-[r:SENT]->() ON (r.value)"
        ]
        
        for index in indexes:
            try:
                self.execute_query(index)
                logger.info(f"Created index: {index}")
            except Exception as e:
                logger.warning(f"Index creation failed: {e}")
    
    def ingest_transactions(self, transactions: List[Dict]):
        """Batch ingest transactions into Neo4j"""
        query = """
        UNWIND $transactions AS tx
        MERGE (sender:Wallet {address: tx.from_address})
        ON CREATE SET sender.first_block = tx.block_number, sender.tx_count = 1
        ON MATCH SET sender.tx_count = coalesce(sender.tx_count, 0) + 1
        
        MERGE (receiver:Wallet {address: tx.to_address})
        ON CREATE SET receiver.first_block = tx.block_number, receiver.tx_count = 1
        ON MATCH SET receiver.tx_count = coalesce(receiver.tx_count, 0) + 1
        
        MERGE (t:Transaction {hash: tx.hash})
        SET t.block_number = tx.block_number, 
            t.value = tx.value,
            t.gas_used = tx.gas_used,
            t.timestamp = tx.block_timestamp
        
        MERGE (sender)-[r:SENT]->(t)
        SET r.block_number = tx.block_number, r.value = tx.value
        
        MERGE (t)-[r2:RECEIVED]->(receiver)
        SET r2.block_number = tx.block_number, r2.value = tx.value
        """
        
        try:
            self.execute_query(query, {"transactions": transactions})
            logger.info(f"Ingested {len(transactions)} transactions")
        except Exception as e:
            logger.error(f"Transaction ingestion failed: {e}")
