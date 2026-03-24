from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

from src.utils.paths import MODEL_FILE
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="ML Inference Service",
    description="Serves default probability predictions for customers",
    version="1.0.0",
)


# Pydantic Input Model
class CustomerFeatures(BaseModel):
    customer_id: str
    txn_count: float
    total_debit: float
    total_credit: float
    avg_amount: float
    kw_rent: int = 0
    kw_netflix: int = 0
    kw_tesco: int = 0
    kw_payroll: int = 0
    kw_bonus: int = 0


# Load Model at Startup
model = None

@app.on_event("startup")
def load_model():
    global model

    logger.info(f"Loading model from {MODEL_FILE}")

    if not MODEL_FILE.exists():
        logger.error("Model file not found")
        raise RuntimeError("Model file not found. Please place model.joblib in artifacts/")

    try:
        model = joblib.load(MODEL_FILE)
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise RuntimeError("Model failed to load")


# Health Check
@app.get("/health")
def health():
    return {"status": "ok"}

# Prediction Endpoint
@app.post("/predict")
def predict(payload: CustomerFeatures):

    if model is None:
        logger.error("Prediction attempted before model load")
        raise HTTPException(status_code=500, detail="Model not loaded")

    logger.info(f"Received prediction request for {payload.customer_id}")

    # Convert to DataFrame (drop customer_id)
    X = pd.DataFrame([payload.dict()]).drop(columns=["customer_id"])

    try:
        proba = float(model.predict_proba(X)[0][1])
        pred = int(proba >= 0.5)
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")

    logger.info(
        f"Prediction for {payload.customer_id}: probability={proba:.4f}, label={pred}"
    )

    return {
        "customer_id": payload.customer_id,
        "probability": proba,
        "prediction": pred,
    }
