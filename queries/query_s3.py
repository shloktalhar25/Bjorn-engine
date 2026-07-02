import duckdb
from pathlib import Path
from config.settings import (
    AWS_REGION,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    BUCKET_NAME,
)

BASE_DIR = Path(__file__).resolve().parent.parent

def run_query(db_path=None, bucket_name=None):
    if db_path is None:
        db_path = BASE_DIR / "queries" / "analytics.db"
    else:
        db_path = Path(db_path)

    if bucket_name is None:
        bucket_name = BUCKET_NAME

    # Ensure parent directory of db_path exists
    db_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Connecting to DuckDB database at: {db_path}")
    con = duckdb.connect(str(db_path))

    try:
        # Install and load httpfs for S3 query support
        print("Installing and loading httpfs extension...")
        con.execute("INSTALL httpfs;")
        con.execute("LOAD httpfs;")

        # Configure AWS credentials for DuckDB
        region = AWS_REGION or "ap-south-1"
        print(f"Setting S3 region to {region}")
        con.execute(f"SET s3_region='{region}';")

        if AWS_ACCESS_KEY_ID:
            con.execute(f"SET s3_access_key_id='{AWS_ACCESS_KEY_ID}';")
        if AWS_SECRET_ACCESS_KEY:
            con.execute(f"SET s3_secret_access_key='{AWS_SECRET_ACCESS_KEY}';")

        # Query S3
        s3_uri = f"s3://{bucket_name}/processed/listings_clean.parquet"
        print(f"Querying S3 parquet file: {s3_uri}")
        query = f"SELECT * FROM read_parquet('{s3_uri}') LIMIT 10;"
        result = con.execute(query)
        df = result.fetchdf()
        print(f"\nQuery Results (Limit 10):\n{df}")
        return df
    finally:
        # Close connection
        con.close()

if __name__ == "__main__":
    run_query()
