from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class Experience:
    title: str
    company: str
    duration_years: float
    description: str = ""


@dataclass
class BehavioralSignals:
    open_source_contributions: int = 0
    platform_activity_level: str = "low"
    leadership_experience: bool = False
    publications: int = 0
    speaking_engagements: int = 0
    collaboration_score: float = 0.0


@dataclass
class Candidate:
    id: str
    name: str
    summary: str
    skills: list[str] = field(default_factory=list)
    total_experience_years: float = 0.0
    seniority_level: str = "mid"
    education: list[str] = field(default_factory=list)
    experience: list[Experience] = field(default_factory=list)
    behavioral_signals: BehavioralSignals = field(default_factory=BehavioralSignals)


@dataclass
class JobDescription:
    id: str
    title: str
    description: str


@dataclass
class ScoredDimension:
    semantic_similarity: float = 0.0
    skill_match: float = 0.0
    experience_relevance: float = 0.0
    role_title_relevance: float = 0.0
    behavioral_signals: float = 0.0


@dataclass
class RankedCandidate:
    rank: int = 0
    candidate_id: str = ""
    name: str = ""
    overall_score: float = 0.0
    semantic_similarity: float = 0.0
    skill_match: float = 0.0
    experience_relevance: float = 0.0
    role_title_relevance: float = 0.0
    behavioral_signals: float = 0.0
    strengths: list[str] = field(default_factory=list)
    concerns: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


DATA_DIR = None


def set_data_dir(path: str) -> None:
    global DATA_DIR
    DATA_DIR = path
