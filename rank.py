#!/usr/bin/env python3
"""Redrob Hackathon — Candidate Ranker for Senior AI Engineer role.

Usage:
    python rank.py                         # default: ./candidates.jsonl -> ./submission.csv
    python rank.py --precompute            # pre-compute semantic embeddings (one-time)
    python rank.py -c sample_candidates.jsonl -o submission.csv
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

EMBEDDING_CACHE = Path("./candidate_embeddings.npy")


def _compute_semantic_scores(candidates, cache_path: Path) -> dict:
    from candidate_ranker.semantic import compute_semantic_scores
    return compute_semantic_scores(candidates, cache_path)


def _precompute(candidates, cache_path: Path) -> None:
    from candidate_ranker.semantic import precompute_embeddings
    precompute_embeddings(candidates, cache_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rank candidates for Senior AI Engineer role"
    )
    parser.add_argument(
        "--candidates", "-c",
        default="./candidates.jsonl",
        help="Path to candidates.jsonl (default: ./candidates.jsonl)",
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
    parser.add_argument(
        "--precompute",
        action="store_true",
        help="Pre-compute semantic embeddings and cache them (one-time, requires network)",
    )
    args = parser.parse_args()

    t0 = time.time()

    logger.info("Loading candidates from %s ...", args.candidates)
    candidates = load_candidates(args.candidates)
    t1 = time.time()
    logger.info("Loaded %d candidates in %.1fs", len(candidates), t1 - t0)

    cache_path = args.out.parent / "candidate_embeddings.npy" if args.out != "./submission.csv" else EMBEDDING_CACHE

    if args.precompute:
        _precompute(candidates, cache_path)
        logger.info("Pre-computation done. Run without --precompute to rank.")
        return

    logger.info("Computing semantic scores ...")
    st = time.time()
    semantic_scores = _compute_semantic_scores(candidates, cache_path)
    logger.info("Semantic scores computed in %.1fs", time.time() - st)

    logger.info("Extracting features and scoring ...")
    scored = []
    for idx, cand in enumerate(candidates):
        if (idx + 1) % 25000 == 0:
            logger.info("  Processed %d / %d", idx + 1, len(candidates))
        features = extract_features(cand)
        features["semantic_score"] = semantic_scores.get(cand.candidate_id, 0.0)
        score = score_candidate(features)
        scored.append((score, cand.candidate_id, features, cand))
    t2 = time.time()
    logger.info("Scored %d candidates in %.1fs", len(scored), t2 - t1)

    scored.sort(key=lambda x: (-x[0], x[1]))

    top_n = min(args.top_n, len(scored))
    ranked = []
    for rank_idx in range(top_n):
        score, cid, features, cand = scored[rank_idx]
        rounded_score = round(score, 4)
        reasoning = generate_reasoning(cid, features, rounded_score, rank_idx + 1, cand)
        ranked.append({
            "candidate_id": cid,
            "rank": rank_idx + 1,
            "score": rounded_score,
            "reasoning": reasoning,
        })

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
