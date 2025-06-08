# tracker.py
# This file defines the FamilyExpenseTracker class, which manages lists of family members
# and expenses, and provides methods to add, update, delete, and calculate totals.

import db 
from models.expense import Expense
from collections import defaultdict
from datetime import datetime, timedelta
from models.heap_expenses import ExpenseHeap

class FamilyExpenseTracker:
    def __init__(self):
        self.db = db 
        self.expense_heap = ExpenseHeap()  # Heap structure to efficiently get top expenses

    def add_family_member(self, name, earning_status=True, earnings=0):
        # Validate that name is not empty
        if not name.strip():
            raise ValueError("Name field cannot be empty")
        # Add new family member to the database where it stores earning_status as integer
        db.add_family_member(name, earning_status, earnings)

    def delete_family_member(self, member):
        # Delete a family member by their database ID
        db.delete_family_member(member.id)

    def update_family_member(self, member, earning_status=True, earnings=0):
        # Update member data in the database, only for provided fields
        db.update_family_member(member.id, earning_status=earning_status, earnings=earnings)

    def calculate_total_earnings(self):
        # Fetch all members from the database
        members = db.get_family_members()
        # Sum earnings for members marked as earning (earning_status == True)
        return sum(member[3] for member in members if member[2])  # member[3]=earnings, member[2]=earning_status boolean

    def add_expense(self, value, category, description, date):
        # Validate input values
        if value == 0:
            raise ValueError("Value cannot be zero")
        if not category.strip():
            raise ValueError("Please choose a category")
        # Convert date object to ISO format string for storage
        date_str = date.isoformat() if isinstance(date, datetime) else date
        # Insert new expense into the database
        db.add_expense(value, category, description, date_str)

    def delete_expense(self, expense):
        # Delete expense from database by its ID
        db.delete_expense(expense.id)

    def calculate_total_expenditure(self):
        # Retrieve all expenses and sum their values
        expenses = db.get_expenses()
        return sum(expense[1] for expense in expenses)  # expense[1] is the value

    def get_spending_by_date(self):
        # Retrieve all expenses and aggregate totals by date
        expenses = db.get_expenses()
        daily_totals = defaultdict(float)
        for expense in expenses:
            # Convert date string back to date object
            date_obj = datetime.fromisoformat(expense[4]).date()
            daily_totals[str(date_obj)] += expense[1]  # expense[1] is the value
        return dict(daily_totals)

    def get_total_expense_this_week(self):
        # Calculate total expenses for the past 7 days including today
        expenses = db.get_expenses()
        today = datetime.today().date()
        week_ago = today - timedelta(days=7)
        total = 0
        for expense in expenses:
            expense_date = datetime.fromisoformat(expense[4]).date()
            if week_ago <= expense_date <= today:
                total += expense[1]
        return total

    def get_total_expense_this_month(self):
        # Calculate total expenses for the current month
        expenses = db.get_expenses()
        today = datetime.today().date()
        start_month = today.replace(day=1)
        total = 0
        for expense in expenses:
            expense_date = datetime.fromisoformat(expense[4]).date()
            if start_month <= expense_date <= today:
                total += expense[1]
        return total

    def get_spending_by_month(self):
        # Aggregate expenses by month (YYYY-MM format) and sum values
        expenses = db.get_expenses()
        monthly_totals = defaultdict(float)
        for expense in expenses:
            expense_date = datetime.fromisoformat(expense[4]).date()
            month = expense_date.strftime("%Y-%m")
            monthly_totals[month] += expense[1]
        return dict(monthly_totals)

    def filter_expenses(self, start_date, end_date, categories, min_amount, max_amount):
        """
        Filters expenses based on provided criteria:
        - Date range between start_date and end_date
        - Expense category in categories list
        - Expense value between min_amount and max_amount
        Returns a list of Expense objects that match the filters.
        """
        expenses = self.db.get_expenses()
        filtered = []
        for row in expenses:
            expense_date = datetime.fromisoformat(row[4]).date()
            if (start_date <= expense_date <= end_date and
                row[2] in categories and
                min_amount <= row[1] <= max_amount):
                filtered.append(Expense.from_db_row(row))
        return filtered

    def sort_expenses(self, expenses, sort_option, ascending=True):
        """
        Sorts a list of Expense objects based on sort_option ('Date', 'Amount', 'Category').
        Returns the sorted list.
        """
        key_funcs = {
            "Date": lambda e: e.date,
            "Amount": lambda e: e.value,
            "Category": lambda e: e.category.lower()
        }
        key_func = key_funcs.get(sort_option, lambda e: e.date)
        return sorted(expenses, key=key_func, reverse=not ascending)

    def get_top_expenses(self, n=3):
        # Rebuild heap from current database expenses to keep it updated
        self.rebuild_expense_heap()
        # Return the top n expenses using the heap
        return self.expense_heap.get_top_n(n)

    def rebuild_expense_heap(self):
        # Clear and rebuild the max-heap with all current expenses
        self.expense_heap = ExpenseHeap()
        expenses = db.get_expenses()
        for expense in expenses:
            # Convert date string to date object for Expense initialization
            expense_date = datetime.fromisoformat(expense[4]).date()
            exp_obj = Expense(expense[1], expense[2], expense[3], expense_date)
            self.expense_heap.push(exp_obj)