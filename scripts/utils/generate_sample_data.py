# scripts/generate_sample_data.py
import json
from pathlib import Path

sample_txs = [
    {
        "from_address": "0xabc...",
        "to_address": "0xdef...",
        "value": "1000000000000000000",  # 1 ETH in wei
        "block_number": 19200001
    },
    {
        "from_address": "0xabc...",
        "to_address": "0xdef...",
        "value": "1000000000000000000",  # 1 ETH in wei
        "block_number": 19200002
    },
    {
        "from_address": "0xabc...",
        "to_address": "0xdef...",
        "value": "1000000000000000000",  # 1 ETH in wei
        "block_number": 19200003
    },
    {
        "from_address": "0xabc...",
        "to_address": "0xdef...",
        "value": "1000000000000000000",  # 1 ETH in wei
        "block_number": 19200004
    },
    {
        "from_address": "0xabc...",
        "to_address": "0xdef...",
        "value": "1000000000000000000",  # 1 ETH in wei
        "block_number": 19200005
    },
    {
        "from_address": "0xabc...",
        "to_address": "0xdef...",
        "value": "1000000000000000000",  # 1 ETH in wei
        "block_number": 19200006
    },
   
]

Path("data/raw/transactions").mkdir(parents=True, exist_ok=True)
with open("data/raw/transactions/sample.json", "w") as f:
    json.dump(sample_txs, f)