import logging
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from candidate_ranker.config import EmbeddingConfig

logger = logging.getLogger(__name__)


class EmbeddingEngine:
    """Generates normalized embeddings for text using sentence-transformers."""

    def __init__(self, config: EmbeddingConfig | None = None) -> None:
        self._config = config or EmbeddingConfig()
        logger.info("Loading embedding model: %s", self._config.model_name)
        self._model: SentenceTransformer = SentenceTransformer(
            self._config.model_name,
            cache_folder=self._config.cache_dir,
        )
        logger.info("Model dimension: %d", self.dimension)

    def embed(self, text: str) -> np.ndarray:
        return self._model.encode(text, normalize_embeddings=self._config.normalize_embeddings)

    def embed_many(self, texts: list[str]) -> np.ndarray:
        return self._model.encode(
            texts,
            normalize_embeddings=self._config.normalize_embeddings,
            show_progress_bar=False,
        )

    @property
    def dimension(self) -> int:
        return self._model.get_embedding_dimension()
