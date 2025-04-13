# 🔍 Blockchain Analyzer

**Ethereum Transaction Intelligence Platform with ETL Pipeline & Threat Detection**

A modular toolkit for blockchain forensic analysis featuring multi-layer data processing and anomaly detection capabilities.

## Features

✅ **Multi-layer ETL Pipeline**  
```Bronze → Silver → Gold``` architecture for data refinement  
✅ **Threat Detection**  
- Chain Hopping identification  
- Smurfing pattern recognition  
- Peel Chain analysis  
✅ **Big Data Processing**  
Apache Spark-powered analytics  
✅ **Visualization**  
- Kibana dashboards  
- Neo4j graph analysis  
✅ **Live Data Ingestion**  
Real-time integration with Infura/Etherscan APIs  

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) 
![Web3.py](https://img.shields.io/badge/Web3.py-6.x-green) 
![Apache Spark](https://img.shields.io/badge/Apache_Spark-3.x-orange) 
![Docker](https://img.shields.io/badge/Docker-24.x-blueviolet)

**Core Components:**  
Python · Web3.py · Apache Spark · Neo4j · Kibana · Docker · Etherscan API · Infura

## Use Cases

🕵️ **AML/CFT Compliance Monitoring**  
🔍 **DeFi Protocol Auditing**  
🖼️ **NFT Market Analysis**  
📊 **Wallet Behavior Profiling**

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Configure API keys in `config/.env`
3. Run Spark application: `spark-submit src/spark/app.py`
