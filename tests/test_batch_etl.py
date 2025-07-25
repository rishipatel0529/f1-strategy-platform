# tests/test_batch_etl.py

import pandas as pd

from src.features.batch_etl import run_batch_etl


def test_batch_etl_output(tmp_path, monkeypatch):
    # --- 1) Create a fake CSV in data/raw/historical/2019 ---
    csv_dir = tmp_path / "data" / "raw" / "historical" / "2019"
    csv_dir.mkdir(parents=True, exist_ok=True)
    sample_csv = csv_dir / "sample_2019.csv"
    sample_csv.write_text("driver_id,lap_number,lap_time\n10,1,90.5\n")

    # --- 2) Create a fake Parquet in data/raw/historical_fastf1/2019 ---
    df_parquet = pd.DataFrame(
        {"driver_id": [11], "lap_number": [1], "lap_time": [91.2]}
    )
    pq_dir = tmp_path / "data" / "raw" / "historical_fastf1" / "2019"
    pq_dir.mkdir(parents=True, exist_ok=True)
    df_parquet.to_parquet(pq_dir / "sample_2019.parquet", index=False)

    # --- 3) Point cwd to our tmp_path so run_batch_etl sees the above ---
    monkeypatch.chdir(tmp_path)

    # --- 4) Run the ETL ---
    df_out = run_batch_etl()

    # --- 5) Assert the merged CSV was written ---
    out_csv = tmp_path / "data" / "historical_telemetry.csv"
    assert out_csv.exists(), f"Expected output at {out_csv}"

    # --- 6) Read it back and verify both rows are present ---
    df_check = pd.read_csv(out_csv)
    assert set(df_check["driver_id"]) == {10, 11}
    assert sorted(df_check["lap_time"].tolist()) == [90.5, 91.2]

    # And ensure the returned DataFrame matches
    assert isinstance(df_out, pd.DataFrame)
    assert set(df_out["driver_id"]) == {10, 11}
    assert sorted(df_out["lap_time"].tolist()) == [90.5, 91.2]
