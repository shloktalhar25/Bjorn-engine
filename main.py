import sys
from pathlib import Path

# Add project root to python path (just in case)
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from preprocessing.transformations import clean_data
from ingestion.upload_to_s3 import upload_file_to_s3
from queries.query_s3 import run_query

def main():
    print("STARTING ETL PIPELINE")
    

    # Step 1: Preprocessing using Polars
    print("Preprocessing Data")
    try:
        processed_file = clean_data()
        print("Preprocessing Step Completed successfully!\n")
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        sys.exit(1)

    # Step 2: Ingesting/Uploading to S3 using boto3
    print("STEP 2: Uploading Cleaned Data to S3")
    try:
        upload_file_to_s3(filepath=processed_file)
        print("Upload Step Completed successfully!\n")
    except Exception as e:
        print(f"Error during upload: {e}")
        sys.exit(1)

    # Step 3: Analytics/Querying using DuckDB
    print("STEP 3: Running S3 Queries using DuckDB")
    try:
        run_query()
        print("Analytics Step Completed successfully!\n")
    except Exception as e:
        print(f"Error during query execution: {e}")
        sys.exit(1)
    print("ETL PIPELINE EXECUTED SUCCESSFULLY")
    

if __name__ == "__main__":
    main()
