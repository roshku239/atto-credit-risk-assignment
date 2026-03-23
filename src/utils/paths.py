from pathlib import Path

# Base project directories
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
LOGS_DIR = BASE_DIR / "logs"
MODELS_DIR = BASE_DIR / "artifacts"   # model.joblib usually lives here

# Ensure required folders exist
ARTIFACTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# File paths
TRANSACTIONS_FILE = DATA_DIR / "transactions.csv"
LABELS_FILE = DATA_DIR / "labels.csv"
TRAINING_SET_FILE = ARTIFACTS_DIR / "training_set.csv"
MODEL_FILE = MODELS_DIR / "model.joblib"
LOG_FILE = LOGS_DIR / "etl.log"
