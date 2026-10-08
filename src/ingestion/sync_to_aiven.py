import os
import pandas as pd
from datetime import datetime, timezone

import psycopg
from dotenv import load_dotenv

load_dotenv()

LOCAL_DB = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
}

AIVEN_DB = {
    "dbname": os.getenv("AIVEN_DB"),
    "user": os.getenv("AIVEN_USER"),
    "password": os.getenv("AIVEN_PASSWORD"),
    "host": os.getenv("AIVEN_HOST"),
    "port": os.getenv("AIVEN_PORT"),
    "sslmode": "require",
}




def main():

    # One fixed timestamp for this entire pipeline run
    refresh_time = datetime.now(timezone.utc)

    print("Pipeline refresh time:", refresh_time)

    # ---------------------------------------------------------
    # Read from local PostgreSQL
    # ---------------------------------------------------------

    print("Connecting to local PostgreSQL...")

    with psycopg.connect(**LOCAL_DB) as local_conn:
        with local_conn.cursor() as local_cur:

            local_cur.execute("""
                SELECT
                    timestamp,
                    date,
                    year,
                    month,
                    day,
                    hour,
                    day_of_week,
                    is_weekend,
                    consumption,
                    solar_generation,
                    wind_onshore,
                    wind_offshore,
                    price,
                    residual_load
                FROM energy_market.bi_energy_market
                ORDER BY timestamp;
            """)

            rows = local_cur.fetchall()

    print(f"Read {len(rows)} rows from local PostgreSQL.")

    # ---------------------------------------------------------
    # Add refresh timestamp
    # ---------------------------------------------------------

    rows_with_refresh = [
        row + (refresh_time,)
        for row in rows
    ]

    # ---------------------------------------------------------
    # Write to Aiven
    # ---------------------------------------------------------

    print("Connecting to Aiven...")

    with psycopg.connect(**AIVEN_DB) as aiven_conn:
        with aiven_conn.cursor() as aiven_cur:

            print("Clearing existing Aiven BI table...")

            aiven_cur.execute("""
                TRUNCATE TABLE energy_market.bi_energy_market;
            """)

            print("Loading data into Aiven...")

            aiven_cur.executemany("""
                INSERT INTO energy_market.bi_energy_market (
                    timestamp,
                    date,
                    year,
                    month,
                    day,
                    hour,
                    day_of_week,
                    is_weekend,
                    consumption,
                    solar_generation,
                    wind_onshore,
                    wind_offshore,
                    price,
                    residual_load,
                    last_refresh_at
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s
                );
            """, rows_with_refresh)

    print(f"Successfully synced {len(rows_with_refresh)} rows to Aiven.")
    print("Refresh timestamp:", refresh_time)


if __name__ == "__main__":
    main()