

# # config/settings.py
# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     # Blockchain
#     INFURA_KEY = os.getenv("")
#     ETHERSCAN_KEY = os.getenv("")
    
#     # Neo4j
#     NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
#     NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
#     NEO4J_PASS = os.getenv("NEO4J_PASS", "password")
    
#     # Spark
#     SPARK_MASTER = os.getenv("SPARK_MASTER", "local[*]")

import os
from pathlib import Path
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Infura Configuration
    INFURA_API_KEY: str
    INFURA_URL: str = "https://mainnet.infura.io/v3/"
    
    # Etherscan Configuration
    ETHERSCAN_API_KEY: str = ""
    
    # Chain Settings
    CHAIN_ID: int = 1
    
    # Path Configuration
    DATA_DIR: Path = Path(__file__).resolve().parent.parent / "data"
    
    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"
        env_file_encoding = 'utf-8'
