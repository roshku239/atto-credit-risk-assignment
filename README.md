Atto – Credit Risk Prediction Assignment
Credit‑risk data pipeline and prediction API built with scalable, fintech‑grade engineering practices 

1. Overview
This repository contains a complete end‑to‑end solution for Atto’s credit‑risk prediction assignment.
It includes:
    A production‑ready ETL pipeline that cleans, validates, and aggregates raw transaction data
    A FastAPI inference service that loads a pre‑trained model and serves predictions
    A clear documentation of assumptions, tradeoffs, and how this would scale in a real‑world environment

2. Repository Structure

Code snippet
.
├── README.md
├── requirements.txt
├── data/
│   ├── transactions.csv
│   └── labels.csv
├── artifacts/
│   ├── model.joblib
│   └── training_set.csv
├── src/
│   ├── etl/
│   │   ├── run_etl.py
│   │   ├── schemas.py
│   │   ├── text_cleaning.py
│   │   ├── feature_engineering.py
│   │   └── aggregation.py
│   ├── api/
│   │   └── inference_service.py
│   └── utils/
│       ├── logging_config.py
│       └── paths.py
└── tests/
    ├── test_etl_run.py

3. How to Run the Project
Install dependencies
pip install -r requirements.txt

Run the ETL pipeline
python -m src/etl/run_etl.py

This generates:
artifacts/training_set.csv

Start the FastAPI service
uvicorn src.api.inference_service:app --reload

Test the API
POST http://localhost:8000/predict

4. Part 1 – Data Engineering Approach

4.1 Data Loading & Exploration
Loaded transactions.csv and labels.csv

Validated schema using Pandera
    Missing descriptions
    Negative/positive amount inconsistencies
    Duplicate transaction IDs
    Outliers in transaction amounts

4.2 Feature Engineering
Aggregated to one row per customer with:
  Core features
  num_transactions
  total_debit
  total_credit
  avg_amount
Domain‑driven features
  spend_volatility → std deviation of amounts
  debit_credit_ratio → proxy for financial stress
  salary_txn_count → income stability
  max_debit → large unexpected expenses

4.3 Text Processing
  Lowercased descriptions
  Removed punctuation and numbers
  Extracted merchant keywords:
  rent, tesco, netflix, salary, payroll, bonus

Generated binary flags such as:
  kw_rent
  kw_salary
  kw_netflix

4.4 Training Dataset
Merged engineered features with labels and saved to:
artifacts/training_set.csv

5. Part 2 – API Development
A lightweight FastAPI service exposes a /predict endpoint.

Key characteristics
Model loaded once at startup
Pydantic validation for input schema
Logging for observability
Clear error handling
Stateless and container‑friendly

Example Response
json
{
  "customer_id": "CUST001",
  "probability": 0.81,
  "prediction": 1
}
