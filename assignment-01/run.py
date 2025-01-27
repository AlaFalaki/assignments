from utils.data_types import InputDataType, MetricType
from src.optimizer import ThresholdOptimizer
import logging

logging.basicConfig(level=logging.INFO) # Or, logging.DEBUG to get all the logs

def main():
    # Sample Data
    data = [
        InputDataType(
            threshold=0.3,
            true_positives=90,
            true_negatives=70,
            false_positives=30,
            false_negatives=10
        ),
        InputDataType(
            threshold=0.5,
            true_positives=80,
            true_negatives=85,
            false_positives=15,
            false_negatives=20
        ),
        InputDataType(
            threshold=0.7,
            true_positives=70,
            true_negatives=90,
            false_positives=10,
            false_negatives=30
        ),
        InputDataType(
            threshold=0.9,
            true_positives=50,
            true_negatives=95,
            false_positives=5,
            false_negatives=50
        )
    ]

    # Initialize the optimizer
    optimizer = ThresholdOptimizer(data, metric_type=MetricType.RECALL)
    min_threshold = 0.9
    

    best_threshold = optimizer.find_best_threshold(min_threshold=min_threshold)
    if best_threshold is not None:
        print(f"Best threshold found: {best_threshold}")
    else:
        print(f"\nNo threshold found meeting minimum recall of {min_threshold}")

if __name__ == "__main__":
    main()