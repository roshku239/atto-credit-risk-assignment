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

3. Create the virtual environment
rm -rf venv
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip

4. How to Run the Project
Install dependencies
pip install -r requirements.txt

Run the ETL pipeline
python -m src.etl.run_etl

This generates:
artifacts/training_set.csv

<img width="560" height="143" alt="image" src="https://github.com/user-attachments/assets/60dcac3d-3bc1-4c2c-bec6-52ab061b9f15" />

Start the FastAPI service
uvicorn src.api.inference_service:app --reload

<img width="953" height="230" alt="image" src="https://github.com/user-attachments/assets/aa0f6e19-48ee-4508-a9f3-337d9709c9bb" />

Test with sample payload
Swagger UI → http://127.0.0.1:8000/docs
Sample payload:
{
  "customer_id": "CUST_0001",
  "txn_count": 3,
  "total_debit": 65.88,
  "total_credit": 2500.00,
  "avg_amount": 855.33,
  "kw_rent": 0,
  "kw_netflix": 1,
  "kw_tesco": 1,
  "kw_payroll": 1,
  "kw_bonus": 0
}
Response:
<img width="784" height="400" alt="image" src="https://github.com/user-attachments/assets/b2373d12-610d-4677-9c57-871534a8730e" />

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
