import pandas as pd

INPUT_PATH = "data/raw/smard_wind_onshore_full.parquet"
OUTPUT_PATH = "data/processed/smard_wind_onshore_clean.parquet"


def clean_wind_onshore_data(df):
    df = df.copy()

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )

    df["wind_onshore"] = pd.to_numeric(
        df["wind_onshore"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["wind_onshore"]
    )

    df = df.drop_duplicates(
        subset=["timestamp"]
    )

    df = df.sort_values(
        "timestamp"
    ).reset_index(drop=True)

    df["date"] = df["timestamp"].dt.date
    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.month
    df["day"] = df["timestamp"].dt.day
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["is_weekend"] = df["day_of_week"] >= 5

    return df


def main():
    print("Loading raw wind onshore data...")

    df = pd.read_parquet(INPUT_PATH)

    print("Raw rows:", len(df))

    clean_df = clean_wind_onshore_data(df)

    print("Clean rows:", len(clean_df))

    print("\nData types:")
    print(clean_df.dtypes)

    print("\nDate range:")
    print(clean_df["timestamp"].min())
    print(clean_df["timestamp"].max())

    clean_df.to_parquet(
        OUTPUT_PATH,
        index=False
    )

    print(
        f"\nSaved cleaned data to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()