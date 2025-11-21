from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_EEP_PATH = BASE_DIR / "data" / "raw" / "eep.csv"
PROCESSED_EEP_PATH = BASE_DIR / "data" / "processed" / "eep_processed.csv"

FIGURES_DIR = BASE_DIR / "results" / "figures"
TABLES_DIR = BASE_DIR / "results" / "tables"

RANDOM_STATE = 42
