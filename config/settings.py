

import os
from pathlib import Path

class Settings:
    # Infura Configuration
    INFURA_API_KEY: str = os.getenv("INFURA_API_KEY", "")
    INFURA_URL: str = "https://mainnet.infura.io/v3/"
    
    # Etherscan Configuration
    ETHERSCAN_API_KEY: str = os.getenv("ETHERSCAN_API_KEY", "")
    
    # Neo4j Configuration
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "password")
    
    # Spark Configuration
    SPARK_MASTER: str = os.getenv("SPARK_MASTER", "local[*]")
    
    # Chain Settings
    CHAIN_ID: int = int(os.getenv("CHAIN_ID", "1"))
    NETWORK: str = os.getenv("NETWORK", "mainnet")
    
    # Path Configuration
    DATA_DIR: Path = Path(__file__).resolve().parent.parent / "data"
    ETL_BRONZE_PATH: Path = Path(__file__).resolve().parent.parent / "etl" / "bronze"
    ETL_SILVER_PATH: Path = Path(__file__).resolve().parent.parent / "etl" / "silver"
    ETL_GOLD_PATH: Path = Path(__file__).resolve().parent.parent / "etl" / "gold"

# Global settings instance
settings = Settings()
