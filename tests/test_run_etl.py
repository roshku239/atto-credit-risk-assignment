import pandas as pd
from pathlib import Path
import shutil

from src.etl.run_etl import (
    load_data,
    transform,
    build_customer_dataset,
    merge_labels,
    save,
)


def setup_temp_env(tmp_path):
    """Create temporary data + artifacts folders with sample CSVs."""
    data_dir = tmp_path / "data"
    artifacts_dir = tmp_path / "artifacts"
    data_dir.mkdir()
    artifacts_dir.mkdir()

    # Sample transactions
    tx = pd.DataFrame({
        "customer_id": ["C1", "C1", "C2"],
        "transaction_id": ["T1", "T2", "T3"],
        "amount": [-50, 200, -10],
        "type": ["debit", "credit", "debit"],
        "description": ["TESCO 123", "SALARY PAYMENT", "RENT FEB"],
        "timestamp": ["2024-01-01", "2024-01-02", "2024-01-03"]
    })
    tx.to_csv(data_dir / "transactions.csv", index=False)

    # Sample labels
    labels = pd.DataFrame({
        "customer_id": ["C1", "C2"],
        "defaulted": [0, 1]
    })
    labels.to_csv(data_dir / "labels.csv", index=False)

    return data_dir, artifacts_dir


# Test 1: ETL transforms and aggregates correctly
def test_etl_transforms_correctly(tmp_path, monkeypatch):

    data_dir, artifacts_dir = setup_temp_env(tmp_path)

    # Patch paths inside run_etl
    monkeypatch.setattr("src.etl.run_etl.DATA_DIR", str(data_dir))
    monkeypatch.setattr("src.etl.run_etl.ARTIFACTS_DIR", str(artifacts_dir))

    # Load
    tx, labels = load_data()

    # Transform
    tx = transform(tx)

    # Aggregate
    customer_df = build_customer_dataset(tx)

    # Merge
    final_df = merge_labels(customer_df, labels)

    # Assertions
    assert "customer_id" in final_df.columns
    assert "txn_count" in final_df.columns
    assert "total_debit" in final_df.columns
    assert "total_credit" in final_df.columns
    assert "defaulted" in final_df.columns

    # Check row count
    assert len(final_df) == 2  # C1 and C2


# Test 2: ETL writes training_set.csv
def test_etl_saves_output(tmp_path, monkeypatch):

    data_dir, artifacts_dir = setup_temp_env(tmp_path)

    monkeypatch.setattr("src.etl.run_etl.DATA_DIR", str(data_dir))
    monkeypatch.setattr("src.etl.run_etl.ARTIFACTS_DIR", str(artifacts_dir))

    # Load + transform + aggregate
    tx, labels = load_data()
    tx = transform(tx)
    customer_df = build_customer_dataset(tx)
    final_df = merge_labels(customer_df, labels)

    # Save
    save(final_df)

    output_file = artifacts_dir / "training_set.csv"
    assert output_file.exists()

    df = pd.read_csv(output_file)
    assert "customer_id" in df.columns
    assert "defaulted" in df.columns
