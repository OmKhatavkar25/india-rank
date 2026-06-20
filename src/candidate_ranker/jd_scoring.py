from __future__ import annotations

import re
from candidate_ranker.redrob_models import Candidate, Skill

JD_CORE_SKILLS = frozenset({
    "embeddings", "retrieval", "ranking", "vector database",
    "vector search", "hybrid search", "pinecone", "weaviate",
    "qdrant", "milvus", "opensearch", "elasticsearch", "faiss",
    "sentence-transformers", "bge", "e5", "evaluation",
    "ndcg", "mrr", "map", "fine-tuning", "lora", "qlora", "peft",
    "llm", "large language model", "python", "production ml",
    "mlops",
})

PROFICIENCY_LABEL = {"beginner": "B", "intermediate": "I", "advanced": "A", "expert": "E"}


def score_candidate(features: dict) -> float:
    """Compute overall fit score for Senior AI Engineer - Founding Team role."""
    s = 0.0
    debug = {}

    # 1. ML/AI Engineering Experience (weight: 0.30)
    ml_score = _score_ml_experience(features)
    s += ml_score * 0.30
    debug["ml_experience"] = round(ml_score, 4)

    # 2. Product Company Experience (weight: 0.20)
    product_score = _score_product_experience(features)
    s += product_score * 0.20
    debug["product_experience"] = round(product_score, 4)

    # 3. Skill Relevance (weight: 0.20)
    skill_score = _score_skills(features)
    s += skill_score * 0.20
    debug["skills"] = round(skill_score, 4)

    # 4. Career Stability & Trajectory (weight: 0.10)
    stability_score = _score_stability(features)
    s += stability_score * 0.10
    debug["stability"] = round(stability_score, 4)

    # 5. Experience Alignment (weight: 0.05)
    exp_years_score = _score_experience_years(features)
    s += exp_years_score * 0.05
    debug["exp_years"] = round(exp_years_score, 4)

    # 6. Behavioral Signals (weight: 0.10)
    behavioral_score = _score_behavioral(features)
    s += behavioral_score * 0.10
    debug["behavioral"] = round(behavioral_score, 4)

    # 7. Education & Location (weight: 0.05)
    edu_loc_score = _score_education_location(features)
    s += edu_loc_score * 0.05
    debug["edu_location"] = round(edu_loc_score, 4)

    # Penalties
    honeypot_penalty = features.get("honeypot_penalty", 0.0)
    s = max(0.0, s - honeypot_penalty)

    return min(s, 1.0)


def _score_ml_experience(f: dict) -> float:
    score = 0.0

    has_ml_role = f.get("ml_title_count", 0) > 0
    current_is_ml = f.get("current_is_ml", False)
    retrieval_exp = f.get("has_retrieval_exp", False)
    prod_ml = f.get("has_production_ml", False)
    relevant_months = f.get("total_relevant_months", 0)

    if current_is_ml:
        score += 0.30
    elif has_ml_role:
        score += 0.20
    else:
        score += 0.05

    if retrieval_exp:
        score += 0.30
    elif has_ml_role:
        score += 0.10

    if prod_ml:
        score += 0.20

    relevant_years = relevant_months / 12.0
    if relevant_years >= 3:
        score += 0.20
    elif relevant_years >= 1:
        score += 0.10

    return min(score, 1.0)


def _score_product_experience(f: dict) -> float:
    total_roles = f.get("total_roles", 0)
    consulting = f.get("consulting_role_count", 0)
    product = f.get("product_role_count", 0)

    if total_roles == 0:
        return 0.3

    if consulting == total_roles:
        return 0.1

    if product > 0:
        ratio = product / total_roles
        return 0.3 + 0.7 * min(ratio, 1.0)

    return 0.3


def _score_skills(f: dict) -> float:
    core = f.get("core_skill_count", 0)
    secondary = f.get("secondary_skill_count", 0)
    tertiary = f.get("tertiary_skill_count", 0)
    blacklist = f.get("blacklist_skill_count", 0)
    quality = f.get("skill_quality_score", 0.0)
    total = f.get("total_skills", 0)
    suspicious = f.get("suspicious_skills", 0)

    core_score = min(core / 8.0, 1.0) * 0.50
    secondary_score = min(secondary / 10.0, 1.0) * 0.20
    tertiary_score = min(tertiary / 15.0, 1.0) * 0.10

    quality_score = min(quality / 20.0, 1.0) * 0.15

    blacklist_penalty = 0.0
    if blacklist > 0 and total > 0:
        ratio = blacklist / total
        blacklist_penalty = min(ratio, 0.5) * 0.10

    suspicious_penalty = min(suspicious * 0.05, 0.20)

    score = core_score + secondary_score + tertiary_score + quality_score
    score = max(0.0, score - blacklist_penalty - suspicious_penalty)

    return min(score, 1.0)


def _score_stability(f: dict) -> float:
    avg_tenure = f.get("avg_tenure_months", 0)
    shortest = f.get("shortest_tenure_months", float("inf"))
    job_hop_count = f.get("job_hop_count", 0)
    total_roles = f.get("total_roles", 0)

    if total_roles <= 1:
        return 0.5

    tenure_score = min(avg_tenure / 36.0, 1.0) * 0.50

    hopping_penalty = 0.0
    if total_roles > 0:
        hop_ratio = job_hop_count / total_roles
        hopping_penalty = min(hop_ratio, 1.0) * 0.30

    short_tenure_penalty = 0.0
    if shortest < 6:
        short_tenure_penalty = 0.20

    return max(0.0, 0.5 + tenure_score - hopping_penalty - short_tenure_penalty)


