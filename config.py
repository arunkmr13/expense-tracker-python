"""
config.py — App Configuration & Setup
======================================
Handles the config file (budgets.json) and defines all file paths.

FILE HANDLING CONCEPTS USED HERE:
  - pathlib.Path for all paths
  - json.load / json.dump for reading and writing config
  - mkdir(exist_ok=True) to ensure folders exist
  - FileNotFoundError handling
"""

import json
from pathlib import Path

# ─── PATHS ────────────────────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).parent          # folder this file lives in
DATA_DIR      = BASE_DIR / "data"
REPORTS_DIR   = BASE_DIR / "reports"
EXPENSES_FILE = DATA_DIR / "expenses.csv"
BUDGET_FILE   = DATA_DIR / "budgets.json"

# ─── DEFAULT BUDGETS ──────────────────────────────────────────────────────────
DEFAULT_BUDGETS = {
    "Food":          3000.0,
    "Transport":     1500.0,
    "Shopping":      2000.0,
    "Entertainment": 1000.0,
    "Health":        1000.0,
    "Utilities":     2000.0,
    "Other":         1000.0,
}

CATEGORIES = list(DEFAULT_BUDGETS.keys())


def setup_dirs():
    """Create data/ and reports/ directories if they don't exist."""
    DATA_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)


def load_budgets():
    """
    Load monthly budgets from budgets.json.
    Returns DEFAULT_BUDGETS if the file doesn't exist yet.
    """
    try:
        with open(BUDGET_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return DEFAULT_BUDGETS.copy()


def save_budgets(budgets: dict):
    """Save the budgets dict to budgets.json with pretty formatting."""
    with open(BUDGET_FILE, "w", encoding="utf-8") as f:
        json.dump(budgets, f, indent=2)
    print(f"  Budgets saved to {BUDGET_FILE}")
