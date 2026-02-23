import asyncio
import aiohttp
import web3
from web3 import Web3
from typing import List, Dict, Any, Optional
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

class BlockchainDataClient:
    """Client for fetching blockchain data from multiple sources"""
    
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(f"{settings.INFURA_URL}{settings.INFURA_API_KEY}"))
        self.etherscan_base_url = "https://api.etherscan.io/api"
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_latest_block_number(self) -> int:
        """Get the latest block number"""
        try:
            return self.w3.eth.block_number
        except Exception as e:
            logger.error(f"Failed to get latest block: {e}")
            raise
    
    async def get_block_transactions(self, block_number: int) -> List[Dict[str, Any]]:
        """Get all transactions in a block"""
        try:
            block = self.w3.eth.get_block(block_number, full_transactions=True)
            transactions = []
            
            for tx in block.transactions:
                tx_data = {
                    "hash": tx.hex(),
                    "block_number": tx.blockNumber,
                    "from_address": tx['from'].lower() if tx['from'] else None,
                    "to_address": tx['to'].lower() if tx['to'] else None,
                    "value": str(tx.value),
                    "gas": tx.gas,
                    "gas_price": tx.gasPrice,
                    "input": tx.input.hex() if tx.input else "0x",
                    "nonce": tx.nonce,
                    "block_timestamp": block.timestamp
                }
                transactions.append(tx_data)
            
            return transactions
            
        except Exception as e:
            logger.error(f"Failed to get block {block_number}: {e}")
            return []
    
    async def get_transaction_receipt(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        """Get transaction receipt with status and gas used"""
        try:
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            return {
                "hash": receipt['transactionHash'].hex(),
                "status": receipt.status,
                "gas_used": receipt.gasUsed,
                "logs": [log.hex() for log in receipt.logs] if receipt.logs else []
            }
        except Exception as e:
            logger.error(f"Failed to get receipt for {tx_hash}: {e}")
            return None
    
    async def get_address_transactions(self, address: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get transactions for a specific address using Etherscan API"""
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
            async with self.session.get(self.etherscan_base_url, params=params) as response:
                data = await response.json()
                
                if data["status"] == "1":
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
                    
                    return transactions
                else:
                    logger.error(f"Etherscan API error: {data.get('message', 'Unknown error')}")
                    return []
                    
        except Exception as e:
            logger.error(f"Failed to get transactions for {address}: {e}")
            return []
    
    async def get_contract_source_code(self, address: str) -> Optional[Dict[str, Any]]:
        """Get contract source code if available"""
        params = {
            "module": "contract",
            "action": "getsourcecode",
            "address": address,
            "apikey": settings.ETHERSCAN_API_KEY
        }
        
        try:
            async with self.session.get(self.etherscan_base_url, params=params) as response:
                data = await response.json()
                
                if data["status"] == "1" and data["result"]:
                    result = data["result"][0]
                    return {
                        "address": address,
                        "contract_name": result.get("ContractName"),
                        "source_code": result.get("SourceCode"),
                        "compiler_version": result.get("CompilerVersion"),
                        "optimization_used": result.get("OptimizationUsed") == "1"
                    }
                else:
                    return None
                    
        except Exception as e:
            logger.error(f"Failed to get contract source for {address}: {e}")
            return None
    
    async def fetch_block_range(self, start_block: int, end_block: int) -> List[Dict[str, Any]]:
        """Fetch transactions for a range of blocks"""
        all_transactions = []
        
        for block_num in range(start_block, end_block + 1):
            logger.info(f"Fetching block {block_num}")
            transactions = await self.get_block_transactions(block_num)
            all_transactions.extend(transactions)
            
            # Add delay to avoid rate limiting
            await asyncio.sleep(0.1)
        
        return all_transactions
    
    def generate_sample_data(self, num_transactions: int = 1000) -> List[Dict[str, Any]]:
        """Generate sample transaction data for testing"""
        import random
        from datetime import datetime, timedelta
        
        # Sample wallet addresses
        sample_wallets = [
            f"0x{''.join(random.choices('0123456789abcdef', k=40))}" 
            for _ in range(100)
        ]
        
        transactions = []
        base_time = int(datetime.now().timestamp())
        
        for i in range(num_transactions):
            tx = {
                "hash": f"0x{''.join(random.choices('0123456789abcdef', k=64))}",
                "block_number": 18000000 + i // 200,  # ~200 tx per block
                "from_address": random.choice(sample_wallets),
                "to_address": random.choice(sample_wallets),
                "value": str(random.randint(10**15, 10**19)),  # 0.001 to 10 ETH
                "gas": random.randint(21000, 500000),
                "gas_price": random.randint(10**9, 10**11),  # 1-100 gwei
                "gas_used": random.randint(21000, 300000),
                "input": "0x" if random.random() > 0.1 else f"0x{''.join(random.choices('0123456789abcdef', k=8))}",
                "nonce": i,
                "block_timestamp": base_time - random.randint(0, 86400),  # Last 24 hours
                "status": True
            }
            transactions.append(tx)
        
        return transactions
