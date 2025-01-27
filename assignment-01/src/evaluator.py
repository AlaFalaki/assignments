from utils.data_types import InputDataType, MetricType
# from torchmetrics.classification import BinaryPrecision, BinaryF1Score, BinaryAccuracy

import logging

# Set up logger
logger = logging.getLogger(__name__)

class MetricsCalculator:
    """Service class responsible for calculating various classification metrics."""
    
    @staticmethod
    def calculate_recall(tp: int, fn: int) -> float:
        """Calculate recall from confusion matrix values."""
        logger.debug(f"Calculating recall with tp={tp}, fn={fn}")

        try:
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            logger.info(f"Calculated recall: {recall:.4f}")
            return recall

        except ZeroDivisionError:
            logger.warning("Zero division encountered in recall calculation, returning 0.0")
            return 0.0

    @staticmethod
    def calculate_metric(data: InputDataType, metric_type: MetricType) -> float:
        """Calculate specified metric directly from confusion matrix values."""
        logger.info(f"Calculating {metric_type} metric")
        logger.debug(
            f"Confusion matrix values - TP: {data.true_positives}, TN: {data.true_negatives}, "
            f"FP: {data.false_positives}, FN: {data.false_negatives}"
        )

        tp = data.true_positives
        tn = data.true_negatives
        fp = data.false_positives
        fn = data.false_negatives
        
        if metric_type == MetricType.RECALL:
            return MetricsCalculator.calculate_recall(tp, fn)
        # elif metric_type == MetricType.PRECISION:
        #     return BinaryPrecision()(tp, fp)
        # elif metric_type == MetricType.F1:
        #     return BinaryF1Score()(tp, fp, fn),
        # elif metric_type == MetricType.ACCURACY:
        #     return BinaryF1Score()(tp, fp, fn)
        else:
            logger.error(f"Invalid metric type requested: {metric_type}")
            raise ValueError(f"Invalid metric type: {metric_type}")