from __future__ import annotations

import re
from datetime import datetime, date
from candidate_ranker.redrob_models import Candidate

CONSULTING_FIRMS = frozenset({
    "tcs", "infosys", "wipro", "accenture", "cognizant", "capgemini",
    "hcl", "tech mahindra", "ltimindtree", "mindtree", "mphasis",
    "hexaware", "cyient", "persistent systems", "atos", "ibm services",
})

ML_AI_TITLES = frozenset({
    "machine learning engineer", "ml engineer", "ai engineer",
    "ai/ml engineer", "data scientist", "research engineer",
    "applied scientist", "applied researcher", "deep learning engineer",
    "nlp engineer", "recommendation engineer", "search engineer",
    "ranking engineer", "computer vision engineer",
    "data engineer", "ml platform engineer", "mlops engineer",
    "inference engineer", "llm engineer", "generative ai engineer",
})

JD_CORE_SKILLS = frozenset({
    "embeddings", "retrieval", "ranking", "vector database",
    "vector search", "hybrid search", "pinecone", "weaviate",
    "qdrant", "milvus", "opensearch", "elasticsearch", "faiss",
    "sentence-transformers", "bge", "e5", "evaluation",
    "ndcg", "mrr", "map", "fine-tuning", "lora", "qlora", "peft",
    "llm", "large language model", "python", "production ml",
    "mlops",
})

JD_SECONDARY_SKILLS = frozenset({
    "learning-to-rank", "xgboost", "gradient boosting",
    "distributed systems", "inference optimization",
    "recommendation system", "search system", "bm25",
    "sparse retrieval", "dense retrieval", "a/b testing",
    "experimentation", "pytorch", "tensorflow",
    "nlp", "natural language processing", "information retrieval",
    "reranking", "two-tower", "cross-encoder", "bi-encoder",
})

JD_TERTIARY_SKILLS = frozenset({
    "kubernetes", "docker", "kafka", "spark", "sql",
    "ci/cd", "aws", "gcp", "azure", "graphql", "rest api",
    "redis", "postgresql", "mongodb", "airflow",
})

JD_BLACKLIST_SKILLS = frozenset({
    "langchain", "photoshop", "illustrator", "sales",
    "marketing", "accounting", "customer support",
    "content writing", "seo", "powerpoint", "excel",
})

PRODUCT_COMPANY_INDUSTRIES = frozenset({
    "software", "internet", "saas", "technology", "fintech",
    "healthtech", "edtech", "e-commerce", "marketplace",
    "social media", "gaming", "transportation", "conglomerate",
    "semiconductor", "hardware", "electronics",
})


def _normalize(text: str) -> str:
    return text.lower().strip()


