import unittest
from datetime import date
from models.tracker import FamilyExpenseTracker
from utils.actions import Action

class TestUndoRedo(unittest.TestCase):
    def setUp(self):
        # Setup tracker and empty undo/redo stacks for each test
        self.tracker = FamilyExpenseTracker()
        self.undo_stack = []
        self.redo_stack = []

    def test_undo_add_expense(self):
        # Simulate adding an expense and then undoing it
        expense_data = {"value": 50, "category": "Food", "description": "Lunch", "date": date(2025,5,15)}
        action = Action("add_expense", expense_data)
        self.undo_stack.append(action)
        self.tracker.add_expense(**expense_data)

        # Undo the addition by removing the expense
        last_action = self.undo_stack.pop()
        if last_action.action_type == "add_expense":
            for exp in self.tracker.expense_list:
                if (exp.value == last_action.item["value"] and exp.category == last_action.item["category"]):
                    self.tracker.delete_expense(exp)
                    break

        self.assertEqual(len(self.tracker.expense_list), 0)  # Expense list should be empty after undo

if __name__ == "__main__":
    unittest.main()
