import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://ash_user:ash_password@localhost:5432/ash_inventory"
)
DATA_PATH = os.getenv(
    "DATA_PATH",
    os.path.join(os.path.dirname(__file__), '../../data/raw/sample_data.csv')
)

# Sample ETL: Extract, Transform, Load

def extract(path):
    print(f"Extracting data from {path}")
    return pd.read_csv(path)


def transform(df):
    print("Transforming data")
    # Example transformation: drop rows with missing values
    df = df.dropna()
    # Add a synthetic binary target: 1 if production_rate > 0, else 0
    df['target'] = (df['production_rate'] > 0).astype(int)
    return df


def load(df, db_url, table_name="assets"):
    print(f"Loading data into {table_name} table")
    engine = create_engine(db_url)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print("Load complete.")


def main():
    df = extract(DATA_PATH)
    df = transform(df)
    # Save processed data for ML pipeline
    processed_path = os.path.join(
        os.path.dirname(__file__),
        '../../data/processed/sample_asset_data.csv'
    )
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    df.to_csv(processed_path, index=False)
    print(f"Processed data saved to {processed_path}")
    load(df, DATABASE_URL)


if __name__ == "__main__":
    main() 