def _extract_role_keywords(candidate: Candidate) -> dict:
    ml_title_count = 0
    total_roles = len(candidate.career_history)
    current_is_ml = False
    has_production_ml = False
    has_retrieval_exp = False
    avg_tenure_months = 0.0
    shortest_tenure_months = float("inf")
    job_hop_count = 0
    consulting_role_count = 0
    product_role_count = 0
    total_relevant_months = 0
    startup_role_count = 0
    current_is_startup = False

    tenures = []
    current_title_lower = _normalize(candidate.profile.current_title)

    if current_title_lower in ML_AI_TITLES or any(
        t in current_title_lower for t in ["machine learning", "ml engineer", "ai engineer",
                                            "data scientist", "research engineer", "applied scientist"]
    ):
        current_is_ml = True

    for entry in candidate.career_history:
        title_lower = _normalize(entry.title)
        company_lower = _normalize(entry.company)
        desc_lower = _normalize(entry.description)
        industry_lower = _normalize(entry.industry)

        is_ml = title_lower in ML_AI_TITLES or any(
            t in title_lower for t in ["machine learning", "ml engineer", "ai", "data science",
                                        "research", "applied", "recommendation", "search",
                                        "ranking", "retrieval", "nlp", "deep learning"]
        )
        if is_ml:
            ml_title_count += 1
            total_relevant_months += entry.duration_months
        elif re.search(
            r"machine learning|deep learning|nlp|recommendation|ranking|retrieval|"
            r"embedding|vector search|fine.tuning|llm|rag|"
            r"production.*(model|ml|ai)|deploy.*(model|ml|ai)|"
            r"trained.*(model|algorithm)|built.*(model|recommendation|ranking|search)",
            desc_lower,
        ):
            total_relevant_months += entry.duration_months

        if re.search(r"production|deploy|shipped|launched|live|prod", desc_lower):
            has_production_ml = True

        if re.search(r"embedding|retrieval|ranking|vector|search|recommendation|ndcg|mrr|map|relevance",
                     desc_lower):
            has_retrieval_exp = True

        if entry.duration_months > 0:
            tenures.append(entry.duration_months)
            if entry.duration_months < 12:
                job_hop_count += 1

        if company_lower in CONSULTING_FIRMS:
            consulting_role_count += 1
        elif industry_lower in PRODUCT_COMPANY_INDUSTRIES or (
            entry.company_size in ("11-50", "51-200", "201-500", "501-1000")
            and company_lower not in CONSULTING_FIRMS
        ):
            product_role_count += 1

        if (
            entry.company_size in ("1-10", "11-50")
            and company_lower not in CONSULTING_FIRMS
        ) or any(t in title_lower for t in [
            "co-founder", "founder", "founding engineer",
            "founding software engineer", "founding ml engineer",
            "early engineer",
        ]):
            startup_role_count += 1
            if entry.is_current:
                current_is_startup = True

    if tenures:
        avg_tenure_months = sum(tenures) / len(tenures)
        shortest_tenure_months = min(tenures)

    return {
        "ml_title_count": ml_title_count,
        "total_roles": total_roles,
        "current_is_ml": current_is_ml,
        "has_production_ml": has_production_ml,
        "has_retrieval_exp": has_retrieval_exp,
        "avg_tenure_months": avg_tenure_months,
        "shortest_tenure_months": shortest_tenure_months,
        "job_hop_count": job_hop_count,
        "consulting_role_count": consulting_role_count,
        "product_role_count": product_role_count,
        "total_relevant_months": total_relevant_months,
        "startup_role_count": startup_role_count,
        "current_is_startup": current_is_startup,
    }


def _extract_skill_features(candidate: Candidate) -> dict:
    core_match = 0
    secondary_match = 0
    tertiary_match = 0
    blacklist_match = 0
    skill_quality_score = 0.0
    total_skills = len(candidate.skills)
    suspicious_skills = 0
    total_endorsements = 0

    proficiency_weight = {"beginner": 0.3, "intermediate": 0.6, "advanced": 0.85, "expert": 1.0}

    for skill in candidate.skills:
        name_lower = _normalize(skill.name)
        prof_weight = proficiency_weight.get(skill.proficiency, 0.5)
        endorsements = skill.endorsements
        duration = skill.duration_months
        total_endorsements += endorsements

        quality = prof_weight * min(1.0, duration / 36.0) * min(1.0, endorsements / 20.0)

        if name_lower in JD_CORE_SKILLS:
            core_match += 1
            skill_quality_score += quality * 3
        elif name_lower in JD_SECONDARY_SKILLS:
            secondary_match += 1
            skill_quality_score += quality * 2
        elif name_lower in JD_TERTIARY_SKILLS:
            tertiary_match += 1
            skill_quality_score += quality * 1
        elif name_lower in JD_BLACKLIST_SKILLS:
            blacklist_match += 1
            skill_quality_score -= quality * 0.5

        if skill.proficiency == "expert" and skill.duration_months < 6:
            suspicious_skills += 1
        if skill.proficiency == "advanced" and skill.endorsements > 50 and skill.duration_months < 12:
            suspicious_skills += 1

    return {
        "core_skill_count": core_match,
        "secondary_skill_count": secondary_match,
        "tertiary_skill_count": tertiary_match,
        "blacklist_skill_count": blacklist_match,
        "skill_quality_score": max(0, skill_quality_score),
        "total_skills": total_skills,
        "suspicious_skills": suspicious_skills,
        "total_endorsements": total_endorsements,
    }


def _extract_behavioral_features(candidate: Candidate) -> dict:
    rs = candidate.redrob_signals
    today = date(2026, 6, 20)

    days_since_active = 999
    if rs.last_active_date:
        try:
            last_active = datetime.strptime(rs.last_active_date, "%Y-%m-%d").date()
            days_since_active = (today - last_active).days
        except (ValueError, TypeError):
            pass

    return {
        "profile_completeness": rs.profile_completeness_score / 100.0,
        "recruiter_response_rate": rs.recruiter_response_rate,
        "days_since_active": max(0, days_since_active),
        "open_to_work": 1.0 if rs.open_to_work_flag else 0.0,
        "search_appearance": rs.search_appearance_30d,
        "saved_by_recruiters": rs.saved_by_recruiters_30d,
        "interview_completion_rate": rs.interview_completion_rate,
        "github_activity_score": max(0, rs.github_activity_score) / 100.0 if rs.github_activity_score >= 0 else 0.0,
        "notice_period_days": rs.notice_period_days,
        "willing_to_relocate": 1.0 if rs.willing_to_relocate else 0.0,
        "connection_count": rs.connection_count,
        "application_demand": rs.profile_views_received_30d + rs.saved_by_recruiters_30d * 10,
    }


