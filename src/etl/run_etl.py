import os
import pandas as pd
from src.etl.schema import TransactionsSchema, LabelsSchema
from src.etl.text_cleaning import clean_description
from src.etl.feature_engineering import add_transaction_features, add_customer_features
from src.etl.aggregation import aggregate_customer_features

DATA_DIR = "data"
ARTIFACTS_DIR = "artifacts"


def load_data():
    tx = pd.read_csv(os.path.join(DATA_DIR, "transactions.csv"))
    labels = pd.read_csv(os.path.join(DATA_DIR, "labels.csv"))
    return tx, labels


def validate(tx, labels):
    TransactionsSchema.validate(tx)
    LabelsSchema.validate(labels)


def transform(tx):
    tx["clean_desc"] = tx["description"].apply(clean_description)
    tx = add_transaction_features(tx)
    return tx


def build_customer_dataset(tx):
    customer_df = aggregate_customer_features(tx)
    customer_df = add_customer_features(customer_df)
    return customer_df


def merge_labels(customer_df, labels):
    return customer_df.merge(labels, on="customer_id", how="left")


def save(df):
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    df.to_csv(os.path.join(ARTIFACTS_DIR, "training_set.csv"), index=False)
    print("Saved artifacts/training_set.csv")


def run():
    print("Starting ETL pipeline..")

    tx, labels = load_data()
    print("Loaded data")

    validate(tx, labels)
    print("Validation passed")

    tx = transform(tx)
    print("Transaction-level features added")

    customer_df = build_customer_dataset(tx)
    print("Customer-level features created")

    final_df = merge_labels(customer_df, labels)
    print("Labels merged")

    save(final_df)
    print("ETL completed")


if __name__ == "__main__":
    run()
