import pandera as pa
from pandera import Column, DataFrameSchema, Check

# Schema for transactions.csv
TransactionsSchema = DataFrameSchema(
    {
        "transaction_id": Column(pa.String, nullable=False),
        "customer_id": Column(pa.String, nullable=False),
        "txn_times": Column(pa.String, nullable=False),  # parsed to datetime later
        "amount": Column(pa.Float, nullable=False),
        "txn_type": Column(
            pa.String,
            nullable=False,
            checks=Check.isin(["credit", "debit"])
        ),
        "description": Column(pa.String, nullable=True),
    },
    strict=True,
    coerce=True,
)

# Schema for labels.csv
LabelsSchema = DataFrameSchema(
    {
        "customer_id": Column(pa.String, nullable=False),
        "defaulted_within_90d": Column(
            pa.Int64,
            nullable=False,
            checks=Check.isin([0, 1])
        ),
    },
    strict=True,
    coerce=True,
)
