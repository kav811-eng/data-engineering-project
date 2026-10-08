import subprocess
import sys


def run_step(description, script):
    print("\n" + "=" * 60)
    print(description)
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, script],
        check=True
    )

    return result


def main():
    print("\nSTARTING FULL ENERGY MARKET PIPELINE")

    # --------------------------------------------------
    # 1. INGESTION
    # --------------------------------------------------

    run_step(
        "1/20 - Ingesting Consumption",
        "src/ingestion/smard_consumption.py"
    )

    run_step(
        "2/20 - Ingesting Solar",
        "src/ingestion/smard_solar.py"
    )

    run_step(
        "3/20 - Ingesting Wind Offshore",
        "src/ingestion/smard_wind_offshore.py"
    )

    run_step(
        "4/20 - Ingesting Wind Onshore",
        "src/ingestion/smard_wind_onshore.py"
    )

    run_step(
        "5/20 - Ingesting Price",
        "src/ingestion/smard_price.py"
    )

    run_step(
        "6/20 - Ingesting Residual Load",
        "src/ingestion/smard_residual_load.py"
    )

    # --------------------------------------------------
    # 2. TRANSFORMATION
    # --------------------------------------------------

    run_step(
        "7/20 - Cleaning Consumption",
        "src/transformation/clean_consumption.py"
    )

    run_step(
        "8/20 - Cleaning Solar",
        "src/transformation/clean_solar.py"
    )

    run_step(
        "9/20 - Cleaning Offshore Wind",
        "src/transformation/clean_wind_offshore.py"
    )

    run_step(
        "10/20 - Cleaning Onshore Wind",
        "src/transformation/clean_wind_onshore.py"
    )

    run_step(
        "11/20 - Cleaning Price",
        "src/transformation/clean_price.py"
    )

    run_step(
        "12/20 - Cleaning Residual Load",
        "src/transformation/clean_residual_load.py"
    )

    # --------------------------------------------------
    # 3. LOAD INTO POSTGRESQL
    # --------------------------------------------------

    run_step(
        "13/20 - Loading Consumption",
        "src/ingestion/load_consumption.py"
    )

    run_step(
        "14/20 - Loading Solar",
        "src/ingestion/load_solar.py"
    )

    run_step(
        "15/20 - Loading Offshore Wind",
        "src/ingestion/load_wind_offshore.py"
    )

    run_step(
        "16/20 - Loading Onshore Wind",
        "src/ingestion/load_wind_onshore.py"
    )

    run_step(
        "17/20 - Loading Price",
        "src/ingestion/load_price.py"
    )

    run_step(
        "18/20 - Loading Residual Load",
        "src/ingestion/load_residual_load.py"
    )

    # --------------------------------------------------
    # 4. VALIDATION
    # --------------------------------------------------

    run_step(
        "19/20 - Validating All Data",
        "src/ingestion/validate_all_data.py"
    )

    run_step("20/20 - Syncing BI Dataset to Aiven", 
        "src/ingestion/sync_to_aiven.py")

    print("\n" + "=" * 60)
    print("FULL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()