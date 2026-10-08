import requests
import pandas as pd


FILTER_ID = 410
REGION = "DE"
RESOLUTION = "hour"


def get_available_periods():
    """Get the available SMARD data-period timestamps."""

    url = (
        f"https://www.smard.de/app/chart_data/"
        f"{FILTER_ID}/{REGION}/index_{RESOLUTION}.json"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    return response.json()["timestamps"]


def download_period(timestamp):
    """Download one SMARD period and return it as a DataFrame."""

    url = (
        f"https://www.smard.de/app/chart_data/"
        f"{FILTER_ID}/{REGION}/"
        f"{FILTER_ID}_{REGION}_{RESOLUTION}_{timestamp}.json"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(
        data["series"],
        columns=["timestamp", "consumption"]
    )

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        unit="ms",
        utc=True
    )

    return df


if __name__ == "__main__":

    periods = get_available_periods()

    print(f"Available periods: {len(periods)}")

    # Download the first 5 periods as a test
    all_data = []

    for i, timestamp in enumerate(periods, start=1):

        print(f"Downloading period {i}/{len(periods)}...")

        df = download_period(timestamp)

        all_data.append(df)

    # Combine periods
    combined_df = pd.concat(
        all_data,
        ignore_index=True
    )

    # Remove missing observations
    combined_df = combined_df.dropna(
        subset=["consumption"]
    )

    # Remove duplicate timestamps
    combined_df = combined_df.drop_duplicates(
        subset=["timestamp"]
    )

    # Sort chronologically
    combined_df = combined_df.sort_values(
        "timestamp"
    ).reset_index(drop=True)

    def validate_data(df):
        """Run basic quality checks on the downloaded dataset."""

        print("\n--- Data validation ---")

        print("Total rows:", len(df))
        print("Missing consumption values:", df["consumption"].isna().sum())
        print("Duplicate timestamps:", df["timestamp"].duplicated().sum())

        print(
        "Timestamp sorted:",
        df["timestamp"].is_monotonic_increasing
        )

    print(
        "Minimum consumption:",
        df["consumption"].min()
    )

    print(
        "Maximum consumption:",
        df["consumption"].max()
    )

    print(
        "Average consumption:",
        df["consumption"].mean()
    )

    # Check time gaps
    time_diff = df["timestamp"].diff().dropna()

    print("\nTime difference between observations:")
    print(time_diff.value_counts().head())


    print("\nFinal dataset:")
    print(combined_df.head())

    print("\nLast rows:")
    print(combined_df.tail())

    print("\nRows:", len(combined_df))

    print("\nDate range:")
    print(combined_df["timestamp"].min())
    print(combined_df["timestamp"].max())

    # Save raw data
output_path = "data/raw/smard_consumption_full.parquet"

combined_df.to_parquet(
    output_path,
    index=False
)

print(f"\nSaved raw data to: {output_path}")

