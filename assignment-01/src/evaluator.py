from utils.data_types import InputDataType, MetricType
# from torchmetrics.classification import BinaryPrecision, BinaryF1Score, BinaryAccuracy


class MetricsCalculator:
    """Service class responsible for calculating various classification metrics."""
    
    @staticmethod
    def calculate_recall(tp: int, fn: int) -> float:
        """Calculate recall from confusion matrix values."""
        try:
            return tp / (tp + fn) if (tp + fn) > 0 else 0.0
        except ZeroDivisionError:
            return 0.0

    @staticmethod
    def calculate_metric(data: InputDataType, metric_type: MetricType) -> float:
        """Calculate specified metric directly from confusion matrix values."""
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
            raise ValueError(f"Invalid metric type: {metric_type}")