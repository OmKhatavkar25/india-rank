# Redrob Hackathon — Candidate Ranker

**Intelligent Candidate Discovery & Ranking Challenge**

Built manually for the **Senior AI Engineer — Founding Team** role at Redrob AI. Ranks 100K candidates and outputs a top-100 submission CSV.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Rank 100K candidates and produce submission.csv
python rank.py --candidates ./candidates.jsonl --out ./submission.csv

# Validate
python validate_submission.py submission.csv
```

**Runtime**: ~12 seconds for 100K candidates on CPU (16 GB, 8 cores).

## Architecture

```
candidates.jsonl ──▶ loader.py ──▶ jd_features.py ──▶ jd_scoring.py ──▶ exporter.py ──▶ submission.csv
                       │               │                    │
                 Parse JSONL      Extract features     Score & rank
                 (100K lines)     (7 dimensions)       (top 100)
```

### Scoring Dimensions

| Dimension | Weight | What it measures |
|-----------|--------|------------------|
| ML/AI Experience | 30% | Has the candidate held ML/AI roles? Do they have retrieval/ranking/embedding experience? |
| Product Company | 20% | Product company background vs consulting-only (explicitly penalized by the JD) |
| Skill Relevance | 20% | JD-relevant skills: embeddings, vector DBs, evaluation, fine-tuning, Python, etc. |
| Career Stability | 10% | Not a title-chaser; average tenure > 18 months |
| Experience Years | 5% | Sweet spot: 5–9 years; penalty outside range |
| Behavioral Signals | 10% | Response rate, recency, notice period, profile views, GitHub activity |
| Education & Location | 5% | Education tier, relevant field, Pune/Noida/other Indian city |

### Key Design Decisions

1. **No simple keyword counting.** The JD explicitly warns: *"The right answer is not 'find candidates whose skills section contains the most AI keywords.'"* The ranker evaluates career history for actual production ML/AI roles at product companies.

2. **Retrieval/ranking experience detection.** Role descriptions are scanned for evidence of deployed ranking, retrieval, search, or recommendation systems — the core of what Redrob's Senior AI Engineer would build.

3. **Consulting penalty.** Candidates whose entire career is at services firms (TCS, Infosys, Wipro, Accenture, etc.) are down-weighted per the JD's explicit disqualifier.

4. **Honeypot resistance.** Skills with "expert" proficiency but <6 months duration, or 20+ skills with <6 months average duration, are flagged and penalized.

5. **Behavioral modifier.** A perfect-on-paper candidate with low response rate, long inactivity, or long notice period is down-weighted.

## Output Format

`candidate_id,rank,score,reasoning` — exactly 100 rows, validated by `validate_submission.py`.

Example:
```
candidate_id,rank,score,reasoning
CAND_0081846,1,0.8799,Lead AI Engineer @ Razorpay | ex: Paytm | 6.6yr ML/AI + retrieval/ranking + prod ML | Elasticsearch, Vector Search, Python | IIT Delhi | 73% response, short notice
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
submission_metadata.yaml         Team info, compute, declarations
validate_submission.py           Hackathon validation gate
```
