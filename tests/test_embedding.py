"""Tests for the embedding engine."""

import numpy as np
import pytest

from candidate_ranker.embedding import EmbeddingEngine


@pytest.fixture
def engine() -> EmbeddingEngine:
    return EmbeddingEngine()


def test_embed_returns_numpy_array(engine: EmbeddingEngine) -> None:
    emb = engine.embed("Hello world")
    assert isinstance(emb, np.ndarray)
    assert emb.shape == (engine.dimension,)


def test_embed_normalized(engine: EmbeddingEngine) -> None:
    emb = engine.embed("Test sentence for embedding")
    norm = np.linalg.norm(emb)
    assert abs(norm - 1.0) < 1e-5


def test_embed_many_shape(engine: EmbeddingEngine) -> None:
    texts = ["First text", "Second text", "Third text"]
    embs = engine.embed_many(texts)
    assert embs.shape == (3, engine.dimension)


def test_similar_texts_higher_similarity(engine: EmbeddingEngine) -> None:
    emb1 = engine.embed("Software engineer with Python experience")
    emb2 = engine.embed("Backend developer skilled in Python")
    emb3 = engine.embed("I like to cook Italian food")

    sim_similar = float(np.dot(emb1, emb2))
    sim_different = float(np.dot(emb1, emb3))

    assert sim_similar > sim_different


def test_dimension_positive(engine: EmbeddingEngine) -> None:
    assert engine.dimension > 0
    assert isinstance(engine.dimension, int)
