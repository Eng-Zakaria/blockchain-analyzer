import time
import logging
from typing import Dict, List, Any, Callable
from dataclasses import dataclass
from src.core.simple_spark import SimpleDataFrame
from src.core.mock_neo4j import MockNeo4jClient

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Store performance metrics for comparison"""
    approach: str
    operation: str
    execution_time: float
    memory_usage: float
    result_count: int
    success: bool
    error_message: str = ""

class PerformanceTester:
    """Test and compare Neo4j vs PySpark performance"""
    
    def __init__(self):
        self.neo4j_client = MockNeo4jClient()
        self.results: List[PerformanceMetrics] = []
    
    def time_operation(self, operation: Callable, operation_name: str, approach: str) -> PerformanceMetrics:
        """Time an operation and capture metrics"""
        start_time = time.time()
        success = True
        error_msg = ""
        result_count = 0
        
        try:
            if approach == "neo4j":
                result = operation()
                result_count = len(result) if isinstance(result, list) else 1
            else:  # pyspark
                result = operation()
                if hasattr(result, 'count'):
                    result_count = result.count()
                elif hasattr(result, '__len__'):
                    result_count = len(result)
                else:
                    result_count = 1
                    
        except Exception as e:
            success = False
            error_msg = str(e)
            logger.error(f"Operation {operation_name} failed for {approach}: {e}")
            result_count = 0
        
        execution_time = time.time() - start_time
        
        metrics = PerformanceMetrics(
            approach=approach,
            operation=operation_name,
            execution_time=execution_time,
            memory_usage=0,  # TODO: Implement memory tracking
            result_count=result_count,
            success=success,
            error_message=error_msg
        )
        
        self.results.append(metrics)
        return metrics
    
    def test_wallet_degree_calculation(self, spark_df: SimpleDataFrame, wallet_address: str):
        """Compare wallet degree calculation"""
        
        # Neo4j approach
        def neo4j_degree():
            query = """
            MATCH (w:Wallet {address: $address})-[r:SENT]-()
            RETURN count(r) as degree
            """
            return self.neo4j_client.execute_query(query, {"address": wallet_address})
        
        # PySpark approach
        def pyspark_degree():
            # Mock implementation - just return a count
            return spark_df.count()
        
        neo4j_metrics = self.time_operation(neo4j_degree, "wallet_degree", "neo4j")
        pyspark_metrics = self.time_operation(pyspark_degree, "wallet_degree", "pyspark")
        
        return neo4j_metrics, pyspark_metrics
    
    def test_multi_hop_analysis(self, spark_df: SimpleDataFrame, start_wallet: str, hops: int = 3):
        """Compare multi-hop transaction analysis"""
        
        # Neo4j approach
        def neo4j_multihop():
            match_pattern = "->".join([f"(w{i}:Wallet)" for i in range(hops + 1)])
            rel_pattern = "-[r{i}:SENT]->".join(["" for i in range(hops)])
            
            query = f"""
            MATCH (w0:Wallet {{address: $start_address}}){rel_pattern}{match_pattern}
            RETURN DISTINCT [w{i}.address for i in range(0, {hops})] as path
            LIMIT 100
            """
            return self.neo4j_client.execute_query(query, {"start_address": start_wallet})
        
        # PySpark approach (simplified)
        def pyspark_multihop():
            # Mock implementation - just return some data
            return spark_df.select("to_address").collect()
        
        neo4j_metrics = self.time_operation(neo4j_multihop, f"multi_hop_{hops}", "neo4j")
        pyspark_metrics = self.time_operation(pyspark_multihop, f"multi_hop_{hops}", "pyspark")
        
        return neo4j_metrics, pyspark_metrics
    
    def test_suspicious_pattern_detection(self, spark_df: SimpleDataFrame):
        """Compare suspicious pattern detection"""
        
        # Neo4j approach - find high-frequency traders
        def neo4j_suspicious():
            query = """
            MATCH (w:Wallet)
            WITH w, size((w)-[:SENT]-()) as total_tx
            WHERE total_tx > 100
            RETURN w.address, total_tx
            ORDER BY total_tx DESC
            LIMIT 50
            """
            return self.neo4j_client.execute_query(query)
        
        # PySpark approach
        def pyspark_suspicious():
            # Mock implementation - just return grouped data
            return spark_df.groupBy("from_address").count().collect()
        
        neo4j_metrics = self.time_operation(neo4j_suspicious, "suspicious_detection", "neo4j")
        pyspark_metrics = self.time_operation(pyspark_suspicious, "suspicious_detection", "pyspark")
        
        return neo4j_metrics, pyspark_metrics
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comparison report"""
        report = {
            "summary": {},
            "detailed_results": [],
            "recommendations": []
        }
        
        # Group results by operation
        operations = {}
        for result in self.results:
            if result.operation not in operations:
                operations[result.operation] = []
            operations[result.operation].append(result)
        
        # Analyze each operation
        for operation, results in operations.items():
            neo4j_result = next((r for r in results if r.approach == "neo4j"), None)
            pyspark_result = next((r for r in results if r.approach == "pyspark"), None)
            
            if neo4j_result and pyspark_result:
                speedup = pyspark_result.execution_time / neo4j_result.execution_time if neo4j_result.execution_time > 0 else 0
                
                operation_summary = {
                    "operation": operation,
                    "neo4j_time": neo4j_result.execution_time,
                    "pyspark_time": pyspark_result.execution_time,
                    "speedup": speedup,
                    "neo4j_success": neo4j_result.success,
                    "pyspark_success": pyspark_result.success,
                    "winner": "neo4j" if speedup > 1 else "pyspark"
                }
                
                report["detailed_results"].append(operation_summary)
        
        # Generate recommendations
        report["recommendations"] = self._generate_recommendations(report["detailed_results"])
        
        return report
    
    def _generate_recommendations(self, results: List[Dict]) -> List[str]:
        """Generate recommendations based on performance results"""
        recommendations = []
        
        neo4j_wins = sum(1 for r in results if r["winner"] == "neo4j")
        pyspark_wins = sum(1 for r in results if r["winner"] == "pyspark")
        
        if neo4j_wins > pyspark_wins:
            recommendations.append("Neo4j performs better for graph traversal queries")
            recommendations.append("Use Neo4j for multi-hop analysis and relationship queries")
        else:
            recommendations.append("PySpark performs better for analytical queries")
            recommendations.append("Use PySpark for aggregations and batch processing")
        
        recommendations.append("Consider hybrid approach: Neo4j for real-time queries, PySpark for batch analytics")
        
        return recommendations
