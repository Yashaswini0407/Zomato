"""
Data ingestion pipeline orchestrator.
"""

import logging
from typing import Optional
from src.app.ingestion.loader import DatasetLoader
from src.app.ingestion.normalizer import SchemaNormalizer
from src.app.ingestion.preprocessor import Preprocessor
from src.app.ingestion.writer import PersistenceWriter
from src.app.config import get_settings


logger = logging.getLogger(__name__)


class IngestionPipeline:
    """
    Orchestrates the complete data ingestion pipeline.

    Coordinates loading, normalization, preprocessing, and persistence.
    """

    def __init__(
        self,
        dataset_id: Optional[str] = None,
        output_path: Optional[str] = None,
    ):
        """
        Initialize the ingestion pipeline.

        Args:
            dataset_id: Hugging Face dataset ID (from config if None)
            output_path: Output file path (from config if None)
        """
        settings = get_settings()

        self.dataset_id = dataset_id or "ManikaSaini/zomato-restaurant-recommendation"
        self.output_path = output_path or settings.data_path

        # Initialize components
        self.loader = DatasetLoader(self.dataset_id)
        self.normalizer = SchemaNormalizer()
        self.preprocessor = Preprocessor(
            budget_low_max=settings.budget_low_max,
            budget_medium_max=settings.budget_medium_max,
        )
        self.writer = PersistenceWriter(self.output_path)

    def run(self, split: Optional[str] = None) -> str:
        """
        Run the complete ingestion pipeline.

        Args:
            split: Dataset split to load (e.g., "train", "test")

        Returns:
            Path to the processed data file

        Raises:
            Exception: If any stage of the pipeline fails
        """
        logger.info("=" * 60)
        logger.info("Starting data ingestion pipeline")
        logger.info("=" * 60)

        try:
            # Stage 1: Load dataset
            logger.info("Stage 1: Loading dataset from Hugging Face")
            raw_dataset = self.loader.load_dataset(split=split)
            logger.info(f"Dataset loaded: {len(raw_dataset)} rows")

            # Stage 2: Normalize schema
            logger.info("Stage 2: Normalizing schema")
            normalized_data = self.normalizer.normalize(raw_dataset)
            logger.info(f"Schema normalized: {len(normalized_data)} rows")

            # Stage 3: Preprocess data
            logger.info("Stage 3: Preprocessing data")
            processed_data = self.preprocessor.preprocess(normalized_data)
            logger.info(f"Data preprocessed: {len(processed_data)} rows")

            # Stage 4: Write to disk
            logger.info("Stage 4: Writing to disk")
            output_path = self.writer.write(processed_data, format="parquet")
            logger.info(f"Data written to: {output_path}")

            # Stage 5: Verify
            logger.info("Stage 5: Verifying output")
            if self.writer.verify():
                logger.info("Verification successful")
            else:
                logger.warning("Verification failed")

            logger.info("=" * 60)
            logger.info("Ingestion pipeline completed successfully")
            logger.info("=" * 60)

            return output_path

        except Exception as e:
            logger.error(f"Ingestion pipeline failed: {e}")
            logger.error("=" * 60)
            raise
