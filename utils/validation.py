# validation.py
# Contains reusable input validation functions for the app.

def validate_member_name(name):
    if not name.strip():
        raise ValueError("Name cannot be empty.")

def validate_earnings(earnings):
    if earnings < 0:
        raise ValueError("Earnings cannot be negative.")

def validate_expense_value(value):
    if value <= 0:
        raise ValueError("Expense value must be greater than zero.")

def validate_category(category):
    if not category.strip():
        raise ValueError("Category must be selected.")
