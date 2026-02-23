from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class MockNeo4jClient:
    """Mock Neo4j client for testing without actual Neo4j server"""
    
    def __init__(self):
        self.data = {}
        logger.info("Using Mock Neo4j Client - no actual database connection")
    
    def close(self):
        """Mock close method"""
        pass
    
    def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict]:
        """Mock query execution"""
        logger.info(f"Mock executing query: {query[:100]}...")
        
        # Return mock results based on query type
        if "degree" in query.lower():
            return [{"degree": 42}]
        elif "suspicious" in query.lower():
            return [{"address": "0x123...", "total_tx": 150}]
        elif "path" in query.lower():
            return [{"path": ["0x123...", "0x456...", "0x789..."]}]
        else:
            return []
    
    def create_wallet_constraints(self):
        """Mock constraint creation"""
        logger.info("Mock creating wallet constraints")
    
    def create_indexes(self):
        """Mock index creation"""
        logger.info("Mock creating indexes")
    
    def ingest_transactions(self, transactions: List[Dict]):
        """Mock transaction ingestion"""
        logger.info(f"Mock ingesting {len(transactions)} transactions")
