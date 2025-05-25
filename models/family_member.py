# family_member.py
# This file defines the FamilyMember class, which represents a person in the family
# and includes their name, earning status, and income amount.

class FamilyMember:
    def __init__(self, name, earning_status=True, earnings=0):
        # The name of the family member
        self.name = name

        # Boolean flag to indicate if this member is earning an income
        self.earning_status = earning_status

        # The amount of income this family member earns (defaults to 0)
        self.earnings = earnings

    def __str__(self):
        # Returns a string representation of the member’s details.
        # This is useful for displaying the member in the UI or debugging.
        return (
            f"Name: {self.name}, "
            f"Earning Status: {'Earning' if self.earning_status else 'Not Earning'}, "
            f"Earnings: {self.earnings}"
        )
