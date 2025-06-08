# family_member.py
# This file defines the FamilyMember class, which represents a person in the family
# and includes their name, earning status, income amount, and database ID.

class FamilyMember:
    def __init__(self, name, earning_status=True, earnings=0, id=None):
        """
        Initialize a FamilyMember object.

        Args:
            name (str): The name of the family member.
            earning_status (bool): True if the member earns income; otherwise False.
            earnings (float): The amount of income earned (default is 0).
            id (int, optional): The database ID of the family member (default None).
        """
        # The name of the family member
        self.name = name

        # Boolean flag indicating if this member is earning income
        self.earning_status = earning_status

        # Income amount of the family member
        self.earnings = earnings

        # Database ID for CRUD operations
        self.id = id

    def __str__(self):
        """
        Returns a string representation of the member’s details.
        Useful for displaying or debugging.
        """
        earning_str = "Earning" if self.earning_status else "Not Earning"
        return f"Name: {self.name}, Earning Status: {earning_str}, Earnings: {self.earnings}, ID: {self.id}"

    @classmethod
    def from_db_row(cls, row):
        """
        Factory method to create a FamilyMember instance from a database row.

        Args:
            row (tuple): A tuple representing a row from the database in the format
                         (id, name, earning_status, earnings)

        Returns:
            FamilyMember: An instance of FamilyMember with attributes set.
        """
        member_id = row[0]
        name = row[1]
        earning_status = bool(row[2])
        earnings = row[3]

        return cls(name, earning_status, earnings, id=member_id)