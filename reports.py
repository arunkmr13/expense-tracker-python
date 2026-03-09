"""
reports.py — Monthly Report Generator
=======================================
Generates a plain-text monthly summary report and saves it to reports/.

FILE HANDLING CONCEPTS USED HERE:
  - Writing formatted text to a .txt file with "w" mode
  - Building multi-line file content with a list + "".join()
  - Using pathlib for the output path
  - tell() and seek() demonstrated in the log appender below
  - Appending to a running log file with "a" mode
"""

from datetime import datetime
from pathlib import Path
from config import REPORTS_DIR, load_budgets
from expenses import get_expenses_by_month, get_monthly_summary

LOG_FILE = REPORTS_DIR / "activity.log"


# ─── REPORT GENERATOR ─────────────────────────────────────────────────────────

def generate_report(year: int, month: int) -> Path:
    """
    Generate a formatted monthly expense report and save it as a .txt file.

    The report includes:
      - Total spending for the month
      - Per-category breakdown with budget comparison
      - Over-budget warnings
      - Individual transaction list

    Returns:
        Path to the saved report file
    """
    month_name = datetime(year, month, 1).strftime("%B %Y")
    expenses   = get_expenses_by_month(year, month)
    summary    = get_monthly_summary(year, month)
    budgets    = load_budgets()
    total      = sum(e["amount"] for e in expenses)

    # ── Build report content as a list of lines, then join ──────────────────
    lines = []
    lines.append("=" * 56 + "\n")
    lines.append(f"   EXPENSE REPORT — {month_name}\n")
    lines.append(f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append("=" * 56 + "\n\n")

    lines.append(f"  TOTAL SPENT THIS MONTH:  ₹{total:>10.2f}\n\n")

    # ── Category breakdown ───────────────────────────────────────────────────
    lines.append("  CATEGORY BREAKDOWN\n")
    lines.append("  " + "-" * 54 + "\n")
    lines.append(f"  {'Category':<16} {'Spent':>10}  {'Budget':>10}  {'Status'}\n")
    lines.append("  " + "-" * 54 + "\n")

    over_budget_cats = []
    for cat in summary:
        spent  = summary[cat]
        budget = budgets.get(cat, 0)
        if spent == 0:
            status = "—"
        elif spent > budget:
            status = "⚠ OVER BUDGET"
            over_budget_cats.append(cat)
        elif spent > budget * 0.8:
            status = "▲ Near limit"
        else:
            status = "✓ OK"
        lines.append(f"  {cat:<16} ₹{spent:>9.2f}  ₹{budget:>9.2f}  {status}\n")

    lines.append("  " + "-" * 54 + "\n\n")

    # ── Warnings ─────────────────────────────────────────────────────────────
    if over_budget_cats:
        lines.append("  ⚠  OVER-BUDGET CATEGORIES:\n")
        for cat in over_budget_cats:
            over = summary[cat] - budgets.get(cat, 0)
            lines.append(f"     {cat}: ₹{over:.2f} over budget\n")
        lines.append("\n")

    # ── Transaction list ─────────────────────────────────────────────────────
    lines.append("  TRANSACTIONS\n")
    lines.append("  " + "-" * 54 + "\n")
    if not expenses:
        lines.append("  No transactions this month.\n")
    else:
        lines.append(f"  {'#':<4} {'Date':<12} {'Category':<14} {'Amount':>9}  Description\n")
        lines.append("  " + "-" * 54 + "\n")
        for e in sorted(expenses, key=lambda x: x["date"]):
            desc = e["description"][:22] + "…" if len(e["description"]) > 23 else e["description"]
            lines.append(
                f"  {e['id']:<4} {e['date']:<12} {e['category']:<14} "
                f"₹{e['amount']:>8.2f}  {desc}\n"
            )

    lines.append("\n" + "=" * 56 + "\n")
    lines.append("  End of Report\n")
    lines.append("=" * 56 + "\n")

    # ── Write to file ─────────────────────────────────────────────────────────
    filename    = f"report_{year}_{month:02d}.txt"
    report_path = REPORTS_DIR / filename

    with open(report_path, "w", encoding="utf-8") as f:
        f.writelines(lines)              # writelines() — writes each string in the list

    log_activity(f"Report generated: {filename} ({len(expenses)} transactions, ₹{total:.2f} total)")
    return report_path


# ─── ACTIVITY LOG ─────────────────────────────────────────────────────────────

def log_activity(message: str):
    """
    Append a timestamped entry to the activity log.

    DEMONSTRATES: append mode ("a") — never overwrites, only adds.
    The log grows over time and records every major user action.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)


def read_log(last_n: int = 10) -> list:
    """
    Read the last N lines from the activity log.

    DEMONSTRATES: seek() + tell() to find end of file, then read lines.
    For a large log, we don't want to load the whole file into memory.

    Args:
        last_n: number of recent log entries to return

    Returns:
        list of log line strings
    """
    if not LOG_FILE.exists():
        return []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        # tell() example: record position, read, check how far we moved
        start_pos = f.tell()       # position before reading (= 0)
        lines     = f.readlines()  # read all lines
        end_pos   = f.tell()       # position after reading (= file size)
        _ = start_pos, end_pos     # stored but not printed (just for demo)

    return lines[-last_n:]         # return only the last N entries
