"""
main.py — Expense Tracker CLI
===============================
Run this file to start the app:  python main.py

This is the entry point. It ties together:
  - expenses.py  (add, view, delete transactions)
  - reports.py   (generate monthly reports, view log)
  - config.py    (view/update category budgets)
"""

import os
from datetime import datetime
from config import setup_dirs, load_budgets, save_budgets, CATEGORIES
from expenses import (
    add_expense, get_all_expenses, get_expenses_by_month,
    get_expenses_by_category, delete_expense, get_monthly_summary,
)
from reports import generate_report, read_log, log_activity

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def clear():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def separator(char="─", width=54):
    print("  " + char * width)


def pick_category() -> str:
    """Display numbered category list and return the user's choice."""
    print()
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    {i}. {cat}")
    while True:
        try:
            idx = int(input("  Choose category number: ")) - 1
            if 0 <= idx < len(CATEGORIES):
                return CATEGORIES[idx]
            print("  Invalid number, try again.")
        except ValueError:
            print("  Please enter a number.")


def get_month_input():
    """Ask user for year/month and return (year, month) ints."""
    now = datetime.now()
    year_str  = input(f"  Year  [{now.year}]: ").strip()
    month_str = input(f"  Month [{now.month}]: ").strip()
    year  = int(year_str)  if year_str  else now.year
    month = int(month_str) if month_str else now.month
    if not (1 <= month <= 12):
        raise ValueError("Month must be between 1 and 12")
    return year, month


# ─── MENU HANDLERS ────────────────────────────────────────────────────────────

def handle_add():
    """Add a new expense."""
    print("\n  ── Add Expense ──")
    try:
        amount_str  = input("  Amount (₹): ").strip()
        amount      = float(amount_str)
        print("  Category:")
        category    = pick_category()
        description = input("  Description: ").strip()
        date_str    = input("  Date (YYYY-MM-DD, Enter for today): ").strip() or None

        expense = add_expense(amount, category, description, date=date_str)
        print(f"\n  ✓ Added! ID: {expense['id']} | ₹{expense['amount']} | {expense['category']}")
        log_activity(f"Added expense #{expense['id']}: ₹{expense['amount']} [{expense['category']}] {description}")
    except ValueError as e:
        print(f"\n  ⚠  {e}")


def handle_view_all():
    """Display all expenses in a table."""
    print("\n  ── All Expenses ──")
    expenses = get_all_expenses()
    if not expenses:
        print("  No expenses recorded yet.")
        return

    separator()
    print(f"  {'ID':<5} {'Date':<12} {'Category':<14} {'Amount':>9}  Description")
    separator()
    for e in expenses:
        desc = e["description"][:24] + "…" if len(e["description"]) > 25 else e["description"]
        print(f"  {e['id']:<5} {e['date']:<12} {e['category']:<14} ₹{e['amount']:>8.2f}  {desc}")
    separator()
    total = sum(e["amount"] for e in expenses)
    print(f"  {'TOTAL':<33} ₹{total:>8.2f}")


def handle_view_month():
    """View expenses for a specific month."""
    print("\n  ── View by Month ──")
    try:
        year, month = get_month_input()
        expenses    = get_expenses_by_month(year, month)
        month_name  = datetime(year, month, 1).strftime("%B %Y")

        print(f"\n  Expenses for {month_name}: {len(expenses)} transactions")
        separator()
        if not expenses:
            print("  No expenses found.")
        else:
            print(f"  {'Date':<12} {'Category':<14} {'Amount':>9}  Description")
            separator()
            for e in expenses:
                print(f"  {e['date']:<12} {e['category']:<14} ₹{e['amount']:>8.2f}  {e['description']}")
            separator()
            total = sum(e["amount"] for e in expenses)
            print(f"  Total: ₹{total:.2f}")
    except ValueError as e:
        print(f"\n  ⚠  {e}")


def handle_view_category():
    """View all expenses for one category."""
    print("\n  ── View by Category ──")
    print("  Choose a category:")
    try:
        category = pick_category()
        expenses = get_expenses_by_category(category)
        print(f"\n  {category}: {len(expenses)} transactions")
        separator()
        if not expenses:
            print("  No expenses in this category.")
        else:
            for e in expenses:
                print(f"  {e['date']}  ₹{e['amount']:>9.2f}  {e['description']}")
            separator()
            total = sum(e["amount"] for e in expenses)
            print(f"  Total: ₹{total:.2f}")
    except ValueError as e:
        print(f"\n  ⚠  {e}")


def handle_delete():
    """Delete an expense by ID."""
    print("\n  ── Delete Expense ──")
    handle_view_all()
    try:
        expense_id = input("\n  Enter ID to delete (or Enter to cancel): ").strip()
        if not expense_id:
            return
        deleted = delete_expense(expense_id)
        print(f"\n  ✓ Deleted: #{deleted['id']} | ₹{deleted['amount']} | {deleted['category']}")
        log_activity(f"Deleted expense #{deleted['id']}: ₹{deleted['amount']} [{deleted['category']}]")
    except ValueError as e:
        print(f"\n  ⚠  {e}")


