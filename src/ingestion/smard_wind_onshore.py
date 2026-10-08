import requests
import pandas as pd

FILTER_ID = 4067
REGION = "DE"
RESOLUTION = "hour"


def get_available_periods():
    url = (
        f"https://www.smard.de/app/chart_data/"
        f"{FILTER_ID}/{REGION}/index_{RESOLUTION}.json"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    return response.json()["timestamps"]


def download_period(timestamp):
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
        columns=["timestamp", "wind_onshore"]
    )

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        unit="ms",
        utc=True
    )

    return df


def main():
    periods = get_available_periods()

    print(f"Available periods: {len(periods)}")

    all_data = []

    for i, timestamp in enumerate(periods, start=1):
        print(f"Downloading period {i}/{len(periods)}...")

        df = download_period(timestamp)
        all_data.append(df)

    combined_df = pd.concat(
        all_data,
        ignore_index=True
    )

    combined_df = combined_df.dropna(
        subset=["wind_onshore"]
    )

    combined_df = combined_df.drop_duplicates(
        subset=["timestamp"]
    )

    combined_df = combined_df.sort_values(
        "timestamp"
    ).reset_index(drop=True)

    print("\nFinal dataset:")
    print(combined_df.head())

    print("\nLast rows:")
    print(combined_df.tail())

    print("\nRows:", len(combined_df))

    print("\nDate range:")
    print(combined_df["timestamp"].min())
    print(combined_df["timestamp"].max())

    output_path = "data/raw/smard_wind_onshore_full.parquet"

    combined_df.to_parquet(
        output_path,
        index=False
    )

    print(f"\nSaved raw data to: {output_path}")


if __name__ == "__main__":
    main()