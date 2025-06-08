import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from datetime import date, timedelta
import db
from models.tracker import FamilyExpenseTracker

class TestFiltering(unittest.TestCase):
    def setUp(self):
        # Initialize DB and clear tables before each test to make sure clean state
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
        self.tracker.add_expense(200, "Food", "Dinner", (today - timedelta(days=10)).isoformat())

    def test_filter_by_category(self):
        filtered = self.tracker.filter_expenses(
            start_date=date.today() - timedelta(days=30),
            end_date=date.today(),
            categories=["Food"],
            min_amount=0,
            max_amount=1000
        )
        self.assertTrue(all(exp.category == "Food" for exp in filtered))
        self.assertEqual(len(filtered), 2)

    def test_filter_by_date_range(self):
        filtered = self.tracker.filter_expenses(
            start_date=date.today() - timedelta(days=5),
            end_date=date.today(),
            categories=["Food", "Utilities", "Transport", "Other"],
            min_amount=0,
            max_amount=1000
        )
        for expense in filtered:
            self.assertTrue(date.today() - timedelta(days=5) <= expense.date <= date.today())

if __name__ == "__main__":
    unittest.main()