def handle_budget_view():
    """Show current monthly budgets."""
    print("\n  ── Monthly Budgets ──")
    budgets = load_budgets()
    separator()
    print(f"  {'Category':<18} {'Budget':>12}")
    separator()
    for cat, amount in budgets.items():
        print(f"  {cat:<18} ₹{amount:>11.2f}")
    separator()


def handle_budget_edit():
    """Edit the budget for a category."""
    print("\n  ── Edit Budget ──")
    handle_budget_view()
    try:
        print("\n  Choose category to update:")
        category = pick_category()
        budgets  = load_budgets()
        current  = budgets.get(category, 0)
        print(f"  Current budget for {category}: ₹{current:.2f}")
        new_val  = float(input("  New budget (₹): ").strip())
        budgets[category] = new_val
        save_budgets(budgets)
        print(f"\n  ✓ Budget for {category} updated to ₹{new_val:.2f}")
        log_activity(f"Updated budget: {category} → ₹{new_val:.2f}")
    except ValueError as e:
        print(f"\n  ⚠  {e}")


def handle_monthly_summary():
    """Show a quick budget vs actual summary for a month."""
    print("\n  ── Monthly Summary ──")
    try:
        year, month = get_month_input()
        summary     = get_monthly_summary(year, month)
        budgets     = load_budgets()
        month_name  = datetime(year, month, 1).strftime("%B %Y")
        total       = sum(summary.values())

        print(f"\n  Summary for {month_name}  |  Total: ₹{total:.2f}")
        separator()
        print(f"  {'Category':<16} {'Spent':>10}  {'Budget':>10}  {'Used':>6}")
        separator()
        for cat in CATEGORIES:
            spent  = summary.get(cat, 0)
            budget = budgets.get(cat, 0)
            pct    = (spent / budget * 100) if budget > 0 else 0
            bar    = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
            flag   = " ⚠" if spent > budget else ""
            print(f"  {cat:<16} ₹{spent:>9.2f}  ₹{budget:>9.2f}  {bar}{flag}")
        separator()
    except ValueError as e:
        print(f"\n  ⚠  {e}")


def handle_generate_report():
    """Generate and save a monthly report as a .txt file."""
    print("\n  ── Generate Report ──")
    try:
        year, month    = get_month_input()
        print("  Generating report…")
        report_path    = generate_report(year, month)
        print(f"\n  ✓ Report saved to: {report_path}")

        show = input("  Preview report? (y/n): ").strip().lower()
        if show == "y":
            print()
            with open(report_path, "r", encoding="utf-8") as f:
                print(f.read())
    except ValueError as e:
        print(f"\n  ⚠  {e}")


def handle_view_log():
    """Display recent activity log entries."""
    print("\n  ── Recent Activity Log ──")
    entries = read_log(last_n=15)
    if not entries:
        print("  No activity logged yet.")
        return
    separator()
    for entry in entries:
        print(" ", entry.rstrip())
    separator()


# ─── MENU ─────────────────────────────────────────────────────────────────────

MENU_ITEMS = [
    ("EXPENSES",       None),
    ("Add expense",    handle_add),
    ("View all",       handle_view_all),
    ("View by month",  handle_view_month),
    ("View by category", handle_view_category),
    ("Delete expense", handle_delete),
    ("BUDGETS",        None),
    ("View budgets",   handle_budget_view),
    ("Edit a budget",  handle_budget_edit),
    ("REPORTS",        None),
    ("Monthly summary",    handle_monthly_summary),
    ("Generate report",    handle_generate_report),
    ("View activity log",  handle_view_log),
]


def print_menu():
    print()
    separator("═")
    print("       💰  Personal Expense Tracker")
    separator("═")
    n = 1
    for label, handler in MENU_ITEMS:
        if handler is None:
            print(f"\n  ── {label} ──")
        else:
            print(f"   {n}. {label}")
            n += 1
    print()
    print("   0. Exit")
    separator("═")


def main():
    setup_dirs()
    log_activity("App started")

    # Build number → handler mapping (skip section headers)
    handlers = {str(i): h for i, (_, h) in enumerate(
        [(l, h) for l, h in MENU_ITEMS if h is not None], start=1
    )}

    while True:
        print_menu()
        choice = input("  Choose option: ").strip()

        if choice == "0":
            log_activity("App exited")
            print("\n  Goodbye! 👋\n")
            break

        handler = handlers.get(choice)
        if handler:
            try:
                handler()
            except Exception as e:
                print(f"\n  ❌ Unexpected error: {e}")
            input("\n  Press Enter to continue…")
        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main()
