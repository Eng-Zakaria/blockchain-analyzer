#!/usr/bin/env python3
"""
Blockchain Analyzer - Main Entry Point
Neo4j vs PySpark Performance Comparison
"""

import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.simple_spark import SimpleSparkClient
from src.core.mock_neo4j import MockNeo4jClient
from src.data.simple_client import SimpleBlockchainClient
from src.data.real_blockchain_client import RealBlockchainClient
from src.comparison.performance_tester import PerformanceTester
from src.spark.etl_pipeline import ETLPipeline
from src.visualization.kibana_dashboard import KibanaDashboard
from src.visualization.elasticsearch_client import ElasticsearchClient
from config.settings import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main application entry point"""
    logger.info("🚀 Starting Blockchain Analyzer")
    
    try:
        # Initialize components
        spark = SimpleSparkClient()
        neo4j_client = MockNeo4jClient()
        performance_tester = PerformanceTester()
        kibana_dashboard = KibanaDashboard()
        elasticsearch_client = ElasticsearchClient()
        
        # Choose data client based on API key availability
        if settings.INFURA_API_KEY and settings.INFURA_API_KEY != "":
            logger.info("🌐 Using real blockchain data from Infura")
            blockchain_client = RealBlockchainClient()
        else:
            logger.info("📝 Using sample blockchain data (no API key found)")
            logger.info("Run 'python setup_env.py' to configure API keys")
            blockchain_client = SimpleBlockchainClient()
        
        # Setup Neo4j schema
        logger.info("📊 Setting up Neo4j schema...")
        try:
            neo4j_client.create_wallet_constraints()
            neo4j_client.create_indexes()
        except Exception as e:
            logger.warning(f"Neo4j setup failed (continuing without Neo4j): {e}")
        
        # Generate sample data for testing
        logger.info("📝 Getting transaction data...")
        
        if isinstance(blockchain_client, RealBlockchainClient):
            # Fetch real blockchain data
            sample_transactions = blockchain_client.fetch_recent_blocks(3)  # Last 3 blocks
            if not sample_transactions:
                logger.warning("No real data fetched, falling back to sample data")
                sample_transactions = SimpleBlockchainClient().generate_sample_data(500)
        else:
            # Use sample data
            sample_transactions = blockchain_client.generate_sample_data(1000)
        
        logger.info(f"Using {len(sample_transactions)} transactions")
        
        # Run ETL pipeline
        logger.info("⚡ Running ETL pipeline...")
        etl_pipeline = ETLPipeline(spark, neo4j_client)
        spark_df = etl_pipeline.process_transactions(sample_transactions)
        
        # Performance comparison tests
        logger.info("🏁 Running performance comparison tests...")
        
        # Test 1: Wallet degree calculation
        sample_wallet = sample_transactions[0]["from_address"]
        neo4j_metrics, pyspark_metrics = performance_tester.test_wallet_degree_calculation(
            spark_df, sample_wallet
        )
        
        # Test 2: Multi-hop analysis
        neo4j_metrics2, pyspark_metrics2 = performance_tester.test_multi_hop_analysis(
            spark_df, sample_wallet, hops=3
        )
        
        # Test 3: Suspicious pattern detection
        neo4j_metrics3, pyspark_metrics3 = performance_tester.test_suspicious_pattern_detection(
            spark_df
        )
        
        # Generate comparison report
        logger.info("📋 Generating comparison report...")
        report = performance_tester.generate_report()
        
        # Create Kibana dashboard
        logger.info("📊 Creating Kibana dashboard...")
        dashboard_config = kibana_dashboard.build_dashboard(spark_df)
        dashboard_path = kibana_dashboard.save_dashboard_config()
        
        # Index data into Elasticsearch for Kibana
        logger.info("🔍 Indexing data into Elasticsearch...")
        mappings = kibana_dashboard.generate_elasticsearch_mappings()
        elasticsearch_client.create_index(mappings)
        elasticsearch_client.index_transactions(sample_transactions)
        
        # Get Elasticsearch stats
        es_stats = elasticsearch_client.get_transaction_stats()
        logger.info(f"📈 Elasticsearch stats: {es_stats}")
        
        # Print final report
        print("\n" + "="*50)
        print("🏆 PERFORMANCE COMPARISON REPORT")
        print("="*50)
        
        for operation in report["summary"]:
            metrics = report["summary"][operation]
            print(f"\n📊 Operation: {operation}")
            print(f"   Neo4j Time: {metrics['neo4j_time']:.4f}s")
            print(f"   PySpark Time: {metrics['pyspark_time']:.4f}s")
            print(f"   Speedup: {metrics['speedup']:.2f}x")
            print(f"   Winner: {metrics['winner']}")
        
        print(f"\n💡 Recommendations:")
        for rec in report["recommendations"]:
            print(f"   • {rec}")
        
        print(f"\n📊 Kibana Dashboard:")
        print(f"   • Dashboard config saved to: {dashboard_path}")
        print(f"   • Total transactions indexed: {es_stats.get('total_transactions', 0)}")
        print(f"   • Unique wallets: {es_stats.get('unique_wallets', 0)}")
        print(f"   • Total ETH volume: {es_stats.get('total_value_eth', 0):.2f}")
        
        print("="*50)
        logger.info("✅ Blockchain Analyzer completed successfully")
        spark.stop()
        
        logger.info("✅ Blockchain Analyzer completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Application failed: {e}")
        raise

if __name__ == "__main__":
    main()
