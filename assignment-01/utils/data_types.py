from pydantic import BaseModel, Field
from enum import Enum

class MetricType(str, Enum):
    """Supported metric types for threshold optimization."""
    RECALL = "recall"
    # PRECISION = "precision"
    # F1 = "f1"
    # ACCURACY = "accuracy"

class InputDataType(BaseModel):
    """Data model for storing classification metrics at a specific threshold."""
    threshold: float = Field(ge=0.0, le=1.0)
    true_positives: int = Field(ge=0)
    true_negatives: int = Field(ge=0)
    false_positives: int = Field(ge=0)
    false_negatives: int = Field(ge=0)