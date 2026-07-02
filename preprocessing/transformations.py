import os
import polars as pl
from pathlib import Path

# Resolve project base directory (parent of preprocessing/)
BASE_DIR = Path(__file__).resolve().parent.parent

def clean_data(raw_path=None, processed_path=None):
    if raw_path is None:
        raw_path = BASE_DIR / "data" / "raw" / "listings.parquet"
    else:
        raw_path = Path(raw_path)

    if processed_path is None:
        processed_path = BASE_DIR / "data" / "processed" / "listings_clean.parquet"
    else:
        processed_path = Path(processed_path)

    print(f"Reading raw data from: {raw_path}")
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw data file not found at {raw_path}")

    # reading the file from the directory
    df = pl.read_parquet(raw_path)
    print(f"Data shape before cleaning: {df.shape}")
    print(f"Before cleaning sample:\n{df.head(5)}")

    # handling missing data:
    # drop any row that contains at least one null value
    df = df.drop_nulls()

    # remove duplicates if any
    df = df.unique()

    print(f"Data shape after cleaning: {df.shape}")
    print(f"After cleaning sample:\n{df.head(5)}")

    # Ensure parent directory exists
    processed_path.parent.mkdir(parents=True, exist_ok=True)

    # save the cleaned data to a new parquet file
    df.write_parquet(processed_path)
    print(f"Cleaned data saved to {processed_path}")
    return processed_path

if __name__ == "__main__":
    clean_data()
