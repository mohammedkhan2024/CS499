# utils/actions.py
# Defines an Action class to represent changes for undo/redo functionality

class Action:
    def __init__(self, action_type, item, data_before=None):
        """
        Represents a user action that can be undone or redone.

        Parameters:
        - action_type (str): The kind of action, e.g. 'add_expense', 'delete_member'
        - item: The object involved in the action (e.g., Expense or FamilyMember instance)
        - data_before: Snapshot of object state before the action (used for updates or deletes)
        """
        self.action_type = action_type
        self.item = item
        self.data_before = data_before
