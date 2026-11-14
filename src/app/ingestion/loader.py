"""
Dataset loader for fetching data from Hugging Face.
"""

import logging
from typing import Optional
from datasets import load_dataset


logger = logging.getLogger(__name__)


class DatasetLoader:
    """
    Loads the Zomato dataset from Hugging Face.

    Attributes:
        dataset_id: Hugging Face dataset identifier
    """

    def __init__(self, dataset_id: str = "ManikaSaini/zomato-restaurant-recommendation"):
        """
        Initialize the dataset loader.

        Args:
            dataset_id: Hugging Face dataset identifier
        """
        self.dataset_id = dataset_id

    def load_dataset(self, split: Optional[str] = None) -> object:
        """
        Load the dataset from Hugging Face.

        Args:
            split: Dataset split to load (e.g., "train", "test")

        Returns:
            Loaded dataset object

        Raises:
            DatasetNotFoundError: If dataset is not found
            Exception: For other loading errors
        """
        logger.info(f"Loading dataset from Hugging Face: {self.dataset_id}")

        try:
            if split:
                dataset = load_dataset(self.dataset_id, split=split)
            else:
                dataset = load_dataset(self.dataset_id)

            logger.info(f"Dataset loaded successfully")
            logger.info(f"Dataset type: {type(dataset)}")

            # If it's a DatasetDict, get the first split
            if hasattr(dataset, 'keys'):
                logger.info(f"Dataset splits: {list(dataset.keys())}")
                first_split = list(dataset.keys())[0]
                logger.info(f"Using split: {first_split}")
                dataset = dataset[first_split]

            logger.info(f"Dataset info: {dataset}")
            logger.info(f"Dataset length: {len(dataset)}")

            if len(dataset) == 0:
                raise ValueError("Dataset is empty")

            return dataset

        except Exception as e:
            if "not found" in str(e).lower() or "does not exist" in str(e).lower():
                logger.error(f"Dataset not found: {self.dataset_id}")
                raise Exception(
                    f"Dataset '{self.dataset_id}' not found on Hugging Face. "
                    f"Please check the dataset ID and ensure you have access."
                ) from e
            logger.error(f"Error loading dataset: {e}")
            raise Exception(f"Failed to load dataset: {e}") from e
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            raise Exception(f"Failed to load dataset: {e}") from e
