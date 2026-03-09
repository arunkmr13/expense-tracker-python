"""
expenses.py — Expense CRUD via CSV
=====================================
All expense records are stored in data/expenses.csv.

FILE HANDLING CONCEPTS USED HERE:
  - csv.DictReader  → read rows as dicts
  - csv.DictWriter  → write dicts as rows
  - open() with "r", "w", "a" modes
  - newline="" for correct CSV behaviour on Windows
  - File existence check before reading
  - Appending a single row without rewriting the whole file

CSV FORMAT (one row per expense):
  id, date, amount, category, description

Example row:
  3, 2024-03-15, 450.00, Food, Lunch at restaurant
"""

import csv
from datetime import datetime
from pathlib import Path
from config import EXPENSES_FILE, CATEGORIES

# CSV column names — order matters for the file
FIELDNAMES = ["id", "date", "amount", "category", "description"]


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def _ensure_csv_header():
    """
    Write the header row to expenses.csv if the file doesn't exist yet.
    Uses 'x' (exclusive create) mode — only creates, never overwrites.
    """
    if not EXPENSES_FILE.exists():
        with open(EXPENSES_FILE, "x", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def _load_all():
    """
    Read all rows from expenses.csv and return as a list of dicts.
    Returns [] if the file doesn't exist or is empty (header only).
    """
    if not EXPENSES_FILE.exists():
        return []
    with open(EXPENSES_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


def _next_id(rows: list) -> str:
    """Generate the next integer ID as a string."""
    if not rows:
        return "1"
    return str(max(int(r["id"]) for r in rows) + 1)


# ─── PUBLIC API ───────────────────────────────────────────────────────────────

def add_expense(amount: float, category: str, description: str, date: str = None) -> dict:
    """
    Append a new expense row to expenses.csv.

    Uses APPEND mode ("a") + DictWriter — adds exactly one row
    without reading or rewriting the entire file. Fast and efficient.

    Args:
        amount:      positive float (e.g. 250.50)
        category:    must be one of CATEGORIES
        description: short text description
        date:        "YYYY-MM-DD" string, defaults to today

    Returns:
        dict of the newly added expense

    Raises:
        ValueError: if category invalid or amount <= 0
    """
    if category not in CATEGORIES:
        raise ValueError(f"Invalid category '{category}'. Choose from: {', '.join(CATEGORIES)}")
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

    _ensure_csv_header()
    all_rows = _load_all()

    expense = {
        "id":          _next_id(all_rows),
        "date":        date or datetime.now().strftime("%Y-%m-%d"),
        "amount":      f"{amount:.2f}",
        "category":    category,
        "description": description.strip(),
    }

    # KEY CONCEPT: append mode — adds row without touching existing data
    with open(EXPENSES_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(expense)

    return expense


def get_all_expenses() -> list:
    """
    Read and return all expense records from the CSV file.

    Returns:
        list of dicts, each with keys: id, date, amount, category, description
        Amount values are returned as floats (converted from strings in CSV).
    """
    rows = _load_all()
    for row in rows:
        row["amount"] = float(row["amount"])   # CSV stores strings; convert back
    return rows


def get_expenses_by_month(year: int, month: int) -> list:
    """
    Filter expenses to a specific year and month.

    Args:
        year:  e.g. 2024
        month: 1–12

    Returns:
        list of matching expense dicts
    """
    all_exp = get_all_expenses()
    return [
        e for e in all_exp
        if e["date"].startswith(f"{year}-{month:02d}")
    ]


def get_expenses_by_category(category: str) -> list:
    """Return all expenses for a specific category."""
    if category not in CATEGORIES:
        raise ValueError(f"Unknown category: {category}")
    return [e for e in get_all_expenses() if e["category"] == category]


def delete_expense(expense_id: str) -> dict:
    """
    Delete an expense by ID.

    Since CSV doesn't support in-place deletion, this:
    1. Reads all rows into memory
    2. Removes the matching row
    3. Rewrites the entire file (read → filter → write)

    This is the standard pattern for CSV deletion.

    Raises:
        ValueError: if ID not found
    """
    all_rows = _load_all()
    target = next((r for r in all_rows if r["id"] == str(expense_id)), None)
    if not target:
        raise ValueError(f"Expense ID '{expense_id}' not found")

    updated = [r for r in all_rows if r["id"] != str(expense_id)]

    # KEY CONCEPT: full rewrite — "w" mode overwrites the file from scratch
    with open(EXPENSES_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(updated)

    target["amount"] = float(target["amount"])
    return target


def get_monthly_summary(year: int, month: int) -> dict:
    """
    Compute spending totals per category for a given month.

    Returns:
        dict like {"Food": 1200.0, "Transport": 340.0, ...}
    """
    expenses = get_expenses_by_month(year, month)
    summary = {cat: 0.0 for cat in CATEGORIES}
    for e in expenses:
        summary[e["category"]] = summary.get(e["category"], 0.0) + e["amount"]
    return summary
