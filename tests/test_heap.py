import unittest
from datetime import date
from models.tracker import FamilyExpenseTracker

class TestHeap(unittest.TestCase):
    def setUp(self):
        # Setup tracker and add expenses for heap tests
        self.tracker = FamilyExpenseTracker()
        self.tracker.add_expense(50, "Food", "Lunch", date(2025, 5, 15))
        self.tracker.add_expense(100, "Utilities", "Electricity", date(2025, 5, 16))
        self.tracker.add_expense(75, "Food", "Dinner", date(2025, 5, 20))

    def test_get_top_expenses(self):
        # Test if top 2 expenses retrieved are correct
        top_expenses = self.tracker.get_top_expenses(2)
        top_values = sorted([e.value for e in top_expenses], reverse=True)
        self.assertEqual(top_values, [100, 75])  # Top two amounts

if __name__ == "__main__":
    unittest.main()
