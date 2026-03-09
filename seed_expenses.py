"""
seed_expenses.py — 6 Months of Sample Data
============================================
Run this from INSIDE the expense_tracker folder:
    python seed_expenses.py

It will populate expenses.csv with realistic data
for October 2025 through March 2026.
"""

import csv
import json
from pathlib import Path

DATA_DIR      = Path(__file__).parent / "data"
EXPENSES_FILE = DATA_DIR / "expenses.csv"
BUDGET_FILE   = DATA_DIR / "budgets.json"
FIELDNAMES    = ["id", "date", "amount", "category", "description"]

DATA_DIR.mkdir(exist_ok=True)

EXPENSES = [
    # ── OCTOBER 2025 ──────────────────────────────────────────────────────────
    ("2025-10-01", 1350, "Food",          "Monthly grocery run — BigBasket"),
    ("2025-10-02",  180, "Transport",     "Ola cab to client meeting"),
    ("2025-10-03",  499, "Entertainment", "Amazon Prime annual renewal"),
    ("2025-10-04",  650, "Health",        "Gym monthly membership"),
    ("2025-10-05", 1800, "Utilities",     "Electricity bill"),
    ("2025-10-06",  220, "Food",          "Breakfast at Cafe Coffee Day"),
    ("2025-10-08",  350, "Transport",     "Petrol fill-up"),
    ("2025-10-09",  899, "Shopping",      "Noise-cancelling earbuds"),
    ("2025-10-11",  430, "Food",          "Team lunch — pizza"),
    ("2025-10-12",  650, "Utilities",     "Internet bill — Jio Fiber"),
    ("2025-10-14",  300, "Entertainment", "Movie tickets — Pushpa 2"),
    ("2025-10-15",  120, "Food",          "Evening snacks"),
    ("2025-10-16",  540, "Health",        "Pharmacy — vitamins and supplements"),
    ("2025-10-18", 2400, "Shopping",      "Formal shirts x3 for office"),
    ("2025-10-19",  160, "Transport",     "Metro card top-up"),
    ("2025-10-21",  780, "Food",          "Birthday dinner outing"),
    ("2025-10-22",  200, "Other",         "Donation — local NGO"),
    ("2025-10-23",  450, "Food",          "Weekly vegetables and fruits"),
    ("2025-10-25",  999, "Entertainment", "Spotify and YouTube Premium combo"),
    ("2025-10-26",  310, "Transport",     "Cab — airport drop"),
    ("2025-10-28",  580, "Food",          "Swiggy orders x4"),
    ("2025-10-30",  750, "Health",        "Doctor consultation"),
    ("2025-10-31",  420, "Other",         "Stationery and notebook"),
    # ── NOVEMBER 2025 ─────────────────────────────────────────────────────────
    ("2025-11-01", 1500, "Food",          "Monthly grocery run — DMart"),
    ("2025-11-02",  650, "Health",        "Gym monthly membership"),
    ("2025-11-03",  180, "Transport",     "Ola cab — late night"),
    ("2025-11-04", 1800, "Utilities",     "Electricity bill"),
    ("2025-11-05",  650, "Utilities",     "Internet bill"),
    ("2025-11-06", 3500, "Shopping",      "Diwali clothes shopping"),
    ("2025-11-07", 1200, "Shopping",      "Diwali sweets and dry fruits"),
    ("2025-11-08",  500, "Entertainment", "Diwali celebration outing"),
    ("2025-11-10",  260, "Food",          "Cafe — work from cafe day"),
    ("2025-11-12",  380, "Transport",     "Petrol fill-up"),
    ("2025-11-13",  890, "Food",          "Zomato orders — whole week"),
    ("2025-11-15",  450, "Health",        "Eye checkup and spectacle cleaning"),
    ("2025-11-17", 1499, "Shopping",      "Winter jacket"),
    ("2025-11-18",  340, "Food",          "Weekly vegetables"),
    ("2025-11-19",  200, "Transport",     "Metro card top-up"),
    ("2025-11-20",  799, "Entertainment", "Netflix subscription"),
    ("2025-11-22",  620, "Food",          "Office farewell dinner"),
    ("2025-11-24",  180, "Other",         "Haircut and grooming"),
    ("2025-11-25",  950, "Food",          "Home party groceries"),
    ("2025-11-26",  430, "Health",        "Pharmacy — cold and fever meds"),
    ("2025-11-28",  160, "Transport",     "Auto to railway station"),
    ("2025-11-29",  500, "Other",         "Gift for colleague"),
    ("2025-11-30",  280, "Food",          "Bakery — cake and snacks"),
    # ── DECEMBER 2025 ─────────────────────────────────────────────────────────
    ("2025-12-01", 1600, "Food",          "Monthly grocery — BigBasket"),
    ("2025-12-01",  650, "Health",        "Gym monthly membership"),
    ("2025-12-02", 1800, "Utilities",     "Electricity bill"),
    ("2025-12-02",  650, "Utilities",     "Internet bill"),
    ("2025-12-03",  420, "Transport",     "Petrol fill-up"),
    ("2025-12-04", 4500, "Shopping",      "Christmas gifts for family"),
    ("2025-12-06",  350, "Food",          "Cafe — team catch-up"),
    ("2025-12-08",  600, "Entertainment", "Christmas party tickets"),
    ("2025-12-10",  280, "Food",          "Weekly vegetables and fruits"),
    ("2025-12-11",  520, "Health",        "Dentist appointment"),
    ("2025-12-13",  180, "Transport",     "Cab — night out"),
    ("2025-12-14", 2200, "Shopping",      "New year outfit and accessories"),
    ("2025-12-16",  750, "Food",          "Zomato — holiday binge"),
    ("2025-12-18",  199, "Entertainment", "Amazon Prime movie rental"),
    ("2025-12-20",  380, "Transport",     "Metro pass monthly"),
    ("2025-12-22", 1100, "Food",          "Christmas dinner groceries"),
    ("2025-12-24",  900, "Entertainment", "New year Eve pre-party"),
    ("2025-12-25",  450, "Food",          "Christmas lunch — restaurant"),
    ("2025-12-26",  300, "Other",         "Year-end donation"),
    ("2025-12-28",  680, "Food",          "Post-Christmas party food"),
    ("2025-12-30", 1500, "Entertainment", "New year Eve party"),
    ("2025-12-31",  240, "Transport",     "Cab — new year night"),
    # ── JANUARY 2026 ──────────────────────────────────────────────────────────
    ("2026-01-01",  500, "Food",          "New year brunch"),
    ("2026-01-02",  650, "Health",        "Gym membership — new year resolution"),
    ("2026-01-02", 1400, "Food",          "Monthly grocery run"),
    ("2026-01-03", 1800, "Utilities",     "Electricity bill"),
    ("2026-01-03",  650, "Utilities",     "Internet bill"),
    ("2026-01-05",  350, "Transport",     "Petrol"),
    ("2026-01-06",  999, "Shopping",      "Fitness tracker — new year goal"),
    ("2026-01-08",  420, "Food",          "Weekly vegetables"),
    ("2026-01-10",  600, "Health",        "Full body health checkup"),
    ("2026-01-12",  220, "Transport",     "Cab to airport"),
    ("2026-01-13",  399, "Entertainment", "Hotstar subscription"),
    ("2026-01-14",  750, "Food",          "Pongal celebration lunch"),
    ("2026-01-16",  480, "Shopping",      "New office bag"),
    ("2026-01-18",  310, "Food",          "Zomato — 3 orders"),
    ("2026-01-20",  200, "Transport",     "Metro card top-up"),
    ("2026-01-22",  550, "Health",        "Physiotherapy session"),
    ("2026-01-24",  180, "Other",         "Haircut"),
    ("2026-01-25",  890, "Food",          "Republic day outing — restaurant"),
    ("2026-01-26",  340, "Entertainment", "Movie — IMAX"),
    ("2026-01-28",  420, "Food",          "Weekly vegetables and groceries"),
    ("2026-01-30",  260, "Transport",     "Cab — doctor visit"),
    # ── FEBRUARY 2026 ─────────────────────────────────────────────────────────
    ("2026-02-01",  899, "Entertainment", "Netflix and Spotify bundle"),
    ("2026-02-01",  600, "Health",        "Gym monthly fee"),
    ("2026-02-03",  450, "Food",          "Lunch at office canteen"),
    ("2026-02-05", 1800, "Utilities",     "Electricity bill"),
    ("2026-02-05",  650, "Utilities",     "Internet bill"),
    ("2026-02-07", 1200, "Food",          "Weekly grocery run"),
    ("2026-02-08",  320, "Transport",     "Ola cab to airport"),
    ("2026-02-10",  180, "Transport",     "Metro monthly pass top-up"),
    ("2026-02-12", 3200, "Shopping",      "New running shoes — Nike"),
    ("2026-02-14",  250, "Entertainment", "Movie tickets x2 — Valentines"),
    ("2026-02-14",  850, "Food",          "Valentines day dinner"),
    ("2026-02-18",  380, "Health",        "Pharmacy — vitamins"),
    ("2026-02-20",  200, "Other",         "Birthday card and gift wrap"),
    ("2026-02-21",  750, "Food",          "Team dinner outing"),
    ("2026-02-22",  420, "Transport",     "Petrol fill-up"),
    ("2026-02-24",  560, "Food",          "Zomato — weekend orders"),
    ("2026-02-25",  990, "Shopping",      "Books from Amazon"),
    ("2026-02-26",  300, "Health",        "Yoga class — 2 sessions"),
    ("2026-02-28",  450, "Food",          "Month-end grocery top-up"),
    # ── MARCH 2026 ────────────────────────────────────────────────────────────
    ("2026-03-01",  650, "Health",        "Gym monthly fee"),
    ("2026-03-01", 1500, "Food",          "Monthly grocery run — BigBasket"),
    ("2026-03-02", 1800, "Utilities",     "Electricity bill"),
    ("2026-03-02",  650, "Utilities",     "Internet bill"),
    ("2026-03-03",  399, "Entertainment", "Netflix subscription"),
    ("2026-03-04",  380, "Transport",     "Petrol fill-up"),
    ("2026-03-05",  280, "Food",          "Breakfast meeting — cafe"),
    ("2026-03-05", 1800, "Shopping",      "Holi outfits and colours"),
    ("2026-03-06",  600, "Entertainment", "Holi party tickets"),
    ("2026-03-06",  950, "Food",          "Holi celebration lunch"),
    ("2026-03-06",  420, "Transport",     "Cab — Holi party and back"),
]

