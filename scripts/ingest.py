"""
CLI script for running the data ingestion pipeline.
"""

import logging
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app.ingestion.pipeline import IngestionPipeline


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


def main():
    """Main entry point for the ingestion script."""
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting data ingestion script")

    try:
        # Create and run pipeline
        pipeline = IngestionPipeline()
        output_path = pipeline.run()

        logger.info(f"Ingestion completed successfully!")
        logger.info(f"Processed data saved to: {output_path}")

        return 0

    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
