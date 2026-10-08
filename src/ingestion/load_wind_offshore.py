import os
import pandas as pd
import psycopg
from dotenv import load_dotenv

load_dotenv()

INPUT_PATH = "data/processed/smard_wind_offshore_clean.parquet"

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))


def main():

    print("Loading Parquet file...")

    df = pd.read_parquet(INPUT_PATH)

    print(f"Rows to load: {len(df)}")

    with psycopg.connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT,
    ) as conn:

        with conn.cursor() as cur:

            print("Loading data into PostgreSQL...")

            rows = df[
                [
                    "timestamp",
                    "wind_offshore",
                    "date",
                    "year",
                    "month",
                    "day",
                    "hour",
                    "day_of_week",
                    "is_weekend",
                ]
            ].itertuples(index=False, name=None)

            cur.executemany(
                """
                INSERT INTO energy_market.wind_offshore_hourly (
                    timestamp,
                    wind_offshore,
                    date,
                    year,
                    month,
                    day,
                    hour,
                    day_of_week,
                    is_weekend
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (timestamp) DO NOTHING;
                """,
                rows,
            )

        conn.commit()

    print("Wind offshore data loaded successfully!")


if __name__ == "__main__":
    main()