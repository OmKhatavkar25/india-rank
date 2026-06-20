#!/usr/bin/env python3
"""Redrob Hackathon — Candidate Ranker for Senior AI Engineer role.

Usage:
    python rank.py --candidates ./candidates.jsonl --out ./submission.csv
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from candidate_ranker.loader import load_candidates
from candidate_ranker.jd_features import extract_features
from candidate_ranker.jd_scoring import score_candidate, generate_reasoning
from candidate_ranker.exporter import export_submission

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)
logger = logging.getLogger("rank")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rank candidates for Senior AI Engineer role"
    )
    parser.add_argument(
        "--candidates", "-c",
        required=True,
        help="Path to candidates.jsonl (or .jsonl.gz)",
    )
    parser.add_argument(
        "--out", "-o",
        default="./submission.csv",
        help="Output CSV path (default: ./submission.csv)",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=100,
        help="Number of top candidates (default: 100)",
    )
    args = parser.parse_args()

    t0 = time.time()

    logger.info("Loading candidates from %s ...", args.candidates)
    candidates = load_candidates(args.candidates)
    t1 = time.time()
    logger.info("Loaded %d candidates in %.1fs", len(candidates), t1 - t0)

    logger.info("Extracting features and scoring ...")
    scored = []
    for idx, cand in enumerate(candidates):
        if (idx + 1) % 25000 == 0:
            logger.info("  Processed %d / %d", idx + 1, len(candidates))
        features = extract_features(cand)
        score = score_candidate(features)
        scored.append((score, cand.candidate_id, features))
    t2 = time.time()
    logger.info("Scored %d candidates in %.1fs", len(scored), t2 - t1)

    # Sort: descending score, then ascending candidate_id (tie-break)
    scored.sort(key=lambda x: (-x[0], x[1]))

    top_n = min(args.top_n, len(scored))
    ranked = []
    for rank_idx in range(top_n):
        score, cid, features = scored[rank_idx]
        rounded_score = round(score, 4)
        reasoning = generate_reasoning(cid, features, rounded_score, rank_idx + 1)
        ranked.append({
            "candidate_id": cid,
            "rank": rank_idx + 1,
            "score": rounded_score,
            "reasoning": reasoning,
        })

    # Ensure non-increasing scores; stable tie-break by candidate_id ascending
    ranked.sort(key=lambda x: (-x["score"], x["candidate_id"]))
    for i, row in enumerate(ranked):
        row["rank"] = i + 1
        if i > 0 and row["score"] > ranked[i - 1]["score"]:
            row["score"] = ranked[i - 1]["score"]

    out_path = export_submission(ranked, args.out)
    t3 = time.time()
    logger.info(
        "Wrote %d ranked candidates to %s in %.1fs (total: %.1fs)",
        len(ranked), out_path, t3 - t2, t3 - t0,
    )

    if ranked:
        logger.info("Top 5:")
        for r in ranked[:5]:
            logger.info("  #%d  %s  %.4f  %s", r["rank"], r["candidate_id"], r["score"], r["reasoning"][:80])


if __name__ == "__main__":
    main()
