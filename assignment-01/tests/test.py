import pytest
from unittest.mock import patch
from utils.data_types import InputDataType, MetricType
from src.evaluator import MetricsCalculator
from src.optimizer import ThresholdOptimizer

@pytest.fixture
def metrics_list():
    return [
        InputDataType(threshold=0.3, true_positives=90, true_negatives=70, false_positives=30, false_negatives=10),
        InputDataType(threshold=0.5, true_positives=80, true_negatives=80, false_positives=20, false_negatives=20),
        InputDataType(threshold=0.7, true_positives=70, true_negatives=90, false_positives=10, false_negatives=30)
    ]

# MetricsCalculator Tests
class TestMetricsCalculator:
    def test_calculate_recall_normal(self):
        """Test recall calculation with normal values"""
        recall = MetricsCalculator.calculate_recall(tp=80, fn=20)
        assert recall == 0.8

    def test_calculate_recall_zero_denominator(self):
        """Test recall calculation when denominator would be zero"""
        recall = MetricsCalculator.calculate_recall(tp=0, fn=0)
        assert recall == 0.0

    def test_calculate_recall_zero_tp(self):
        """Test recall calculation with zero true positives"""
        recall = MetricsCalculator.calculate_recall(tp=0, fn=10)
        assert recall == 0.0

    def test_calculate_recall_invalid_type(self):
        """Test recall calculation with invalid input types"""
        recall = MetricsCalculator.calculate_recall(tp=-10, fn=-20)
        assert recall == 0.0

    def test_calculate_metric_invalid(self):
        """Test invalid metric type"""
        metrics = InputDataType(
            threshold=0.5,
            true_positives=80,
            true_negatives=80,
            false_positives=20,
            false_negatives=20
        )
        with pytest.raises(ValueError, match="Invalid metric type"):
            MetricsCalculator.calculate_metric(metrics, "invalid_metric")

# ThresholdOptimizer Tests
class TestThresholdOptimizer:
    def test_init_empty_list(self):
        """Test initialization with empty metrics list"""
        with pytest.raises(ValueError, match="Metrics list cannot be empty"):
            ThresholdOptimizer([])

    def test_find_best_threshold_normal(self, metrics_list):
        """Test finding best threshold under normal conditions"""
        optimizer = ThresholdOptimizer(metrics_list, MetricType.RECALL)
        with patch.object(MetricsCalculator, 'calculate_metric') as mock_calc:
            mock_calc.side_effect = [0.9, 0.85, 0.8]  # Values for each threshold
            result = optimizer.find_best_threshold(min_threshold=0.8)
            assert result == 0.7  # Should return highest threshold meeting criteria

    def test_find_best_threshold_none_valid(self, metrics_list):
        """Test when no thresholds meet the minimum requirement"""
        optimizer = ThresholdOptimizer(metrics_list, MetricType.RECALL)
        with patch.object(MetricsCalculator, 'calculate_metric') as mock_calc:
            mock_calc.return_value = 0.7  # All thresholds below minimum
            result = optimizer.find_best_threshold(min_threshold=0.9)
            assert result is None

    def test_find_best_threshold_invalid_min(self, metrics_list):
        """Test with invalid min_threshold values"""
        optimizer = ThresholdOptimizer(metrics_list)
        with pytest.raises(ValueError, match="min_threshold must be between 0 and 1"):
            optimizer.find_best_threshold(min_threshold=1.5)
        with pytest.raises(ValueError, match="min_threshold must be between 0 and 1"):
            optimizer.find_best_threshold(min_threshold=-0.1)

    def test_find_best_threshold_edge_cases(self, metrics_list):
        """Test edge cases for threshold values"""
        optimizer = ThresholdOptimizer(metrics_list)
        # Test with min_threshold = 0
        with patch.object(MetricsCalculator, 'calculate_metric') as mock_calc:
            mock_calc.return_value = 0.1
            result = optimizer.find_best_threshold(min_threshold=0)
            assert result == 0.7  # Should return highest threshold

        # Test with min_threshold = 1
        with patch.object(MetricsCalculator, 'calculate_metric') as mock_calc:
            mock_calc.return_value = 1.0
            result = optimizer.find_best_threshold(min_threshold=1)
            assert result == 0.7  # Should return highest threshold meeting criteria

# Integration Tests
def test_end_to_end_optimization(metrics_list):
    """Test the complete workflow of threshold optimization"""
    optimizer = ThresholdOptimizer(metrics_list, MetricType.RECALL)
    best_threshold = optimizer.find_best_threshold(min_threshold=0.9)
    assert isinstance(best_threshold, (float, type(None)))
    if best_threshold is not None:
        assert 0 <= best_threshold <= 1