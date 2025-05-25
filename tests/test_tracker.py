# test_tracker.py
# Unit tests for FamilyExpenseTracker class methods

import unittest
from datetime import date, timedelta
from models.tracker import FamilyExpenseTracker

class TestFamilyExpenseTracker(unittest.TestCase):

    def setUp(self):
        # This method runs before each test — creates a new tracker object
        self.tracker = FamilyExpenseTracker()

    def test_add_family_member(self):
        # Add a new member and verify list count and name
        self.tracker.add_family_member("Alice", True, 3000)
        self.assertEqual(len(self.tracker.members), 1)
        self.assertEqual(self.tracker.members[0].name, "Alice")

    def test_calculate_total_earnings(self):
        # Only earning members should count toward total earnings
        self.tracker.add_family_member("Alice", True, 3000)
        self.tracker.add_family_member("Bob", False, 2000)  # Ignored
        total = self.tracker.calculate_total_earnings()
        self.assertEqual(total, 3000)

    def test_add_expense(self):
        # Add an expense and verify the entry was recorded
        self.tracker.add_expense(100, "Food", "Lunch", date.today())
        self.assertEqual(len(self.tracker.expense_list), 1)
        self.assertEqual(self.tracker.expense_list[0].category, "Food")

    def test_calculate_total_expenditure(self):
        # Add multiple expenses and verify sum is accurate
        self.tracker.add_expense(100, "Food", "Lunch", date.today())
        self.tracker.add_expense(50, "Transport", "Bus", date.today())
        total = self.tracker.calculate_total_expenditure()
        self.assertEqual(total, 150)

    def test_get_total_expense_this_week(self):
        # One expense in the last 7 days, one older — only one should count
        today = date.today()
        last_week = today - timedelta(days=3)
        old = today - timedelta(days=10)

        self.tracker.add_expense(100, "Food", "Recent", last_week)
        self.tracker.add_expense(50, "Food", "Too old", old)

        total = self.tracker.get_total_expense_this_week()
        self.assertEqual(total, 100)

# Entry point for test execution
if __name__ == '__main__':
    unittest.main()
