import pandas as pd


INPUT_PATH = "data/raw/smard_consumption_full.parquet"
OUTPUT_PATH = "data/processed/smard_consumption_clean.parquet"


def clean_consumption_data(df):
    """Clean and validate SMARD electricity consumption data."""

    df = df.copy()

    # Ensure timestamp is datetime
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )

    # Add time dimensions
    df["date"] = df["timestamp"].dt.date
    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.month
    df["day"] = df["timestamp"].dt.day
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["is_weekend"] = df["day_of_week"] >= 5

    # Remove rows without consumption
    df = df.dropna(
        subset=["consumption"]
    )

    # Remove duplicate timestamps
    df = df.drop_duplicates(
        subset=["timestamp"]
    )

    # Sort chronologically
    df = df.sort_values(
        "timestamp"
    ).reset_index(drop=True)

    # Make sure consumption is numeric
    df["consumption"] = pd.to_numeric(
        df["consumption"],
        errors="coerce"
    )

    # Remove any rows that became invalid
    df = df.dropna(
        subset=["consumption"]
    )

    return df


def main():

    print("Loading raw data...")

    df = pd.read_parquet(INPUT_PATH)

    print("Raw rows:", len(df))

    clean_df = clean_consumption_data(df)

    print("Clean rows:", len(clean_df))

    print("\nClean data:")
    print(clean_df.head())

    print("\nData types:")
    print(clean_df.dtypes)

    print("\nColumns:")
    print(clean_df.columns.tolist())

    print("\nDate range:")
    print(clean_df["timestamp"].min())
    print(clean_df["timestamp"].max())

    # Save processed data
    clean_df.to_parquet(
        OUTPUT_PATH,
        index=False
    )

    print(
        f"\nSaved cleaned data to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()