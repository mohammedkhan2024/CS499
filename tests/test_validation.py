# test_validation.py
# Unit tests for input validation functions used in form inputs

import unittest
from utils.validation import (
    validate_member_name,
    validate_earnings,
    validate_expense_value,
    validate_category
)

class TestValidation(unittest.TestCase):

    def test_valid_name(self):
        # Should pass silently for a valid name
        validate_member_name("John")

    def test_blank_name_raises_error(self):
        # Should raise ValueError if name is blank
        with self.assertRaises(ValueError):
            validate_member_name("")

    def test_valid_earnings(self):
        # Should pass for non-negative earnings
        validate_earnings(100)

    def test_negative_earnings_raises_error(self):
        # Should raise ValueError if earnings are negative
        with self.assertRaises(ValueError):
            validate_earnings(-10)

    def test_valid_expense_value(self):
        # Should pass for a valid expense value
        validate_expense_value(25)

    def test_zero_expense_value_raises_error(self):
        # Should raise ValueError if value is zero or less
        with self.assertRaises(ValueError):
            validate_expense_value(0)

    def test_valid_category(self):
        # Should pass for a non-empty category
        validate_category("Food")

    def test_blank_category_raises_error(self):
        # Should raise ValueError if category is blank or just spaces
        with self.assertRaises(ValueError):
            validate_category("   ")

# Entry point for test execution
if __name__ == "__main__":
    unittest.main()
