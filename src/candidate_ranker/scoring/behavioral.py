import numpy as np

from candidate_ranker.models import Candidate
from candidate_ranker.scoring import BaseScorer


class BehavioralScorer(BaseScorer):
    """Platform activity, OSS contributions, leadership, speaking, collaboration."""

    def score(self, candidate: Candidate, candidate_embedding: np.ndarray) -> float:
        signals = candidate.behavioral_signals
        score = 0.0

        if signals.open_source_contributions > 0:
            score += min(signals.open_source_contributions / 20.0, 0.20)

        activity = signals.platform_activity_level.lower()
        if activity == "high":
            score += 0.20
        elif activity == "medium":
            score += 0.10

        if signals.leadership_experience:
            score += 0.20

        if signals.publications > 0:
            score += min(signals.publications / 5.0, 0.10)

        if signals.speaking_engagements > 0:
            score += min(signals.speaking_engagements / 5.0, 0.10)

        if signals.collaboration_score > 0.7:
            score += 0.20

        return min(score, 1.0)
