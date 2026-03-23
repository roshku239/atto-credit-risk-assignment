import pandas as pd
import numpy as np


def add_transaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add row-level features before aggregation."""
    df["is_debit"] = (df["type"] == "debit").astype(int)
    df["is_credit"] = (df["type"] == "credit").astype(int)
    df["abs_amount"] = df["amount"].abs()

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["txn_month"] = df["timestamp"].dt.month
    df["txn_day"] = df["timestamp"].dt.day
    df["txn_weekday"] = df["timestamp"].dt.weekday

    return df


def add_customer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add engineered features after aggregation."""
    df["debit_credit_ratio"] = df.apply(
        lambda row: row["total_debit"] / row["total_credit"]
        if row["total_credit"] > 0 else np.nan,
        axis=1,
    )

    df["net_flow"] = df["total_credit"] - df["total_debit"]
    df["avg_txn_amount"] = df["total_amount"] / df["txn_count"]
    df["debit_ratio"] = df["debit_count"] / df["txn_count"]
    df["credit_ratio"] = df["credit_count"] / df["txn_count"]

    return df
