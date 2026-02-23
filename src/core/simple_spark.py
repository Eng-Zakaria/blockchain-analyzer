import logging
from typing import List, Dict, Any
import pandas as pd

logger = logging.getLogger(__name__)

class SimpleSparkClient:
    """Mock Spark client using pandas for testing without Spark"""
    
    def __init__(self):
        logger.info("Using Simple Spark Client (pandas-based) - no actual Spark cluster")
    
    def create_dataframe(self, data: List[Dict[str, Any]]) -> 'SimpleDataFrame':
        """Create a simple dataframe"""
        return SimpleDataFrame(data)
    
    def stop(self):
        """Mock stop method"""
        pass

class SimpleDataFrame:
    """Simple DataFrame implementation using pandas"""
    
    def __init__(self, data: List[Dict[str, Any]]):
        self.df = pd.DataFrame(data)
        self._count = len(data)
    
    def count(self):
        """Count rows"""
        return self._count
    
    def filter(self, condition):
        """Mock filter - just return all data for simplicity"""
        return self
    
    def select(self, *columns):
        """Mock select - return selected columns"""
        selected_data = self.df[list(columns)].to_dict('records')
        return SimpleDataFrame(selected_data)
    
    def groupBy(self, column):
        """Mock group by - return simple aggregation"""
        return SimpleGroupedData(self.df, column)
    
    def withColumn(self, col_name, expression):
        """Mock withColumn - just return same dataframe"""
        return self
    
    def dropDuplicates(self, columns):
        """Mock drop duplicates"""
        unique_data = self.df.drop_duplicates(subset=columns).to_dict('records')
        return SimpleDataFrame(unique_data)
    
    def collect(self):
        """Return data as list of Row objects"""
        return [SimpleRow(row) for row in self.df.to_dict('records')]
    
    def write(self):
        """Mock write operations"""
        return SimpleDataFrameWriter()

class SimpleGroupedData:
    """Mock grouped data operations"""
    
    def __init__(self, df, group_column):
        self.df = df
        self.group_column = group_column
    
    def agg(self, *expressions):
        """Mock aggregation"""
        grouped = self.df.groupby(self.group_column).size().reset_index(name='count')
        return SimpleDataFrame(grouped.to_dict('records'))
    
    def count(self):
        """Mock count"""
        return SimpleDataFrame(self.df.groupby(self.group_column).size().reset_index(name='count').to_dict('records'))

class SimpleRow:
    """Mock Row object"""
    
    def __init__(self, data):
        self._data = data
    
    def __getitem__(self, key):
        return self._data[key]
    
    def __getattr__(self, name):
        return self._data.get(name)

class SimpleDataFrameWriter:
    """Mock DataFrame writer"""
    
    def mode(self, mode):
        return self
    
    def parquet(self, path):
        logger.info(f"Mock writing to parquet: {path}")
        return self
