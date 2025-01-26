from src.evaluator import MetricsCalculator
from utils.data_types import InputDataType, MetricType

from typing import List, Optional

class ThresholdOptimizer:
    """Class for finding optimal classification threshold."""
    
    def __init__(self, data: List[InputDataType], metric_type: MetricType = MetricType.RECALL):
        """
        Initialize with a list of InputDataType.
        
        Args:
            data: List of InputDataType objects
            metric_type: Type of metric to optimize (default: recall)
        
        Raises:
            ValueError: If data is empty
        """
        if not data:
            raise ValueError("Metrics list cannot be empty")
            
        self.data = data
        self.metric_type = metric_type
        self.calculator = MetricsCalculator()

    def find_best_threshold(self, min_threshold: float = 0.9) -> Optional[float]:
        """
        Find the best threshold that yields metric >= min_threshold.
        
        Args:
            min_threshold: Minimum required metric value (default: 0.9)
            
        Returns:
            The highest threshold that meets the minimum requirement,
            or None if no threshold satisfies the condition.
            
        Raises:
            ValueError: If min_threshold is not between 0 and 1
        """
        if not 0 <= min_threshold <= 1:
            raise ValueError("min_threshold must be between 0 and 1")

        valid_thresholds = []
        for metrics in self.data:
            calculated_metric = self.calculator.calculate_metric(metrics, self.metric_type)
            if calculated_metric >= min_threshold:
                valid_thresholds.append(metrics)
        
        if not valid_thresholds:
            return None
        
        # Return the highest threshold that meets the requirement
        return max(valid_thresholds, key=lambda x: x.threshold).threshold
