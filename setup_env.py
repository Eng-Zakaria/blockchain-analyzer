#!/usr/bin/env python3
"""
Setup script to configure environment variables for real blockchain data
"""

import os
from pathlib import Path

def setup_environment():
    """Setup environment variables with user input"""
    
    print("🔧 Blockchain Analyzer - Environment Setup")
    print("=" * 50)
    
    # Get Infura API key
    infura_key = input("Enter your Infura API key: ").strip()
    if not infura_key:
        print("❌ Infura API key is required!")
        return False
    
    # Get Etherscan API key (optional)
    etherscan_key = input("Enter your Etherscan API key (optional): ").strip()
    
    # Get Neo4j configuration (optional)
    neo4j_uri = input("Enter Neo4j URI (default: bolt://localhost:7687): ").strip()
    if not neo4j_uri:
        neo4j_uri = "bolt://localhost:7687"
    
    neo4j_user = input("Enter Neo4j username (default: neo4j): ").strip()
    if not neo4j_user:
        neo4j_user = "neo4j"
    
    neo4j_password = input("Enter Neo4j password: ").strip()
    
    # Create .env file
    env_content = f"""# Blockchain API Keys
INFURA_API_KEY={infura_key}
ETHERSCAN_API_KEY={etherscan_key}

# Neo4j Configuration
NEO4J_URI={neo4j_uri}
NEO4J_USER={neo4j_user}
NEO4J_PASSWORD={neo4j_password}

# Spark Configuration
SPARK_MASTER=local[*]

# Chain Settings
CHAIN_ID=1
NETWORK=mainnet

# Data Paths
DATA_DIR=./data
ETL_BRONZE_PATH=./etl/bronze
ETL_SILVER_PATH=./etl/silver
ETL_GOLD_PATH=./etl/gold
"""
    
    env_file = Path(__file__).parent / ".env"
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Environment configuration saved to {env_file}")
    print("🚀 You can now run the application with real blockchain data!")
    
    return True

if __name__ == "__main__":
    setup_environment()
