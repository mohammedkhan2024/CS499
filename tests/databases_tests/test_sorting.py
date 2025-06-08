import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from datetime import date, timedelta
import db
from models.tracker import FamilyExpenseTracker

class TestSorting(unittest.TestCase):
    def setUp(self):
        # Initialize DB and clear tables before each test for isolation
        db.init_db()
        with db.get_connection() as conn:
            conn.execute("DELETE FROM expenses")
            conn.execute("DELETE FROM family_members")
            conn.commit()

        self.tracker = FamilyExpenseTracker()
        self.tracker.add_family_member("Alice", True, 5000)
        self.tracker.add_family_member("Bob", True, 3000)

        today = date.today()
        self.tracker.add_expense(100, "Food", "Groceries", today.isoformat())
        self.tracker.add_expense(150, "Utilities", "Electricity", today.isoformat())
        self.tracker.add_expense(50, "Food", "Snack", (today - timedelta(days=2)).isoformat())

    def test_sort_by_amount_ascending(self):
        # Fetch all expenses via filter_expenses (wide filter to get all)
        expenses = self.tracker.filter_expenses(
            start_date=date.today() - timedelta(days=365),
            end_date=date.today(),
            categories=["Food", "Utilities", "Transport", "Other"],
            min_amount=0,
            max_amount=1000000
        )
        sorted_expenses = self.tracker.sort_expenses(expenses, "Amount", ascending=True)
        amounts = [expense.value for expense in sorted_expenses]
        self.assertEqual(amounts, sorted(amounts))

    def test_sort_by_date_descending(self):
        expenses = self.tracker.filter_expenses(
            start_date=date.today() - timedelta(days=365),
            end_date=date.today(),
            categories=["Food", "Utilities", "Transport", "Other"],
            min_amount=0,
            max_amount=1000000
        )
        sorted_expenses = self.tracker.sort_expenses(expenses, "Date", ascending=False)
        dates = [expense.date for expense in sorted_expenses]
        self.assertEqual(dates, sorted(dates, reverse=True))

if __name__ == "__main__":
    unittest.main()
