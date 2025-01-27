from src.evaluator import MetricsCalculator
from utils.data_types import InputDataType, MetricType

from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

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
        logger.info(f"Initializing ThresholdOptimizer with metric type: {metric_type.name}")

        if not data:
            logger.error("Attempted to initialize with empty data")
            raise ValueError("Metrics list cannot be empty")
            
        logger.debug(f"Initialized with {len(data)} data points")
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
        logger.info(f"Finding best threshold with minimum requirement: {min_threshold}")

        if not 0 <= min_threshold <= 1:
            logger.error(f"Invalid min_threshold value: {min_threshold}")
            raise ValueError("min_threshold must be between 0 and 1")

        valid_thresholds = []
        logger.debug(f"Processing {len(self.data)} thresholds")

        for metrics in self.data:
            calculated_metric = self.calculator.calculate_metric(metrics, self.metric_type)
            logger.debug(
                    f"Threshold {metrics.threshold:.4f} yielded {self.metric_type.name}: "
                    f"{calculated_metric:.4f}"
                )

            if calculated_metric >= min_threshold:
                valid_thresholds.append(metrics)
                logger.debug(f"Threshold {metrics.threshold:.4f} meets minimum requirement")
        
        if not valid_thresholds:
            logger.warning("No thresholds found meeting the minimum requirement")
            return None
        
        # Return the highest threshold that meets the requirement
        best_threshold = max(valid_thresholds, key=lambda x: x.threshold).threshold
        logger.info(f"Found best threshold: {best_threshold:.4f}")

        return best_threshold
