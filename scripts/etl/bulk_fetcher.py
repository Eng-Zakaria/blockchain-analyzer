# scripts/etl/bulk_fetcher.py
from config.settings import settings
import json
from web3 import Web3
from pathlib import Path
from datetime import datetime
import time
from hexbytes import HexBytes
from collections.abc import MutableMapping

class BulkTransactionFetcher:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(f"{settings.INFURA_URL}{settings.INFURA_API_KEY}"))
        self.output_dir = settings.DATA_DIR / "raw"
        self.output_dir.mkdir(exist_ok=True)
        
    def _convert_value(self, value):
        """Special handling for different value types"""
        if isinstance(value, HexBytes):
            return value.hex()
        elif isinstance(value, bytes):
            return value.hex()
        elif isinstance(value, (int, float, str, bool)) or value is None:
            return value
        elif isinstance(value, MutableMapping):
            return {k: self._convert_value(v) for k, v in value.items()}
        elif isinstance(value, (list, tuple)):
            return [self._convert_value(x) for x in value]
        else:
            return str(value)  # Fallback conversion

    def fetch_block_range(self, start_block, end_block, batch_size=100):
        """Fetch all transactions in a block range"""
        for block_num in range(start_block, end_block + 1):
            try:
                start_time = time.time()
                block = self.w3.eth.get_block(block_num, full_transactions=True)
                
                # Convert entire block to serializable format first
                block_data = {
                    'number': block.number,
                    'timestamp': block.timestamp,
                    'transactions': []
                }
                
                success_count = 0
                for tx in block.transactions:
                    try:
                        tx_dict = dict(tx)
                        receipt = self.w3.eth.get_transaction_receipt(tx.hash)
                        
                        tx_data = {
                            **{k: self._convert_value(v) for k, v in tx_dict.items()},
                            'receipt': {k: self._convert_value(v) for k, v in dict(receipt).items()},
                            'block_datetime': datetime.utcfromtimestamp(block.timestamp).isoformat()
                        }
                        
                        self._save_transaction(block.number, tx_data)
                        success_count += 1
                        
                    except Exception as tx_error:
                        print(f"⚠️ Failed to process tx {tx.hash.hex()}: {str(tx_error)}")
                        continue
                
                elapsed = time.time() - start_time
                print(f"✅ Block {block_num} ({success_count}/{len(block.transactions)} txs) in {elapsed:.2f}s")
                
                if block_num % batch_size == 0:
                    time.sleep(0.5)  # Rate limiting
                    
            except Exception as block_error:
                print(f"❌ Block {block_num} failed: {str(block_error)}")
                continue

    def _save_transaction(self, block_num, tx_data):
        """Save transaction with proper encoding"""
        block_dir = self.output_dir / str(block_num)
        block_dir.mkdir(exist_ok=True)
        
        filepath = block_dir / f"{tx_data['hash']}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(tx_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetcher = BulkTransactionFetcher()
    
    # Test with recent blocks
    latest = fetcher.w3.eth.block_number
    fetcher.fetch_block_range(latest - 20, latest)  # First try with just 5 blocks