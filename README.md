# Personal Expense Tracker (CLI)

A command-line based Personal Expense Tracker built using Python.  
This project demonstrates Python file handling using CSV, JSON, and text files to store and manage expense data.

---

## Features

- Add new expenses
- View all expenses
- Filter expenses by month
- Filter expenses by category
- Delete expenses
- Set and edit category budgets
- Generate monthly reports
- View activity logs

---

## Technologies Used

- Python
- CSV file handling
- JSON file handling
- CLI (Command Line Interface)

---

## Project Structure

expense_tracker/
├── main.py # CLI interface  
├── expenses.py # Expense management logic  
├── reports.py # Report generation  
├── config.py # Configuration and file paths  
├── seed_expenses.py # Sample data generator  
│  
├── data/  
│ ├── expenses.csv # Expense records  
│ └── budgets.json # Budget configuration  
│  
└── reports/  
├── activity.log # Application logs  
└── report_YYYY_MM.txt # Generated reports  

---

## How It Works

The program runs through a CLI menu system.

Users can:

1. Add expenses
2. View expense history
3. Filter expenses by month or category
4. Manage category budgets
5. Generate monthly expense reports

All data is stored locally using file handling instead of a database.

---

## Run the Project

Clone the repository or download the project.

Then run:

```bash
python main.py
