import random
import time
from typing import List, Dict, Any
from datetime import datetime, timedelta

class SimpleBlockchainClient:
    """Simple blockchain data client for testing without external dependencies"""
    
    def __init__(self):
        pass
    
    def generate_sample_data(self, num_transactions: int = 1000) -> List[Dict[str, Any]]:
        """Generate sample transaction data for testing"""
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
