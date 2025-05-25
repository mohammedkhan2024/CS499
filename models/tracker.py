# tracker.py
# This file defines the FamilyExpenseTracker class, which manages lists of family members
# and expenses, and provides methods to add, update, delete, and calculate totals.

from models.family_member import FamilyMember
from models.expense import Expense
from collections import defaultdict
from datetime import datetime, timedelta

class FamilyExpenseTracker:
    def __init__(self):
        # Initialize empty lists for family members and expenses
        self.members = []
        self.expense_list = []

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