def _score_experience_years(f: dict) -> float:
    years = f.get("years_exp", 0)

    if 5 <= years <= 9:
        return 1.0
    elif 3 <= years < 5:
        return 0.6 + (years - 3) * 0.2
    elif 9 < years <= 12:
        return 0.8 - (years - 9) * 0.1
    elif years < 3:
        return max(0.1, years * 0.15)
    else:
        return max(0.2, 0.5 - (years - 12) * 0.05)


def _score_behavioral(f: dict) -> float:
    score = 0.0

    response_rate = f.get("recruiter_response_rate", 0)
    if response_rate > 0.7:
        score += 0.25
    elif response_rate > 0.4:
        score += 0.15
    elif response_rate > 0.1:
        score += 0.05

    days_inactive = f.get("days_since_active", 999)
    if days_inactive < 30:
        score += 0.20
    elif days_inactive < 90:
        score += 0.12
    elif days_inactive < 180:
        score += 0.05

    open_to_work = f.get("open_to_work", 0)
    score += open_to_work * 0.10

    demand = f.get("application_demand", 0)
    if demand > 100:
        score += 0.10
    elif demand > 50:
        score += 0.05

    github = f.get("github_activity_score", 0)
    if github > 0.5:
        score += 0.10
    elif github > 0.1:
        score += 0.05

    completeness = f.get("profile_completeness", 0)
    if completeness > 0.8:
        score += 0.10
    elif completeness > 0.5:
        score += 0.05

    notice = f.get("notice_period_days", 90)
    if notice <= 30:
        score += 0.10
    elif notice <= 60:
        score += 0.05

    interview_rate = f.get("interview_completion_rate", 0)
    if interview_rate > 0.8:
        score += 0.05

    return min(score, 1.0)


def _score_education_location(f: dict) -> float:
    score = 0.0

    edu_tier = f.get("education_tier_score", 0.2)
    score += edu_tier * 0.30

    has_relevant_field = f.get("has_relevant_field", 0)
    score += has_relevant_field * 0.20

    location = f.get("location", "").lower()
    country = f.get("country", "").lower()

    preferred_locations = {"pune", "noida", "mumbai", "delhi", "gurgaon", "hyderabad", "bengaluru", "bangalore", "chennai"}
    if any(city in location for city in preferred_locations):
        score += 0.30
    elif country == "india":
        score += 0.15

    willing = f.get("willing_to_relocate", 0)
    score += willing * 0.20

    return min(score, 1.0)


def _get_matched_skill_names(candidate: Candidate) -> list[str]:
    """Return names of skills that match the JD core taxonomy."""
    matched = []
    for s in candidate.skills:
        name_lower = s.name.lower().strip()
        if name_lower in JD_CORE_SKILLS:
            matched.append(s.name)
    return matched[:3]


def _prev_company_str(candidate: Candidate | None) -> str:
    """Previous company names only, up to 2."""
    if not candidate or not candidate.career_history:
        return ""
    seen = []
    for entry in candidate.career_history:
        if entry.is_current:
            continue
        co = entry.company.strip()
        if co and co not in seen:
            seen.append(co)
        if len(seen) >= 2:
            break
    return ", ".join(seen) if seen else ""


def generate_reasoning(
    candidate_id: str, features: dict, score: float, rank: int,
    candidate: Candidate | None = None,
) -> str:
    """Clean one-line summary — easy for a recruiter to scan."""

    title = features.get("current_title", "")
    company = features.get("current_company", "")
    current = f"{title} @ {company}" if title and company else title

    prev = _prev_company_str(candidate)

    relevant_exp = features.get("total_relevant_months", 0) / 12.0
    has_retrieval = features.get("has_retrieval_exp", False)
    has_prod = features.get("has_production_ml", False)
    exp = f"{relevant_exp:.1f}yr ML/AI" if relevant_exp > 0 else ""
    if has_retrieval:
        exp += " + retrieval/ranking"
    if has_prod:
        exp += " + prod ML"

    skill_names = _get_matched_skill_names(candidate) if candidate else []
    skills = ", ".join(skill_names) if skill_names else ""

    edu = ""
    if candidate and candidate.education:
        best = candidate.education[0]
        for e in candidate.education:
            if e.tier in ("tier_1",) or (e.end_year or 0) > (best.end_year or 0):
                best = e
        edu = best.institution.strip()

    rr = features.get("recruiter_response_rate", 0)
    signal = f"{rr:.0%} response" if rr >= 0.5 else ""

    loc = features.get("location", "")
    preferred = {"pune", "noida", "mumbai", "delhi", "gurgaon", "hyderabad", "bangalore"}
    city = ""
    if loc and any(c in loc.lower() for c in preferred):
        city = loc.split(",")[0].strip()

    notice = features.get("notice_period_days", 90)
    notice_str = "short notice" if notice <= 30 else ""

    # Build minimal, scannable string
    bits = [current]
    if prev:
        bits.append(f"ex: {prev}")
    if exp:
        bits.append(exp)
    if skills:
        bits.append(skills)
    if edu:
        bits.append(edu)
    tail = ", ".join(s for s in [signal, city, notice_str] if s)
    if tail:
        bits.append(tail)

    return " | ".join(bits)[:250]
