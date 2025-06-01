import unittest
from datetime import date
from models.tracker import FamilyExpenseTracker

class TestFiltering(unittest.TestCase):
    def setUp(self):
        # Create a new tracker and add sample expenses before each test
        self.tracker = FamilyExpenseTracker()
        self.tracker.add_expense(50, "Food", "Lunch", date(2025, 5, 15))
        self.tracker.add_expense(100, "Utilities", "Electricity", date(2025, 5, 16))
        self.tracker.add_expense(75, "Food", "Dinner", date(2025, 5, 20))

    def test_filter_by_category(self):
        # Test filtering only "Food" category expenses
        filtered = self.tracker.filter_expenses(
            start_date=date(2025,5,1),
            end_date=date(2025,5,31),
            categories=["Food"],
            min_amount=0,
            max_amount=200
        )
        self.assertEqual(len(filtered), 2)  # Expect 2 Food expenses
        for expense in filtered:
            self.assertEqual(expense.category, "Food")  # All should be Food

    def test_filter_by_date_range(self):
        # Test filtering expenses within a specific date range
        filtered = self.tracker.filter_expenses(
            start_date=date(2025,5,15),
            end_date=date(2025,5,16),
            categories=["Food", "Utilities"],
            min_amount=0,
            max_amount=200
        )
        self.assertEqual(len(filtered), 2)  # Both expenses fall in this date range

if __name__ == "__main__":
    unittest.main()