# Write CSV
with open(EXPENSES_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
    writer.writeheader()
    for i, (date, amount, category, desc) in enumerate(EXPENSES, start=1):
        writer.writerow({
            "id":          str(i),
            "date":        date,
            "amount":      f"{amount:.2f}",
            "category":    category,
            "description": desc,
        })

print(f"  Written {len(EXPENSES)} expenses to {EXPENSES_FILE}")

# Write budgets
budgets = {
    "Food":          5000.0,
    "Transport":     2000.0,
    "Shopping":      3000.0,
    "Entertainment": 1500.0,
    "Health":        2000.0,
    "Utilities":     3000.0,
    "Other":         1000.0,
}
with open(BUDGET_FILE, "w", encoding="utf-8") as f:
    json.dump(budgets, f, indent=2)
print(f"  Written budgets to {BUDGET_FILE}")
print()
print("  Monthly breakdown")
print("  " + "-" * 44)

months = [
    ("Oct 2025", "2025-10"),
    ("Nov 2025", "2025-11"),
    ("Dec 2025", "2025-12"),
    ("Jan 2026", "2026-01"),
    ("Feb 2026", "2026-02"),
    ("Mar 2026", "2026-03"),
]
for label, prefix in months:
    m = [e for e in EXPENSES if e[0].startswith(prefix)]
    total = sum(e[1] for e in m)
    print(f"  {label}:  {len(m):>2} transactions  |  Rs.{total:>7,}")

total_all = sum(e[1] for e in EXPENSES)
print("  " + "-" * 44)
print(f"  {'6-month total':<14}  {len(EXPENSES):>2} transactions  |  Rs.{total_all:>7,}")
print()
print("  Done! Now run:  python main.py")
