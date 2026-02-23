import requests
import logging
from typing import List, Dict, Any, Optional
from config.settings import settings

logger = logging.getLogger(__name__)

class RealBlockchainClient:
    """Real blockchain data client using Infura and Etherscan APIs"""
    
    def __init__(self):
        if not settings.INFURA_API_KEY:
            raise ValueError("INFURA_API_KEY is required. Run setup_env.py first.")
        
        self.infura_url = f"https://mainnet.infura.io/v3/{settings.INFURA_API_KEY}"
        self.etherscan_url = "https://api.etherscan.io/api"
        
    def get_latest_block_number(self) -> int:
        """Get the latest block number from Infura"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "eth_blockNumber",
                "params": [],
                "id": 1
            }
            
            response = requests.post(self.infura_url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            if "result" in result:
                return int(result["result"], 16)  # Convert hex to int
            
            raise Exception(f"Unexpected response: {result}")
            
        except Exception as e:
            logger.error(f"Failed to get latest block: {e}")
            raise
    
    def get_block_transactions(self, block_number: int) -> List[Dict[str, Any]]:
        """Get all transactions in a block from Infura"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "eth_getBlockByNumber",
                "params": [hex(block_number), True],  # True for full transactions
                "id": 1
            }
            
            response = requests.post(self.infura_url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            if "result" not in result:
                raise Exception(f"Unexpected response: {result}")
            
            block = result["result"]
            if not block:
                return []
            
            transactions = []
            for tx in block.get("transactions", []):
                tx_data = {
                    "hash": tx.get("hash", ""),
                    "block_number": block_number,
                    "from_address": tx.get("from", "").lower() if tx.get("from") else None,
                    "to_address": tx.get("to", "").lower() if tx.get("to") else None,
                    "value": tx.get("value", "0"),
                    "gas": int(tx.get("gas", "0"), 16),
                    "gas_price": int(tx.get("gasPrice", "0"), 16),
                    "input": tx.get("input", "0x"),
                    "nonce": int(tx.get("nonce", "0"), 16),
                    "block_timestamp": int(block.get("timestamp", "0"), 16)
                }
                transactions.append(tx_data)
            
            logger.info(f"Retrieved {len(transactions)} transactions from block {block_number}")
            return transactions
            
        except Exception as e:
            logger.error(f"Failed to get block {block_number}: {e}")
            return []
    
    def get_address_transactions(self, address: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get transactions for a specific address using Etherscan API"""
        if not settings.ETHERSCAN_API_KEY:
            logger.warning("Etherscan API key not provided. Using limited data.")
            return []
        
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": 0,
            "endblock": 99999999,
            "sort": "desc",
            "apikey": settings.ETHERSCAN_API_KEY
        }
        
        try:
            response = requests.get(self.etherscan_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data.get("status") == "1" and data.get("result"):
                transactions = []
                for tx in data["result"][:limit]:
                    tx_data = {
                        "hash": tx["hash"],
                        "block_number": int(tx["blockNumber"]),
                        "from_address": tx["from"].lower(),
                        "to_address": tx["to"].lower() if tx["to"] else None,
                        "value": tx["value"],
                        "gas": int(tx["gas"]),
                        "gas_price": int(tx["gasPrice"]),
                        "gas_used": int(tx["gasUsed"]),
                        "input": tx["input"],
                        "nonce": int(tx["nonce"]),
                        "block_timestamp": int(tx["timeStamp"]),
                        "status": int(tx["isError"]) == 0
                    }
                    transactions.append(tx_data)
                
                logger.info(f"Retrieved {len(transactions)} transactions for address {address}")
                return transactions
            else:
                logger.error(f"Etherscan API error: {data.get('message', 'Unknown error')}")
                return []
                
        except Exception as e:
            logger.error(f"Failed to get transactions for {address}: {e}")
            return []
    
    def fetch_recent_blocks(self, num_blocks: int = 5) -> List[Dict[str, Any]]:
        """Fetch transactions from recent blocks"""
        try:
            latest_block = self.get_latest_block_number()
            logger.info(f"Latest block: {latest_block}")
            
            all_transactions = []
            start_block = max(0, latest_block - num_blocks + 1)
            
            for block_num in range(start_block, latest_block + 1):
                logger.info(f"Fetching block {block_num}")
                transactions = self.get_block_transactions(block_num)
                all_transactions.extend(transactions)
            
            logger.info(f"Total transactions fetched: {len(all_transactions)}")
            return all_transactions
            
        except Exception as e:
            logger.error(f"Failed to fetch recent blocks: {e}")
            return []
