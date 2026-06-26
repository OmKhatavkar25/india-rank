# Redrob Hackathon — Candidate Ranker

**Intelligent Candidate Discovery & Ranking Challenge**

Built manually for the **Senior AI Engineer — Founding Team** role at Redrob AI. Ranks 100K candidates and outputs a top-100 submission CSV.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Rank 100K candidates and produce submission.csv (uses TF-IDF, no network)
python rank.py

# Validate
python validate_submission.py submission.csv

# (Optional) Pre-compute transformer embeddings for better semantic matching
# Requires network on first run, ~25 min on CPU, cached for future runs
python rank.py --precompute
```

**Runtime with TF-IDF**: ~47s (5s load + 30s TF-IDF + 12s scoring). **With transformer cache**: ~25s. TF-IDF is the default and always runs; the transformer cache upgrades it when present.

## Architecture

```
candidates.jsonl ──▶ loader.py ──▶ jd_features.py ──▶ jd_scoring.py ──▶ exporter.py ──▶ submission.csv
                       │               │                    │
                    Parse JSONL      Extract features     Score & rank
                  (100K lines)     (9 dimensions)       (top 100)
                                    semantic.py ────────▶ (JD-candidate
                                    always-on              cosine similarity)
                                    TF-IDF          ──▶  Transformer cache
                                    (no-cache path)       (if .npy exists)
```

### Scoring Dimensions

| Dimension | Weight | What it measures |
|-----------|--------|------------------|
| Semantic Matching | 25% | Cosine similarity between JD and candidate profile via Sentence Transformer (all-MiniLM-L6-v2) |
| ML/AI Experience | 18% | Has the candidate held ML/AI roles? Do they have retrieval/ranking/embedding experience? |
| Skill Relevance | 12% | JD-relevant skills: embeddings, vector DBs, evaluation, fine-tuning, Python, etc. |
| Product Company | 10% | Product company background vs consulting-only (explicitly penalized by the JD) |
| Startup Experience | 10% | Startup/early-stage background (company size 1-50, founder titles) — Founding Team fit |
| Behavioral Signals | 10% | Response rate, recency, notice period, profile views, GitHub activity |
| Career Stability | 6% | Not a title-chaser; average tenure > 18 months |
| Education & Location | 5% | Education tier, relevant field, Pune/Noida/other Indian city |
| Experience Years | 4% | Sweet spot: 5–9 years; penalty outside range |

### Key Design Decisions

1. **No simple keyword counting.** The JD explicitly warns: *"The right answer is not 'find candidates whose skills section contains the most AI keywords.'"* The ranker evaluates career history for actual production ML/AI roles at product companies.

2. **Semantic JD-candidate matching (strongest signal at 25%) — always on.** Every ranking run computes TF-IDF cosine similarity between the JD and each candidate's full profile (headline + summary + skills + **career descriptions**). If a transformer embedding cache exists, it upgrades to sentence-transformer all-MiniLM-L6-v2 embeddings. Never falls back to `semantic_score = 0`.

3. **Career descriptions included in semantic matching.** The candidate text fed to TF-IDF/transformer includes up to 5 most-recent career descriptions. A "Software Engineer" at Google whose description says "designed and deployed embedding-based retrieval serving 10M users" will semantically match the JD even though their title isn't ML-tagged.

4. **Description-based ML months.** When a career entry's description contains ML evidence (recommendation, ranking, LLM, training models, etc.), the months count toward `total_relevant_months` even for non-ML titles. No more "0yr ML/AI" for engineers who built ML systems but had generic titles.

5. **Consulting penalty.** Candidates whose entire career is at services firms (TCS, Infosys, Wipro, Accenture, etc.) are down-weighted per the JD's explicit disqualifier.

6. **Honeypot resistance.** Skills with "expert" proficiency but <6 months duration, or 20+ skills with <6 months average duration, are flagged and penalized.

7. **Behavioral modifier.** A perfect-on-paper candidate with low response rate, long inactivity, or long notice period is down-weighted.

8. **Self-taught friendly education.** Candidates with no education entries get a neutral score (0.5) instead of a low "unknown" tier. The ranking doesn't penalize the absence of credentials.

9. **Early-career job-hopping tolerance.** Job-hopping and short-tenure penalties only apply after 3+ years of experience. Early-career exploration is not penalized.

10. **Semiconductor & hardware companies classified as product.** Companies like NVIDIA, Intel, AMD are properly classified as product companies for the product experience score.

## Output Format

`candidate_id,rank,score,reasoning` — exactly 100 rows, validated by `validate_submission.py`.

Example:
```
candidate_id,rank,score,reasoning
CAND_0071974,1,0.8004,"Senior AI Engineer @ Netflix | ex: Meta, Mad Street Den | 7.7yr ML/AI + retrieval/ranking + prod ML | LoRA, Weaviate, PEFT | NIT Warangal | 76% response"
```

## Project Structure

```
rank.py                          Entry point
src/candidate_ranker/
  loader.py                      JSONL parser
  redrob_models.py               Candidate data models
  jd_features.py                 Feature extraction (30+ features)
  jd_scoring.py                  Scoring engine + reasoning
  exporter.py                    CSV exporter
validate_submission.py           Hackathon validation gate
```
