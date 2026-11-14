"""
Persistence writer for saving processed data.
"""

import logging
import os
from typing import Optional
import pandas as pd


logger = logging.getLogger(__name__)


class PersistenceWriter:
    """
    Writes processed restaurant data to persistent storage.

    Supports multiple formats: Parquet (primary), SQLite (fallback).
    """

    def __init__(self, output_path: str = "data/processed/restaurants.parquet"):
        """
        Initialize the persistence writer.

        Args:
            output_path: Path where processed data will be saved
        """
        self.output_path = output_path

    def write(self, df: pd.DataFrame, format: str = "parquet") -> str:
        """
        Write the processed data to disk.

        Args:
            df: Processed DataFrame to write
            format: Output format ("parquet" or "sqlite")

        Returns:
            Path to the written file

        Raises:
            IOError: If write operation fails
        """
        logger.info(f"Writing processed data to {self.output_path}")

        # Ensure output directory exists
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        try:
            if format == "parquet":
                self._write_parquet(df)
            elif format == "sqlite":
                self._write_sqlite(df)
            else:
                raise ValueError(f"Unsupported format: {format}")

            logger.info(f"Data written successfully to {self.output_path}")
            logger.info(f"Total rows written: {len(df)}")

            return self.output_path

        except Exception as e:
            logger.error(f"Error writing data: {e}")
            raise IOError(f"Failed to write data: {e}") from e

    def _write_parquet(self, df: pd.DataFrame) -> None:
        """
        Write data in Parquet format.

        Args:
            df: DataFrame to write
        """
        try:
            df.to_parquet(self.output_path, index=False)
            logger.info("Data written in Parquet format")
        except ImportError:
            logger.error("PyArrow not installed for Parquet format")
            raise
        except Exception as e:
            logger.error(f"Failed to write Parquet: {e}")
            raise

    def _write_sqlite(self, df: pd.DataFrame) -> None:
        """
        Write data in SQLite format.

        Args:
            df: DataFrame to write
        """
        try:
            # Change extension to .db for SQLite
            sqlite_path = self.output_path.replace(".parquet", ".db")
            df.to_sql("restaurants", f"sqlite:///{sqlite_path}", if_exists="replace", index=False)
            logger.info(f"Data written in SQLite format to {sqlite_path}")
        except ImportError:
            logger.error("SQLAlchemy not installed for SQLite format")
            raise
        except Exception as e:
            logger.error(f"Failed to write SQLite: {e}")
            raise

    def verify(self) -> bool:
        """
        Verify that the written file is valid.

        Returns:
            True if file is valid, False otherwise
        """
        if not os.path.exists(self.output_path):
            logger.warning(f"File does not exist: {self.output_path}")
            return False

        try:
            if self.output_path.endswith(".parquet"):
                df = pd.read_parquet(self.output_path)
                logger.info(f"Verification successful: {len(df)} rows in file")
                return True
            elif self.output_path.endswith(".db"):
                # SQLite verification would go here
                logger.info("SQLite verification not implemented")
                return True
        except Exception as e:
            logger.error(f"Verification failed: {e}")
            return False

        return False
