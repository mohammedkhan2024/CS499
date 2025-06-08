import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from datetime import date
import db
from models.tracker import FamilyExpenseTracker
from utils.actions import Action
from models.family_member import FamilyMember
from models.expense import Expense
from datetime import datetime

class TestUndoRedo(unittest.TestCase):
    def setUp(self):
        # Initialize DB and clear tables for clean slate
        db.init_db()
        with db.get_connection() as conn:
            conn.execute("DELETE FROM expenses")
            conn.execute("DELETE FROM family_members")
            conn.commit()

        self.tracker = FamilyExpenseTracker()
        # Simulate session state stacks for undo and redo
        self.session_state = {
            "undo_stack": [],
            "redo_stack": []
        }

    def test_undo_add_expense(self):
        today = date.today()
        # Add expense via tracker
        self.tracker.add_expense(100, "Food", "Lunch", today.isoformat())

        # Create and push undo action
        action = Action(
            action_type="add_expense",
            item={
                "value": 100,
                "category": "Food",
                "description": "Lunch",
                "date": today
            }
        )
        self.session_state["undo_stack"].append(action)

        # Undo: remove the expense matching details
        last_action = self.session_state["undo_stack"].pop()
        expenses = self.tracker.db.get_expenses()
        to_delete = None
        for e in expenses:
            # e tuple: (id, value, category, description, date, member_id)
            e_date = datetime.fromisoformat(e[4]).date()
            if (e[1] == last_action.item["value"] and e[2] == last_action.item["category"]
                and e[3] == last_action.item["description"] and e_date == last_action.item["date"]):
                to_delete = e
                break
        if to_delete:
            self.tracker.delete_expense(Expense.from_db_row(to_delete))
            self.tracker.rebuild_expense_heap()

        # Verify expense was removed
        expenses_after = self.tracker.db.get_expenses()
        self.assertFalse(any(e[1] == 100 for e in expenses_after))

    def test_redo_add_expense(self):
        today = date.today()
        # Create redo action (re-adding expense)
        action = Action(
            action_type="add_expense",
            item={
                "value": 150,
                "category": "Transport",
                "description": "Taxi",
                "date": today
            }
        )
        self.session_state["redo_stack"].append(action)

        # Redo: add expense again
        redo_action = self.session_state["redo_stack"].pop()
        self.tracker.add_expense(
            redo_action.item["value"],
            redo_action.item["category"],
            redo_action.item["description"],
            redo_action.item["date"]
        )
        self.tracker.rebuild_expense_heap()

        # Verify expense was added
        expenses = self.tracker.db.get_expenses()
        self.assertTrue(any(e[1] == 150 for e in expenses))

    def test_undo_delete_expense(self):
        today = date.today()
        # Add expense to delete
        self.tracker.add_expense(200, "Utilities", "Electricity", today.isoformat())
        expenses = self.tracker.db.get_expenses()
        exp_to_delete = next(e for e in expenses if e[1] == 200)
        expense_obj = Expense.from_db_row(exp_to_delete)

        # Delete expense
        self.tracker.delete_expense(expense_obj)
        self.tracker.rebuild_expense_heap()

        # Prepare undo action for delete
        action = Action(
            action_type="delete_expense",
            item={
                "value": expense_obj.value,
                "category": expense_obj.category,
                "description": expense_obj.description,
                "date": expense_obj.date
            }
        )
        self.session_state["undo_stack"].append(action)

        # Undo the deletion by re-adding expense
        undo_action = self.session_state["undo_stack"].pop()
        self.tracker.add_expense(
            undo_action.item["value"],
            undo_action.item["category"],
            undo_action.item["description"],
            undo_action.item["date"]
        )
        self.tracker.rebuild_expense_heap()

        # Verify expense is back
        expenses_after = self.tracker.db.get_expenses()
        self.assertTrue(any(e[1] == 200 for e in expenses_after))

    def test_undo_add_member(self):
        # Add a family member
        self.tracker.add_family_member("Alice", True, 5000)

        # Create undo action for add member
        action = Action(
            action_type="add_member",
            item={
                "name": "Alice",
                "earning_status": True,
                "earnings": 5000
            }
        )
        self.session_state["undo_stack"].append(action)

        # Undo: find and delete the member
        last_action = self.session_state["undo_stack"].pop()
        members = self.tracker.db.get_family_members()
        to_delete = None
        for m in members:
            if (m[1] == last_action.item["name"] and m[2] == last_action.item["earning_status"]
                and m[3] == last_action.item["earnings"]):
                to_delete = m
                break
        if to_delete:
            self.tracker.delete_family_member(FamilyMember.from_db_row(to_delete))

        # Verify member is deleted
        members_after = self.tracker.db.get_family_members()
        self.assertFalse(any(m[1] == "Alice" for m in members_after))

    def test_redo_add_member(self):
        # Prepare redo action for adding member
        action = Action(
            action_type="add_member",
            item={
                "name": "Bob",
                "earning_status": False,
                "earnings": 0
            }
        )
        self.session_state["redo_stack"].append(action)

        # Redo: add member again
        redo_action = self.session_state["redo_stack"].pop()
        self.tracker.add_family_member(
            redo_action.item["name"],
            redo_action.item["earning_status"],
            redo_action.item["earnings"]
        )

        # Verify member was added
        members = self.tracker.db.get_family_members()
        self.assertTrue(any(m[1] == "Bob" for m in members))

    def test_undo_delete_member(self):
        # Add member to delete
        self.tracker.add_family_member("Carol", True, 7000)
        members = self.tracker.db.get_family_members()
        mem_to_delete = next(m for m in members if m[1] == "Carol")
        member_obj = FamilyMember.from_db_row(mem_to_delete)

        # Delete the member
        self.tracker.delete_family_member(member_obj)

        # Prepare undo action for delete
        action = Action(
            action_type="delete_member",
            item={
                "name": member_obj.name,
                "earning_status": member_obj.earning_status,
                "earnings": member_obj.earnings
            }
        )
        self.session_state["undo_stack"].append(action)

        # Undo deletion by re-adding member
        undo_action = self.session_state["undo_stack"].pop()
        self.tracker.add_family_member(
            undo_action.item["name"],
            undo_action.item["earning_status"],
            undo_action.item["earnings"]
        )

        # Verify member is back
        members_after = self.tracker.db.get_family_members()
        self.assertTrue(any(m[1] == "Carol" for m in members_after))


if __name__ == "__main__":
    unittest.main()