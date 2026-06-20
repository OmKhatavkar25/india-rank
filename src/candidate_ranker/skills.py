"""Skill taxonomy with normalization and extraction."""

from __future__ import annotations

import re


class SkillEntry:
    __slots__ = ("canonical", "category", "aliases")

    def __init__(self, canonical: str, category: str, aliases: list[str]) -> None:
        self.canonical = canonical
        self.category = category
        self.aliases = aliases


SKILL_TAXONOMY: list[SkillEntry] = [
    # Programming Languages
    SkillEntry("python", "programming_language", ["python3", "py"]),
    SkillEntry("javascript", "programming_language", ["js", "ecmascript", "es6"]),
    SkillEntry("typescript", "programming_language", ["ts"]),
    SkillEntry("java", "programming_language", []),
    SkillEntry("go", "programming_language", ["golang"]),
    SkillEntry("rust", "programming_language", []),
    SkillEntry("c++", "programming_language", ["cpp", "cplusplus"]),
    SkillEntry("c#", "programming_language", ["csharp"]),
    SkillEntry("kotlin", "programming_language", []),
    SkillEntry("swift", "programming_language", []),
    SkillEntry("ruby", "programming_language", []),
    SkillEntry("scala", "programming_language", []),
    SkillEntry("r", "programming_language", []),
    # Databases
    SkillEntry("sql", "database", ["mysql", "postgresql", "postgres", "sqlite"]),
    SkillEntry("nosql", "database", ["mongodb", "cassandra", "dynamodb", "firestore", "couchdb"]),
    SkillEntry("redis", "database", []),
    SkillEntry("elasticsearch", "database", ["es"]),
    # Cloud
    SkillEntry("aws", "cloud", ["amazon web services", "ec2", "s3", "lambda"]),
    SkillEntry("gcp", "cloud", ["google cloud platform", "gcs", "bigquery"]),
    SkillEntry("azure", "cloud", ["microsoft azure"]),
    # DevOps & Infrastructure
    SkillEntry("docker", "devops", ["containerization", "container"]),
    SkillEntry("kubernetes", "devops", ["k8s"]),
    SkillEntry("terraform", "devops", ["iac"]),
    SkillEntry("ansible", "devops", []),
    SkillEntry("ci/cd", "devops", ["jenkins", "github actions", "gitlab ci", "circleci"]),
    SkillEntry("prometheus", "devops", []),
    SkillEntry("grafana", "devops", []),
    # Backend Frameworks
    SkillEntry("nodejs", "backend", ["node", "node.js"]),
    SkillEntry("django", "backend", []),
    SkillEntry("flask", "backend", []),
    SkillEntry("fastapi", "backend", []),
    SkillEntry("spring", "backend", ["spring boot"]),
    SkillEntry("express", "backend", ["expressjs"]),
    SkillEntry("graphql", "backend", []),
    SkillEntry("rest", "backend", ["restful", "rest api"]),
    SkillEntry("grpc", "backend", []),
    SkillEntry("kafka", "backend", ["apache kafka"]),
    # Frontend
    SkillEntry("react", "frontend", ["reactjs", "react.js"]),
    SkillEntry("angular", "frontend", ["angularjs", "angular.js"]),
    SkillEntry("vue", "frontend", ["vuejs", "vue.js"]),
    SkillEntry("nextjs", "frontend", ["next.js"]),
    SkillEntry("css", "frontend", ["css3"]),
    # ML & Data Science
    SkillEntry("tensorflow", "ml", ["tf"]),
    SkillEntry("pytorch", "ml", []),
    SkillEntry("scikit-learn", "ml", ["sklearn"]),
    SkillEntry("machine learning", "ml", ["ml"]),
    SkillEntry("deep learning", "ml", ["dl", "neural networks"]),
    SkillEntry("nlp", "ml", ["natural language processing"]),
    SkillEntry("computer vision", "ml", ["cv"]),
    SkillEntry("llm", "ml", ["large language model", "gpt", "generative ai", "transformer"]),
    SkillEntry("mlops", "ml", []),
    # Data Engineering
    SkillEntry("pandas", "data", []),
    SkillEntry("numpy", "data", []),
    SkillEntry("spark", "data", ["apache spark", "pyspark"]),
    SkillEntry("airflow", "data", ["apache airflow"]),
    SkillEntry("snowflake", "data", []),
    SkillEntry("dbt", "data", []),
    # Tools
    SkillEntry("git", "tools", ["github", "gitlab", "bitbucket", "version control"]),
    # Management & Soft Skills
    SkillEntry("product management", "management", ["pm"]),
    SkillEntry("agile", "management", ["scrum", "kanban"]),
    SkillEntry("leadership", "soft_skill", ["team lead", "tech lead", "engineering manager"]),
    SkillEntry("communication", "soft_skill", ["written communication", "verbal communication"]),
    SkillEntry("project management", "management", []),
]


SKILL_MAP: dict[str, SkillEntry] = {}
for entry in SKILL_TAXONOMY:
    SKILL_MAP[entry.canonical] = entry
    for alias in entry.aliases:
        SKILL_MAP[alias] = entry


def normalize_skill(raw: str) -> str | None:
    """Return canonical skill name or None if not in taxonomy."""
    key = raw.strip().lower()
    entry = SKILL_MAP.get(key)
    return entry.canonical if entry else None


def extract_skills(text: str) -> list[str]:
    """Extract canonical skill names found in text."""
    text_lower = text.lower()
    found: set[str] = set()

    for entry in SKILL_TAXONOMY:
        # Check canonical
        pattern = re.compile(rf"\b{re.escape(entry.canonical)}\b", re.IGNORECASE)
        if pattern.search(text_lower):
            found.add(entry.canonical)
            continue
        # Check aliases
        for alias in entry.aliases:
            if alias in text_lower:
                found.add(entry.canonical)
                break

    return sorted(found)


def skill_coverage(jd_skills: set[str], candidate_skills: set[str]) -> float:
    """Return fraction of JD skills present in candidate skills."""
    if not jd_skills:
        return 0.5
    return len(jd_skills & candidate_skills) / len(jd_skills)
