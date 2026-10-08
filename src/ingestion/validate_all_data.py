import os
import pandas as pd
import psycopg
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))

TABLES = [
    "consumption_hourly",
    "solar_hourly",
    "wind_offshore_hourly",
    "wind_onshore_hourly",
    "price_hourly",
    "residual_load_hourly",
]


def validate_table(cur, table):
    print(f"\n--- {table} ---")

    cur.execute(f"""
        SELECT
            COUNT(*),
            MIN(timestamp),
            MAX(timestamp)
        FROM energy_market.{table};
    """)

    row_count, min_timestamp, max_timestamp = cur.fetchone()

    print("Rows:", row_count)
    print("Start:", min_timestamp)
    print("End:", max_timestamp)

    cur.execute(f"""
        SELECT COUNT(*)
        FROM energy_market.{table}
        WHERE timestamp IS NULL;
    """)

    null_timestamps = cur.fetchone()[0]

    print("Null timestamps:", null_timestamps)

    cur.execute(f"""
        SELECT COUNT(*)
        FROM (
            SELECT timestamp
            FROM energy_market.{table}
            GROUP BY timestamp
            HAVING COUNT(*) > 1
        ) duplicates;
    """)

    duplicate_timestamps = cur.fetchone()[0]

    print("Duplicate timestamps:", duplicate_timestamps)


def main():
    print("Starting full data validation...")

    with psycopg.connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT,
    ) as conn:

        with conn.cursor() as cur:

            for table in TABLES:
                validate_table(cur, table)

    print("\nValidation complete!")


if __name__ == "__main__":
    main()