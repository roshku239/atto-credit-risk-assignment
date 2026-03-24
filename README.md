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


**1. What part of the exercise did you find most challenging, and why?**
The trickiest part was aligning the raw CSV structure, schema validation, and feature engineering logic.
This mirrors real world challenges: upstream data often drifts, and ensuring the pipeline is both strict (to catch issues) and flexible (to evolve safely) requires careful design.I also kept the ETL lightweight, but still production oriented, clear and easy to maintain.
	
**2. What tradeoffs did you make? (e.g., speed vs. accuracy, simplicity vs. completeness)**
Simplicity vs. Completeness
Choosen a clean, Pandas based ETL rather than Spark. For this dataset size, Pandas was the right choice to iterate on and easier to read.

Speed vs. Accuracy
The model is simple to keep inference latency low. More complex models could improve accuracy but would increase cost and operational overhead.

Strictness vs. Flexibility
Pandera validation added to catch schema issues but I avoided over engineering rules that would slow iteration.

**3. Assume this needs to run in production with these constraints:**
– Cloud provider: Azure
– Budget: £500/month
– Latency requirement: <100ms per prediction
– Expected traffic: 1000 predictions/hour initially
What would you improve or change first?

Make the API stateless, 
load the model once (Keep in memory) 
can be deployed on Azure Container Apps 
add lightweight monitoring to track the cost and performance

**4. How would you deploy the FastAPI service and make the model artifact available?**
I would containerise the FastAPI service, push the image to Azure Container Registry, and deploy it to Azure Container Apps with autoscaling. 
It can also be bundle the model artifact inside the Docker image for minimal latency and operational simplicity. 
If model updates become frequent, I’d move the artifact to Azure Blob Storage and load it at startup using Managed Identity. 
Application Insights would provide latency, error, and drift monitoring.


**5. If transaction volume jumped from thousands to millions per day, how would you rethink Part 1?**

if volume jumps from thousands to millions per day, Part 1 (the ETL pipeline) needs a fundamental architectural shift. Pandas based, single machine processing won’t survive that scale due to memory limits, runtime bottlenecks and operational fragility. Also millions of transactions/day require scalable, fault tolerant, and cost efficient architecture.

Move from Pandas → Distributed Processing (Spark) 
Store raw + processed data in Delta Lake for ACID properties
Move to incremental ETL instead of full load
Implement feature store for Centralised feature definitions + Versioning and lineage
Implement Data quality and schema Enforcement
Use orchestration tool to manage the dependencies and SLA
Cost optimization can be done after deep dive into Spot instances (Job clusters with resource pooling, warm clusters), Partitioning, Auto scaling, Cache only when required, Avoid shuffles

**6. What metrics would you track in production and why? What could go wrong with this model in production?**

For optimized cost and time 
API health and latency, Latency, Throughput, Error Rate, Resource Utilization

For Model efficiency:
Input Schema Violations and missing values - To prevent silent failures when upstream systems change schema
Prediction Distribution - To monitor the predicted label distribution over time. 
Model Confidence - To track the predicted probability and calibration drift.   
Feature Distribution and Drift - To track the input features alignment with the base model


**7. If you used AI tools such as ChatGPT, Claude, Copilot, or any other tools:**
– Where and how did you use them? (e.g., boilerplate code, debugging, syntax help)
- How did they help or hinder your process?

Where and how:  
For small tasks such as improving documentation clarity, quick syntax checks, and occasional debugging of minor issues.

How they helped:  
They sped up routine work—refining wording, confirming syntax, and spotting simple bugs so I could focus on core implementation.

How they hindered:  
Some suggestions needed verification for accuracy, but overall they caused no meaningful drawbacks.
