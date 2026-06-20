"""Abstract base class for all scoring dimensions."""

from abc import ABC, abstractmethod

import numpy as np

from candidate_ranker.models import Candidate


class BaseScorer(ABC):
    """Each scorer computes a single dimension of candidate fit."""

    def __init__(self, jd_text: str, jd_embedding: np.ndarray) -> None:
        self.jd_text = jd_text
        self.jd_embedding = jd_embedding

    @abstractmethod
    def score(self, candidate: Candidate, candidate_embedding: np.ndarray) -> float:
        """Return a score in [0, 1] for this dimension."""
