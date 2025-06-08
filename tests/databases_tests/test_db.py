
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from datetime import date
import db

class TestDBOperations(unittest.TestCase):
    def setUp(self):
        # Initialize the database schema
        db.init_db()
        # Clean tables before each test to make sure isolated test environment
        with db.get_connection() as conn:
            conn.execute("DELETE FROM expenses")
            conn.execute("DELETE FROM family_members")
            conn.commit()

    def test_add_and_get_family_member(self):
        # Add a family member and verify it exists in DB
        member_id = db.add_family_member("Alice", True, 5000)
        members = db.get_family_members()
        self.assertTrue(any(m[0] == member_id and m[1] == "Alice" for m in members))

    def test_update_family_member(self):
        # Add then update a family member's earning status and earnings
        member_id = db.add_family_member("Bob", False, 0)
        db.update_family_member(member_id, earning_status=True, earnings=2000)
        members = db.get_family_members()
        updated = next(m for m in members if m[0] == member_id)
        self.assertEqual(updated[2], 1)
        self.assertEqual(updated[3], 2000)

    def test_delete_family_member(self):
        # Add then delete a family member and verify deletion
        member_id = db.add_family_member("Charlie", True, 3000)
        db.delete_family_member(member_id)
        members = db.get_family_members()
        self.assertFalse(any(m[0] == member_id for m in members))

    def test_add_and_get_expense(self):
        # Add an expense and verify it is retrieved correctly
        expense_id = db.add_expense(100, "Food", "Lunch", date.today().isoformat())
        expenses = db.get_expenses()
        self.assertTrue(any(e[0] == expense_id and e[2] == "Food" for e in expenses))

    def test_update_expense(self):
        # Add then update an expense's details
        expense_id = db.add_expense(50, "Transport", "Taxi", date.today().isoformat())
        db.update_expense(expense_id, value=60, category="Transport", description="Uber")
        expenses = db.get_expenses()
        updated = next(e for e in expenses if e[0] == expense_id)
        self.assertEqual(updated[1], 60)
        self.assertEqual(updated[3], "Uber")

    def test_delete_expense(self):
        # Add then delete an expense and verify deletion
        expense_id = db.add_expense(20, "Other", "Snacks", date.today().isoformat())
        db.delete_expense(expense_id)
        expenses = db.get_expenses()
        self.assertFalse(any(e[0] == expense_id for e in expenses))

if __name__ == "__main__":
    unittest.main()