# tracker.py
# This file defines the FamilyExpenseTracker class, which manages lists of family members
# and expenses, and provides methods to add, update, delete, and calculate totals.

from models.family_member import FamilyMember
from models.expense import Expense
from collections import defaultdict
from datetime import datetime, timedelta
from models.heap_expenses import ExpenseHeap

class FamilyExpenseTracker:
    def __init__(self):
        # Initialize empty lists for family members, expenses and heap for expenses
        self.members = []
        self.expense_list = []
        self.expense_heap = ExpenseHeap()

    def add_family_member(self, name, earning_status=True, earnings=0):
        # Validates name and adds a new FamilyMember object to the list
        if not name.strip():
            raise ValueError("Name field cannot be empty")
        member = FamilyMember(name, earning_status, earnings)
        self.members.append(member)

    def delete_family_member(self, member):
        # Removes a family member from the list
        self.members.remove(member)

    def update_family_member(self, member, earning_status=True, earnings=0):
        # Updates an existing member's earnings and earning status
        if member:
            member.earning_status = earning_status
            member.earnings = earnings

    def calculate_total_earnings(self):
        # Calculates total income from all members marked as earning
        return sum(
            member.earnings for member in self.members if member.earning_status
        )

    def add_expense(self, value, category, description, date):
        # Validates and adds a new Expense object to the list
        if value == 0:
            raise ValueError("Value cannot be zero")
        if not category.strip():
            raise ValueError("Please choose a category")
        expense = Expense(value, category, description, date)
        self.expense_list.append(expense)
        self.expense_heap.push(expense) 

    def delete_expense(self, expense):
        # Removes an expense from the list
        self.expense_list.remove(expense)

    def calculate_total_expenditure(self):
        # Calculates the total value of all expenses
        return sum(expense.value for expense in self.expense_list)

    def get_spending_by_date(self):
        """
        Groups all expenses by date and returns a dictionary 
        with total amounts spent per date.
        """
        daily_totals = defaultdict(float)
        for expense in self.expense_list:
            daily_totals[str(expense.date)] += expense.value
        return dict(daily_totals)

    def get_total_expense_this_week(self):
        """
        Calculates total expenses over the past 7 days (including today).
        Filters expenses based on their date.
        """
        today = datetime.today().date()
        week_ago = today - timedelta(days=7)

        total = 0
        for expense in self.expense_list:
            expense_date = expense.date

            # Normalize to just the date if it's a datetime object
            if isinstance(expense_date, datetime):
                expense_date = expense_date.date()

            # Include only expenses from within the last 7 days
            if week_ago <= expense_date <= today:
                total += expense.value

        return total
    
    def get_top_expenses(self, n=3):
        # Retrieve top n expenses from the heap
        return self.expense_heap.get_top_n(n)
    
    def rebuild_expense_heap(self):
        """
        Rebuilds the internal expense max-heap from the current expense list.
        Call this after any modification (add/delete) to keep the heap in sync.
        """
        self.expense_heap = ExpenseHeap()
        for expense in self.expense_list:
            self.expense_heap.push(expense)

    
    def filter_expenses(self, start_date, end_date, categories, min_amount, max_amount):
        # Initialize an empty list to hold expenses that meet the filter criteria
        filtered = []

        # Iterate through all expenses stored in the tracker
        for expense in self.expense_list:
            expense_date = expense.date

            # If the expense date is a datetime object, convert it to a date object for consistent comparison
            if isinstance(expense_date, datetime):
                expense_date = expense_date.date()

            # Check if the expense meets all filter criteria:
            # 1. The expense date falls within the specified date range (start_date to end_date)
            # 2. The expense category is one of the selected categories
            # 3. The expense value is within the specified min and max amount range
            if (start_date <= expense_date <= end_date and
                expense.category in categories and
                min_amount <= expense.value <= max_amount):
                # If all conditions are met, add the expense to the filtered list
                filtered.append(expense)

        return filtered
    
    def sort_expenses(self, expenses, sort_option, ascending=True):
        # Dictionary mapping sorting options to key functions
        key_funcs = {
            "Date": lambda x: x.date,
            "Amount": lambda x: x.value,
            "Category": lambda x: x.category.lower(),  # lowercase for consistent alphabetical sorting
        }
        # Select the appropriate key function, default to sorting by date
        key_func = key_funcs.get(sort_option, lambda x: x.date)

        # Return the sorted list, reversing if descending order is requested
        return sorted(expenses, key=key_func, reverse=not ascending)
    
    def get_total_expense_this_month(self):
        # Get today's date
        today = datetime.today().date()

        # Calculate first day of the current month
        start_month = today.replace(day=1)

        total = 0
        # Sum expense values where the expense date falls within the current month
        for expense in self.expense_list:
            expense_date = expense.date
            if isinstance(expense_date, datetime):
                expense_date = expense_date.date()
            if start_month <= expense_date <= today:
                total += expense.value

        return total
    
    def get_spending_by_month(self):
        # Dictionary to hold total spending per month
        monthly_totals = defaultdict(float)

        # Sum all expenses grouped by year and month string
        for expense in self.expense_list:
            expense_date = expense.date
            if isinstance(expense_date, datetime):
                expense_date = expense_date.date()
            month = expense_date.strftime("%Y-%m")
            monthly_totals[month] += expense.value

        return dict(monthly_totals)




