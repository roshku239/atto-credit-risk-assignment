**Atto – Credit Risk Prediction Assignment**

Credit‑risk data pipeline and prediction API built with scalable, fintech‑grade engineering practices

**Overview**

This repository contains a complete end‑to‑end solution for Atto’s credit‑risk prediction assignment. It includes:

    A production‑ready ETL pipeline that cleans, validates, and aggregates raw transaction data

    A FastAPI inference service that loads a pre‑trained model and serves predictions

    Clear documentation of assumptions, trade‑offs, and how this system would scale in a real‑world environment

**Repository Structure**
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
