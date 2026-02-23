import logging
import json
from typing import List, Dict, Any
from datetime import datetime
from src.core.simple_spark import SimpleDataFrame

logger = logging.getLogger(__name__)

class KibanaDashboard:
    """Kibana dashboard generator for blockchain analytics"""
    
    def __init__(self):
        self.dashboard_config = {
            "dashboard": {
                "title": "Blockchain Forensics Dashboard",
                "description": "Real-time blockchain transaction analysis",
                "panelsJSON": "",
                "timeRestore": False,
                "timeTo": "now",
                "timeFrom": "now-24h",
                "refreshInterval": {
                    "pause": False,
                    "value": 30000
                },
                "kibanaSavedObjectMeta": {
                    "searchSourceJSON": json.dumps({
                        "query": {"match_all": {}},
                        "filter": []
                    })
                }
            }
        }
        self.panels = []
    
    def create_transaction_volume_panel(self) -> Dict[str, Any]:
        """Create transaction volume over time panel"""
        return {
            "id": "transaction-volume",
            "type": "histogram",
            "title": "Transaction Volume (Last 24h)",
            "gridData": {
                "x": 0,
                "y": 0,
                "w": 24,
                "h": 15,
                "i": "1"
            },
            "visState": json.dumps({
                "title": "Transaction Volume",
                "type": "histogram",
                "params": {
                    "grid": {"categoryLines": False, "style": {"color": "#eee"}},
                    "categoryAxes": [{
                        "id": "CategoryAxis-1",
                        "type": "category",
                        "position": "bottom",
                        "show": True,
                        "style": {},
                        "scale": {"type": "linear"},
                        "labels": {"show": True, "truncate": 100},
                        "title": {"text": "Timestamp"}
                    }],
                    "valueAxes": [{
                        "id": "ValueAxis-1",
                        "name": "LeftAxis-1",
                        "type": "value",
                        "position": "left",
                        "show": True,
                        "style": {},
                        "scale": {"type": "linear", "mode": "normal"},
                        "labels": {"show": True, "rotate": 0, "filter": False, "truncate": 100},
                        "title": {"text": "Transaction Count"}
                    }],
                    "seriesParams": [{
                        "show": True,
                        "type": "histogram",
                        "mode": "stacked",
                        "data": {"label": "Transaction Count", "id": "1"}
                    }]
                },
                "aggs": [
                    {
                        "id": "1",
                        "enabled": True,
                        "type": "count",
                        "schema": "metric",
                        "params": {}
                    },
                    {
                        "id": "2",
                        "enabled": True,
                        "type": "date_histogram",
                        "schema": "segment",
                        "params": {
                            "field": "block_timestamp",
                            "interval": "1h",
                            "customInterval": "2h",
                            "min_doc_count": 1,
                            "extended_bounds": {}
                        }
                    }
                ]
            })
        }
    
    def create_gas_price_panel(self) -> Dict[str, Any]:
        """Create gas price analysis panel"""
        return {
            "id": "gas-price-analysis",
            "type": "line",
            "title": "Gas Price Trends",
            "gridData": {
                "x": 24,
                "y": 0,
                "w": 24,
                "h": 15,
                "i": "2"
            },
            "visState": json.dumps({
                "title": "Gas Price Trends",
                "type": "line",
                "params": {
                    "grid": {"categoryLines": False, "style": {"color": "#eee"}},
                    "categoryAxes": [{
                        "id": "CategoryAxis-1",
                        "type": "category",
                        "position": "bottom",
                        "show": True,
                        "style": {},
                        "scale": {"type": "linear"},
                        "labels": {"show": True, "truncate": 100},
                        "title": {"text": "Time"}
                    }],
                    "valueAxes": [{
                        "id": "ValueAxis-1",
                        "name": "LeftAxis-1",
                        "type": "value",
                        "position": "left",
                        "show": True,
                        "style": {},
                        "scale": {"type": "linear", "mode": "normal"},
                        "labels": {"show": True, "rotate": 0, "filter": False, "truncate": 100},
                        "title": {"text": "Gas Price (Gwei)"}
                    }],
                    "seriesParams": [{
                        "show": True,
                        "type": "line",
                        "mode": "normal",
                        "data": {"label": "Avg Gas Price", "id": "1"},
                        "drawLinesBetweenPoints": True,
                        "showCircles": True
                    }]
                },
                "aggs": [
                    {
                        "id": "1",
                        "enabled": True,
                        "type": "avg",
                        "schema": "metric",
                        "params": {"field": "gas_price"}
                    },
                    {
                        "id": "2",
                        "enabled": True,
                        "type": "date_histogram",
                        "schema": "segment",
                        "params": {
                            "field": "block_timestamp",
                            "interval": "1h",
                            "customInterval": "2h",
                            "min_doc_count": 1,
                            "extended_bounds": {}
                        }
                    }
                ]
            })
        }
    
    def create_suspicious_transactions_panel(self) -> Dict[str, Any]:
        """Create suspicious transactions detection panel"""
        return {
            "id": "suspicious-tx",
            "type": "table",
            "title": "High-Value Transactions (> 10 ETH)",
            "gridData": {
                "x": 0,
                "y": 15,
                "w": 48,
                "h": 20,
                "i": "3"
            },
            "visState": json.dumps({
                "title": "High-Value Transactions",
                "type": "table",
                "params": {
                    "perPage": 10,
                    "showPartialRows": False,
                    "showMeticsAtAllLevels": False,
                    "sort": {
                        "columnIndex": 0,
                        "direction": "desc"
                    },
                    "showTotal": False,
                    "totalFunc": "sum"
                },
                "aggs": [
                    {
                        "id": "1",
                        "enabled": True,
                        "type": "avg",
                        "schema": "metric",
                        "params": {}
                    },
                    {
                        "id": "2",
                        "enabled": True,
                        "type": "terms",
                        "schema": "bucket",
                        "params": {
                            "field": "hash",
                            "size": 10,
                            "order": "desc",
                            "orderBy": "1"
                        }
                    },
                    {
                        "id": "3",
                        "enabled": True,
                        "type": "terms",
                        "schema": "bucket",
                        "params": {
                            "field": "from_address",
                            "size": 5,
                            "order": "desc",
                            "orderBy": "1"
                        }
                    },
                    {
                        "id": "4",
                        "enabled": True,
                        "type": "terms",
                        "schema": "bucket",
                        "params": {
                            "field": "to_address",
                            "size": 5,
                            "order": "desc",
                            "orderBy": "1"
                        }
                    },
                    {
                        "id": "5",
                        "enabled": True,
                        "type": "avg",
                        "schema": "metric",
                        "params": {"field": "value"}
                    }
                ]
            })
        }
    
    def create_wallet_activity_panel(self) -> Dict[str, Any]:
        """Create wallet activity heatmap panel"""
        return {
            "id": "wallet-activity",
            "type": "heatmap",
            "title": "Most Active Wallets",
            "gridData": {
                "x": 0,
                "y": 35,
                "w": 24,
                "h": 15,
                "i": "4"
            },
            "visState": json.dumps({
                "title": "Most Active Wallets",
                "type": "heatmap",
                "params": {
                    "addTooltip": True,
                    "addLegend": True,
                    "enableHover": False,
                    "legendPosition": "right",
                    "times": [],
                    "colorsNumber": 4,
                    "colorSchema": "Greens",
                    "setColorRange": False,
                    "colorsRange": [],
                    "invertColors": False,
                    "percentageMode": False,
                    "valueAxes": [{
                        "show": False,
                        "id": "ValueAxis-1",
                        "type": "value",
                        "scale": {"type": "linear", "defaultYExtents": False}
                    }]
                },
                "aggs": [
                    {
                        "id": "1",
                        "enabled": True,
                        "type": "count",
                        "schema": "metric",
                        "params": {}
                    },
                    {
                        "id": "2",
                        "enabled": True,
                        "type": "terms",
                        "schema": "segment",
                        "params": {
                            "field": "from_address",
                            "size": 10,
                            "order": "desc",
                            "orderBy": "1"
                        }
                    },
                    {
                        "id": "3",
                        "enabled": True,
                        "type": "terms",
                        "schema": "group",
                        "params": {
                            "field": "to_address",
                            "size": 5,
                            "order": "desc",
                            "orderBy": "1"
                        }
                    }
                ]
            })
        }
    
    def create_network_flow_panel(self) -> Dict[str, Any]:
        """Create transaction network flow panel"""
        return {
            "id": "network-flow",
            "type": "pie",
            "title": "Transaction Types Distribution",
            "gridData": {
                "x": 24,
                "y": 35,
                "w": 24,
                "h": 15,
                "i": "5"
            },
            "visState": json.dumps({
                "title": "Transaction Types",
                "type": "pie",
                "params": {
                    "addTooltip": True,
                    "addLegend": True,
                    "legendPosition": "right",
                    "isDonut": True
                },
                "aggs": [
                    {
                        "id": "1",
                        "enabled": True,
                        "type": "count",
                        "schema": "metric",
                        "params": {}
                    },
                    {
                        "id": "2",
                        "enabled": True,
                        "type": "terms",
                        "schema": "segment",
                        "params": {
                            "field": "tx_type",
                            "size": 10,
                            "order": "desc",
                            "orderBy": "1"
                        }
                    }
                ]
            })
        }
    
    def build_dashboard(self, spark_df: SimpleDataFrame) -> Dict[str, Any]:
        """Build complete Kibana dashboard configuration"""
        logger.info("📊 Building Kibana dashboard...")
        
        # Add all panels
        self.panels = [
            self.create_transaction_volume_panel(),
            self.create_gas_price_panel(),
            self.create_suspicious_transactions_panel(),
            self.create_wallet_activity_panel(),
            self.create_network_flow_panel()
        ]
        
        # Convert panels to JSON
        self.dashboard_config["dashboard"]["panelsJSON"] = json.dumps(self.panels)
        
        logger.info(f"✅ Created dashboard with {len(self.panels)} panels")
        return self.dashboard_config
    
    def save_dashboard_config(self, filename: str = "kibana_dashboard.json"):
        """Save dashboard configuration to file"""
        dashboard_path = f"./visualization/{filename}"
        
        import os
        os.makedirs(os.path.dirname(dashboard_path), exist_ok=True)
        
        with open(dashboard_path, 'w') as f:
            json.dump(self.dashboard_config, f, indent=2)
        
        logger.info(f"💾 Dashboard configuration saved to {dashboard_path}")
        return dashboard_path
    
    def generate_elasticsearch_mappings(self) -> Dict[str, Any]:
        """Generate Elasticsearch index mappings for blockchain data"""
        return {
            "mappings": {
                "properties": {
                    "hash": {"type": "keyword"},
                    "block_number": {"type": "long"},
                    "from_address": {"type": "keyword"},
                    "to_address": {"type": "keyword"},
                    "value": {"type": "double"},
                    "gas": {"type": "long"},
                    "gas_price": {"type": "double"},
                    "gas_used": {"type": "long"},
                    "input": {"type": "text"},
                    "nonce": {"type": "long"},
                    "block_timestamp": {"type": "date"},
                    "status": {"type": "boolean"},
                    "tx_type": {"type": "keyword"},
                    "value_eth": {"type": "double"},
                    "risk_score": {"type": "integer"},
                    "processed_at": {"type": "date"}
                }
            }
        }
