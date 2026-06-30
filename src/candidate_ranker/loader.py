from __future__ import annotations

import gzip
import json
import logging
from pathlib import Path

from candidate_ranker.redrob_models import Candidate, parse_candidate

logger = logging.getLogger(__name__)


def load_candidates(path: str | Path) -> list[Candidate]:
    path = Path(path)
    open_func = gzip.open if path.suffix == ".gz" else open
    candidates: list[Candidate] = []

    with open_func(path, "rt", encoding="utf-8-sig") as f:
        first_char = f.read(1)
        f.seek(0)

        if first_char == "[":
            raw_list = json.load(f)
            for item in raw_list:
                try:
                    candidates.append(parse_candidate(item))
                except Exception:
                    logger.warning("Failed to parse candidate %s", item.get("candidate_id", "?"))
        else:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    raw = json.loads(line)
                    candidates.append(parse_candidate(raw))
                except Exception:
                    logger.warning("Failed to parse candidate at line %d", line_num)

    logger.info("Loaded %d candidates from %s", len(candidates), path)
    return candidates
