import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path("data/raw/rental_inquiries_raw.csv")
OUTPUT_PATH = Path("data/processed/rental_inquiries_cleaned.csv")

def load_data(path):
    return pd.read_csv(path)

def clean_data(df):
    # Standardize text columns
    df["preferred_area"] = df["preferred_area"].str.strip().str.title()
    df["bedroom_type"] = df["bedroom_type"].str.strip()
    df["source_channel"] = df["source_channel"].str.strip()

    # Convert date columns
    df["move_in_date"] = pd.to_datetime(df["move_in_date"])
    df["created_at"] = pd.to_datetime(df["created_at"])

    # Create budget segment
    df["budget_segment"] = pd.cut(
        df["budget"],
        bins = [0, 1500, 2000, 2500, 6000],
        labels=["Low", "Medium", "High", "Premium"]
    )

    # Create conversion flag
    df["is_converted"] = df["status"].apply(lambda x: 1 if x == "Converted" else 0)

    return df

def save_data(df, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)

if __name__ == "__main__":
    data = load_data(RAW_DATA_PATH)
    cleaned_data = clean_data(data)
    save_data(cleaned_data, OUTPUT_PATH)
    print("Data cleaning completed successfully.")

    