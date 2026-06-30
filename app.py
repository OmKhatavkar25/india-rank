"""Streamlit sandbox for India Runs — Candidate Ranker demo."""

from __future__ import annotations

import sys
import time
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

st.set_page_config(page_title="India Runs — Candidate Ranker", layout="wide")
st.title("India Runs — Candidate Ranker")
st.markdown("**Senior AI Engineer — Founding Team @ Redrob AI**")

uploaded = st.file_uploader("Upload candidates.jsonl", type=["jsonl"])
sample_size = st.slider("Candidates to rank", 100, 2000, 500, help="Process a subset for demo speed")

if uploaded:
    with st.spinner("Ranking candidates..."):
        t0 = time.time()
        tmp = Path("_uploaded_candidates.jsonl")
        tmp.write_bytes(uploaded.read())

        from candidate_ranker.loader import load_candidates
        from candidate_ranker.jd_features import extract_features
        from candidate_ranker.jd_scoring import score_candidate, generate_reasoning
        from candidate_ranker.semantic import compute_semantic_scores

        candidates = load_candidates(tmp)[:sample_size]
        t1 = time.time()

        cache_path = Path("candidate_embeddings.npy")
        semantic_scores = compute_semantic_scores(candidates, cache_path)
        t2 = time.time()

        scored = []
        for c in candidates:
            f = extract_features(c)
            f["semantic_score"] = semantic_scores.get(c.candidate_id, 0.0)
            s = score_candidate(f)
            scored.append((s, c.candidate_id, f, c))

        scored.sort(key=lambda x: (-x[0], x[1]))
        t3 = time.time()

        tmp.unlink(missing_ok=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Candidates", len(scored))
    col2.metric("Load time", f"{t1-t0:.1f}s")
    col3.metric("Semantic", f"{t2-t1:.1f}s")
    col4.metric("Scoring", f"{t3-t2:.1f}s")

    rows = []
    for i, (s, cid, f, c) in enumerate(scored[:20]):
        reasoning = generate_reasoning(cid, f, round(s, 4), i + 1, c)
        rows.append({
            "Rank": i + 1,
            "Candidate": cid,
            "Score": f"{s:.4f}",
            "Reasoning": reasoning,
        })

    st.subheader("Top 20")
    st.dataframe(rows, use_container_width=True, hide_index=True)

    with st.expander("Full top-100"):
        all_rows = []
        for i, (s, cid, f, c) in enumerate(scored[:100]):
            reasoning = generate_reasoning(cid, f, round(s, 4), i + 1, c)
            all_rows.append({"Rank": i + 1, "Candidate": cid, "Score": f"{s:.4f}", "Reasoning": reasoning})
        st.dataframe(all_rows, use_container_width=True, hide_index=True)

else:
    st.info("Upload a candidates.jsonl file to start ranking.")
    st.markdown("""
    **To extract a sample from your full dataset:**
    ```bash
    head -n 500 candidates.jsonl > sample_candidates.jsonl
    ```
    """)
