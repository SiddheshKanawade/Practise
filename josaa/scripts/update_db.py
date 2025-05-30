import pymongo
import pandas as pd
import os
from glob import glob

MONGO_URL = (
    "mongodb+srv://testsiddheshkanawade:Q41c1fALOVs3nLaU@cluster0.pf6vbum.mongodb.net/"
)

DB_NAME = "josaa"
COLLECTION_NAME = "college_data"

client = pymongo.MongoClient(MONGO_URL)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


def process_csv_file(file_path):
    # Read CSV file
    df = pd.read_csv(file_path)

    # Convert DataFrame to list of dictionaries
    records = df.to_dict("records")

    # Add category information from directory structure
    category = file_path.split("/")[2]  # Extract category from path
    for record in records:
        record["Category"] = category

    return records


def main():
    # Delete existing data
    collection.delete_many({})
    print("Cleared existing data from collection")

    # Get all CSV files from output directory
    csv_files = glob("./output/**/*.csv", recursive=True)

    total_records = 0
    for file_path in csv_files:
        records = process_csv_file(file_path)
        if records:
            # Insert records in bulk
            collection.insert_many(records)
            total_records += len(records)
            print(f"Processed {file_path}: {len(records)} records")

    print(f"\nTotal records inserted: {total_records}")
    print("Database update complete!")


if __name__ == "__main__":
    main()
