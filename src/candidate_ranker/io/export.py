"""Export ranked candidates to CSV and JSON formats."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from candidate_ranker.models import RankedCandidate


def export_csv(ranked: list[RankedCandidate], output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Rank",
            "Candidate ID",
            "Name",
            "Overall Score",
            "Semantic Similarity",
            "Skill Match",
            "Experience Relevance",
            "Role Title Relevance",
            "Behavioral Signals",
            "Strengths",
            "Concerns",
        ])
        for rc in ranked:
            writer.writerow([
                rc.rank,
                rc.candidate_id,
                rc.name,
                f"{rc.overall_score:.2f}",
                f"{rc.semantic_similarity:.2f}",
                f"{rc.skill_match:.2f}",
                f"{rc.experience_relevance:.2f}",
                f"{rc.role_title_relevance:.2f}",
                f"{rc.behavioral_signals:.2f}",
                "; ".join(rc.strengths),
                "; ".join(rc.concerns),
            ])

    return output_path


def export_json(ranked: list[RankedCandidate], output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = [rc.to_dict() for rc in ranked]
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return output_path
