import logging
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from config.settings import settings

logger = logging.getLogger(__name__)

class ElasticsearchClient:
    """Elasticsearch client for indexing blockchain data"""
    
    def __init__(self):
        self.host = getattr(settings, 'ELASTICSEARCH_HOST', 'localhost')
        self.port = getattr(settings, 'ELASTICSEARCH_PORT', 9200)
        self.index_name = "blockchain-transactions"
        
        # Mock implementation - replace with real elasticsearch-py when available
        logger.info("Using Mock Elasticsearch Client")
        self.mock_data = []
    
    def create_index(self, mappings: Dict[str, Any]) -> bool:
        """Create Elasticsearch index with mappings"""
        try:
            logger.info(f"📝 Creating index: {self.index_name}")
            logger.info(f"📋 Index mappings: {json.dumps(mappings, indent=2)}")
            
            # Mock implementation
            logger.info("✅ Index created successfully (mock)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create index: {e}")
            return False
    
    def index_transactions(self, transactions: List[Dict[str, Any]]) -> bool:
        """Index transactions into Elasticsearch"""
        try:
            logger.info(f"📊 Indexing {len(transactions)} transactions...")
            
            indexed_count = 0
            for tx in transactions:
                # Prepare document for Elasticsearch
                doc = self._prepare_document(tx)
                
                # Mock indexing
                self.mock_data.append(doc)
                indexed_count += 1
                
                if indexed_count % 100 == 0:
                    logger.info(f"📝 Indexed {indexed_count} transactions...")
            
            logger.info(f"✅ Successfully indexed {indexed_count} transactions")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to index transactions: {e}")
            return False
    
    def _prepare_document(self, tx: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare transaction document for Elasticsearch"""
        doc = {
            "hash": tx.get("hash", ""),
            "block_number": tx.get("block_number", 0),
            "from_address": tx.get("from_address", ""),
            "to_address": tx.get("to_address", ""),
            "value": self._parse_value(tx.get("value", "0")),
            "gas": tx.get("gas", 0),
            "gas_price": tx.get("gas_price", 0),
            "gas_used": tx.get("gas_used", 0),
            "input": tx.get("input", "0x"),
            "nonce": tx.get("nonce", 0),
            "block_timestamp": self._parse_timestamp(tx.get("block_timestamp", 0)),
            "status": tx.get("status", True),
            "processed_at": datetime.utcnow().isoformat()
        }
        
        # Add computed fields
        doc["value_eth"] = doc["value"] / 10**18
        doc["tx_type"] = self._classify_transaction(tx)
        doc["risk_score"] = self._calculate_risk_score(doc)
        
        return doc
    
    def _parse_value(self, value_str: str) -> float:
        """Parse hex value string to float"""
        try:
            if isinstance(value_str, str) and value_str.startswith("0x"):
                return float(int(value_str, 16))
            return float(value_str)
        except:
            return 0.0
    
    def _parse_timestamp(self, timestamp: int) -> str:
        """Parse timestamp to ISO format"""
        try:
            return datetime.fromtimestamp(timestamp).isoformat()
        except:
            return datetime.utcnow().isoformat()
    
    def _classify_transaction(self, tx: Dict[str, Any]) -> str:
        """Classify transaction type"""
        if not tx.get("to_address"):
            return "contract_creation"
        elif tx.get("input", "0x") != "0x":
            return "contract_interaction"
        else:
            return "simple_transfer"
    
    def _calculate_risk_score(self, doc: Dict[str, Any]) -> int:
        """Calculate risk score for transaction"""
        score = 0
        
        # High value transactions
        if doc["value_eth"] > 100:
            score += 3
        elif doc["value_eth"] > 10:
            score += 2
        elif doc["value_eth"] > 1:
            score += 1
        
        # Contract interactions
        if doc["tx_type"] == "contract_interaction":
            score += 1
        
        # High gas usage
        if doc["gas_used"] > 200000:
            score += 1
        
        return min(score, 5)  # Cap at 5
    
    def search_transactions(self, query: Dict[str, Any], size: int = 100) -> List[Dict[str, Any]]:
        """Search transactions with query"""
        try:
            logger.info(f"🔍 Searching transactions with query: {query}")
            
            # Mock search implementation
            results = self.mock_data[:size]
            logger.info(f"📊 Found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []
    
    def get_aggregation(self, agg_query: Dict[str, Any]) -> Dict[str, Any]:
        """Perform aggregation query"""
        try:
            logger.info(f"📊 Running aggregation: {agg_query}")
            
            # Mock aggregation
            result = {
                "buckets": [
                    {"key": "simple_transfer", "doc_count": 750},
                    {"key": "contract_interaction", "doc_count": 200},
                    {"key": "contract_creation", "doc_count": 50}
                ]
            }
            
            logger.info("✅ Aggregation completed (mock)")
            return result
            
        except Exception as e:
            logger.error(f"❌ Aggregation failed: {e}")
            return {}
    
    def get_transaction_stats(self) -> Dict[str, Any]:
        """Get transaction statistics"""
        try:
            total_tx = len(self.mock_data)
            if total_tx == 0:
                return {"total_transactions": 0}
            
            # Calculate stats
            total_value = sum(tx["value_eth"] for tx in self.mock_data)
            avg_gas_price = sum(tx["gas_price"] for tx in self.mock_data) / total_tx
            
            stats = {
                "total_transactions": total_tx,
                "total_value_eth": total_value,
                "average_gas_price_gwei": avg_gas_price / 10**9,
                "unique_wallets": len(set(tx["from_address"] for tx in self.mock_data) | 
                                   set(tx["to_address"] for tx in self.mock_data))
            }
            
            logger.info(f"📊 Transaction stats: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"❌ Failed to get stats: {e}")
            return {}
