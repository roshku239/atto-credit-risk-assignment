**Atto – Credit Risk Prediction Assignment**

Credit‑risk data pipeline and prediction API built with scalable, fintech‑grade engineering practices

**Overview**

This repository contains a complete end‑to‑end solution for Atto’s credit‑risk prediction assignment. It includes:

    A production‑ready ETL pipeline that cleans, validates, and aggregates raw transaction data

    A FastAPI inference service that loads a pre‑trained model and serves predictions

    Clear documentation of assumptions, trade‑offs, and how this system would scale in a real‑world environment

**Repository Structure**
<img width="260" height="458" alt="image" src="https://github.com/user-attachments/assets/ebade43a-19e5-4674-aa82-3b616fedf10c" />

**Create the Virtual Environment**
rm -rf venv
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
**Note:** Python 3.10 is recommended for compatibility with the model and scikit‑learn version used.

**How to Run the Project**
1. Install Dependencies
pip install -r requirements.txt
2. Run the ETL Pipeline
python -m src.etl.run_etl
This generates artifacts/training_set.csv
<img width="554" height="155" alt="image" src="https://github.com/user-attachments/assets/26b664d2-654e-48f1-aa33-70ab07ace99b" />
3. Start the FastAPI Service
uvicorn src.api.inference_service:app --reload
<img width="937" height="241" alt="image" src="https://github.com/user-attachments/assets/61169643-65ee-403e-b84f-6c8eee9d66a9" />
Swagger UI available at: http://127.0.0.1:8000/docs
4. Test With Sample Payload

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
Example response:
<img width="809" height="425" alt="image" src="https://github.com/user-attachments/assets/b17a9068-f090-4ff8-a0cc-a27366751f3e" />
