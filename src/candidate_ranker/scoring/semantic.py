import numpy as np

from candidate_ranker.models import Candidate
from candidate_ranker.scoring import BaseScorer


class SemanticScorer(BaseScorer):
    """Cosine similarity between JD embedding and candidate embedding."""

    def score(self, candidate: Candidate, candidate_embedding: np.ndarray) -> float:
        return float(np.dot(self.jd_embedding, candidate_embedding))
