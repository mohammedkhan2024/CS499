# expense.py
# This file defines the Expense class, which stores information about a single expense,
# including its value, category, description, date, and database ID.

from datetime import datetime

class Expense:
    def __init__(self, value, category, description, date, id=None):
        """
        Initialize an Expense object.

        Args:
            value (float): Amount of money spent.
            category (str): Expense category, e.g., Food, Utilities.
            description (str): Optional description of the expense.
            date (datetime.date): Date the expense was incurred.
            id (int, optional): Database ID of the expense. Defaults to None.
        """
        self.value = value
        self.category = category
        self.description = description
        self.date = date
        self.id = id  # Database ID, useful for updates and deletions

    def __str__(self):
        """
        Return a string representation of the Expense object.
        Useful for debugging and display.
        """
        return f"Value: {self.value}, Category: {self.category}, Description: {self.description}, Date: {self.date}, ID: {self.id}"

    @classmethod
    def from_db_row(cls, row):
        """
        Factory method to create an Expense object from a database row.

        Args:
            row (tuple): A database row containing expense data in the format:
                         (id, value, category, description, date, member_id)

        Returns:
            Expense: An instantiated Expense object.
        """
        expense_id = row[0]
        value = row[1]
        category = row[2]
        description = row[3]
        date_str = row[4]
        # Convert date string to datetime.date object if necessary
        if isinstance(date_str, str):
            date = datetime.fromisoformat(date_str).date()
        else:
            date = date_str

        return cls(value, category, description, date, id=expense_id)
