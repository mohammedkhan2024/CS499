import unittest
from datetime import date
from models.tracker import FamilyExpenseTracker

class TestSorting(unittest.TestCase):
    def setUp(self):
        # Setup tracker with some expenses before each test
        self.tracker = FamilyExpenseTracker()
        self.tracker.add_expense(50, "Food", "Lunch", date(2025, 5, 15))
        self.tracker.add_expense(100, "Utilities", "Electricity", date(2025, 5, 16))
        self.tracker.add_expense(75, "Food", "Dinner", date(2025, 5, 20))

    def test_sort_by_amount_ascending(self):
        # Sort expenses by amount in ascending order
        expenses = self.tracker.sort_expenses(self.tracker.expense_list, "Amount", ascending=True)
        amounts = [e.value for e in expenses]
        self.assertEqual(amounts, [50, 75, 100])  # Check order is correct

    def test_sort_by_date_descending(self):
        # Sort expenses by date in descending order
        expenses = self.tracker.sort_expenses(self.tracker.expense_list, "Date", ascending=False)
        dates = [e.date for e in expenses]
        self.assertEqual(dates, [date(2025,5,20), date(2025,5,16), date(2025,5,15)])

if __name__ == "__main__":
    unittest.main()