def _extract_education_features(candidate: Candidate) -> dict:
    tier_score_map = {"tier_1": 1.0, "tier_2": 0.8, "tier_3": 0.5, "tier_4": 0.3, "unknown": 0.2}
    relevant_fields = frozenset({
        "computer science", "computer engineering", "data science",
        "artificial intelligence", "machine learning", "mathematics",
        "statistics", "information technology", "electrical engineering",
        "electronics", "software engineering",
    })

    best_tier = 0.0
    has_relevant_field = False

    for edu in candidate.education:
        tier = tier_score_map.get(edu.tier, 0.2)
        if tier > best_tier:
            best_tier = tier
        if _normalize(edu.field_of_study) in relevant_fields:
            has_relevant_field = True

    return {
        "education_tier_score": best_tier,
        "has_relevant_field": 1.0 if has_relevant_field else 0.0,
    }


def _extract_summary_signals(candidate: Candidate) -> dict:
    headline = _normalize(candidate.profile.headline)
    summary = _normalize(candidate.profile.summary)
    combined = f"{headline} {summary}"

    ml_keywords = [
        "machine learning", "deep learning", "nlp", "natural language processing",
        "recommendation system", "recommendation engine", "ranking algorithm",
        "information retrieval", "search algorithm", "neural network",
        "transformer", "embedding", "vector database", "vector search",
        "trained model", "built model", "deployed model", "production model",
        "a/b testing", "experimentation", "data science",
        "llm", "large language model", "fine-tuning", "pytorch", "tensorflow",
        "xgboost", "gradient boosting", "retrieval augmented generation", "rag",
    ]

    startup_keywords = [
        "startup", "early-stage", "early stage", "0-to-1", "0 to 1",
        "founding team", "first engineer", "seed stage", "series a",
        "built from scratch", "greenfield",
    ]

    non_ml_domains = [
        "marketing", "sales", "accounting", "hr", "recruitment",
        "customer support", "content writing", "administration",
        "mechanical engineering", "civil engineering",
    ]

    ml_mentions = sum(1 for kw in ml_keywords if kw in combined)
    startup_mentions = sum(1 for kw in startup_keywords if kw in combined)
    non_ml_mentions = sum(1 for kw in non_ml_domains if kw in combined)

    return {
        "summary_ml_mentions": min(ml_mentions, 10),
        "summary_startup_mentions": min(startup_mentions, 5),
        "summary_non_ml_mentions": non_ml_mentions,
    }


def _check_honeypot(candidate: Candidate) -> float:
    penalty = 0.0

    expert_beginner_skills = sum(
        1 for s in candidate.skills
        if s.proficiency in ("advanced", "expert") and s.duration_months < 6
    )
    if expert_beginner_skills >= 3:
        penalty += 0.2

    if len(candidate.skills) >= 20:
        avg_duration = sum(s.duration_months for s in candidate.skills) / len(candidate.skills)
        if avg_duration < 6:
            penalty += 0.3

    all_consulting = all(
        _normalize(e.company) in CONSULTING_FIRMS for e in candidate.career_history
    )
    if all_consulting and candidate.profile.years_of_experience > 8:
        penalty += 0.1

    return penalty


def extract_features(candidate: Candidate) -> dict:
    role = _extract_role_keywords(candidate)
    skills = _extract_skill_features(candidate)
    behavioral = _extract_behavioral_features(candidate)
    education = _extract_education_features(candidate)
    summary = _extract_summary_signals(candidate)
    honeypot = _check_honeypot(candidate)

    return {
        **role,
        **skills,
        **behavioral,
        **education,
        **summary,
        "honeypot_penalty": honeypot,
        "years_exp": candidate.profile.years_of_experience,
        "location": candidate.profile.location,
        "country": candidate.profile.country,
        "current_title": candidate.profile.current_title,
        "current_company": candidate.profile.current_company,
        "current_industry": candidate.profile.current_industry,
    }
