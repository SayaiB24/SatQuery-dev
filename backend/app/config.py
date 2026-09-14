import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
SESSIONS_DIR = STORAGE_DIR / "sessions"
EVIDENCE_DIR = STORAGE_DIR / "evidence"

# Ensure directories exist
STORAGE_DIR.mkdir(exist_ok=True)
SESSIONS_DIR.mkdir(exist_ok=True)
EVIDENCE_DIR.mkdir(exist_ok=True)

# Application settings
APP_TITLE = "SatQuery AI API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Agentic Vision-Language Assistant for Multimodal Remote Sensing (ISRO SIH26167)"

# Validation thresholds (SPDD §4.2)
MIN_FOOTPRINT_OVERLAP_PERCENT = 70.0
MAX_NODATA_PERCENT = 40.0
CLOUD_MASK_WARN_PERCENT = 40.0

# CORS settings
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "*"
]
