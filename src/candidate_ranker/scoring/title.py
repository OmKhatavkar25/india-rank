import re

import numpy as np

from candidate_ranker.models import Candidate
from candidate_ranker.scoring import BaseScorer


ROLE_KEYWORDS = [
    "engineer", "developer", "scientist", "manager", "architect",
    "analyst", "designer", "researcher", "consultant", "lead",
    "head", "director", "principal", "staff",
]


class TitleScorer(BaseScorer):
    """Checks if candidate's role titles align with JD role keywords."""

    def score(self, candidate: Candidate, candidate_embedding: np.ndarray) -> float:
        jd_keywords = self._extract_jd_role_keywords()
        if not jd_keywords:
            return 0.5

        candidate_titles = [e.title.lower() for e in candidate.experience]
        matches = sum(
            1 for title in candidate_titles
            for kw in jd_keywords
            if kw in title
        )
        return min(matches / max(len(jd_keywords), 1), 1.0)

    def _extract_jd_role_keywords(self) -> set[str]:
        jd_lower = self.jd_text.lower()
        found: set[str] = set()
        for kw in ROLE_KEYWORDS:
            if re.search(rf"\b{re.escape(kw)}\b", jd_lower):
                found.add(kw)
        return found
