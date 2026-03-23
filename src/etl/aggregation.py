import pandas as pd


def aggregate_customer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate transaction-level features into customer-level metrics."""

    agg = (
        df.groupby("customer_id")
        .agg(
            txn_count=("transaction_id", "count"),
            total_debit=("amount", lambda x: x[x < 0].sum()),
            total_credit=("amount", lambda x: x[x > 0].sum()),
            total_amount=("amount", "sum"),
            debit_count=("is_debit", "sum"),
            credit_count=("is_credit", "sum"),
            debit_std=("amount", lambda x: x[x < 0].std()),
            all_desc=("clean_desc", lambda x: " ".join(x)),
        )
        .reset_index()
    )

    return agg
