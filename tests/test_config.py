"""Tests for the config module."""

from pathlib import Path

from candidate_ranker.config import AppConfig, load_config


def test_default_config_loaded() -> None:
    cfg = AppConfig()
    assert cfg.embedding.model_name == "all-MiniLM-L6-v2"
    assert abs(cfg.scoring.semantic_similarity - 0.35) < 1e-6
    assert abs(cfg.scoring.skill_match - 0.25) < 1e-6
    assert abs(cfg.scoring.experience_relevance - 0.20) < 1e-6
    assert cfg.pipeline.top_n == 20


def test_load_config_from_path() -> None:
    config_path = Path(__file__).parent.parent / "config" / "default.yaml"
    cfg = load_config(config_path)
    assert cfg.embedding.model_name == "all-MiniLM-L6-v2"
    assert cfg.export.default_format == "csv"
