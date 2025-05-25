# expense.py
# This file defines the Expense class, which stores information about a single expense,
# including its value, category, description, and date.

class Expense:
    def __init__(self, value, category, description, date):
        # Amount of money spent for the expense
        self.value = value
        
        # Category of the expense (e.g., Food, Utilities, Transport)
        self.category = category
        
        # Optional text description of the expense
        self.description = description
        
        # Date the expense was incurred (expected as a datetime.date object)
        self.date = date

    def __str__(self):
        # String representation of the expense — useful for debugging or display
        return f"Value: {self.value}, Category: {self.category}, Description: {self.description}, Date: {self.date}"
