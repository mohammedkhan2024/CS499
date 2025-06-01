import unittest
from datetime import date, timedelta
from models.tracker import FamilyExpenseTracker

class TestBudgetCalculations(unittest.TestCase):
    def setUp(self):
        # Setup tracker and add expenses to test budget calculations
        self.tracker = FamilyExpenseTracker()
        today = date.today()
        self.tracker.add_expense(50, "Food", "Lunch", today - timedelta(days=15))  # within current month
        self.tracker.add_expense(100, "Food", "Dinner", today - timedelta(days=5))  # within last week
        self.tracker.add_expense(75, "Utilities", "Electricity", today - timedelta(days=1))  # within last week

    def test_total_expense_this_month(self):
        # Test that total expense for the month is calculated correctly
        total = self.tracker.get_total_expense_this_month()
        self.assertEqual(total, 225)  # Sum of all expenses in current month

    def test_total_expense_this_week(self):
        # Assuming today is May 21, 2025, test weekly total calculation
        total = self.tracker.get_total_expense_this_week()
        self.assertEqual(total, 175)  # Expenses in last 7 days only

if __name__ == "__main__":
    unittest.main()
