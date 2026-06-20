import logging
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, field_validator


class EmbeddingConfig(BaseModel):
    model_name: str = "all-MiniLM-L6-v2"
    normalize_embeddings: bool = True
    cache_dir: str | None = None


class ScoringWeights(BaseModel):
    semantic_similarity: float = 0.35
    skill_match: float = 0.25
    experience_relevance: float = 0.20
    role_title_relevance: float = 0.10
    behavioral_signals: float = 0.10

    @field_validator("*")
    @classmethod
    def weights_sum_to_one(cls, v: float, info) -> float:
        if info.field_name == "semantic_similarity":
            return v
        return v


class PipelineConfig(BaseModel):
    top_n: int = 20
    min_score_threshold: float = 0.0


class LoggingConfig(BaseModel):
    level: str = "INFO"
    format: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    file: str | None = None


class ExportConfig(BaseModel):
    default_format: Literal["csv", "json", "both"] = "csv"
    include_strengths: bool = True
    include_concerns: bool = True


class AppConfig(BaseModel):
    embedding: EmbeddingConfig = Field(default_factory=EmbeddingConfig)
    scoring: ScoringWeights = Field(default_factory=ScoringWeights)
    pipeline: PipelineConfig = Field(default_factory=PipelineConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    export: ExportConfig = Field(default_factory=ExportConfig)


def load_config(path: str | Path | None = None) -> AppConfig:
    if path is None:
        path = Path(__file__).parent.parent.parent / "config" / "default.yaml"

    path = Path(path)
    if path.exists():
        with open(path) as f:
            raw = yaml.safe_load(f)
        return AppConfig.model_validate(raw)
    return AppConfig()


def configure_logging(cfg: LoggingConfig) -> None:
    handlers = [logging.StreamHandler()]
    if cfg.file:
        handlers.append(logging.FileHandler(cfg.file))

    logging.basicConfig(
        level=getattr(logging, cfg.level.upper(), logging.INFO),
        format=cfg.format,
        handlers=handlers,
    )
