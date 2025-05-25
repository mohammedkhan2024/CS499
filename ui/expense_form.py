# expense_form.py
# This file defines the UI component for logging expenses.
# It provides a form for users to enter expense value, category,
# description, and date. It also handles the submission and displays success or error messages.

import streamlit as st
from utils.validation import validate_expense_value, validate_category  # Validation functions
from utils.logger import logger  # Logger to track expense submissions

def render_expense_form(session_state):
    # Section title
    st.markdown("### 💸 Add Expenses")

    # Collapsible form area
    with st.expander("Add Expenses"):
        # Use columns to organize form layout
        col1, col2 = st.columns(2)

        with col1:
            # Numeric input for the amount of the expense
            expense_value = st.number_input("Value", min_value=0)

        with col2:
            # Dropdown menu for selecting an expense category
            expense_category = st.selectbox("Category", ["Food", "Utilities", "Transport", "Other"])

        # Additional details
        expense_description = st.text_input("Description")  # Optional description
        expense_date = st.date_input("Date")  # Date the expense occurred

        # Handle form submission
        if st.button("Add Expense"):
            try:
                # Validate inputs
                validate_expense_value(expense_value)
                validate_category(expense_category)

                # Add the expense to the tracker stored in session
                session_state.expense_tracker.add_expense(
                    expense_value, expense_category, expense_description, expense_date
                )

                # Show success message
                st.success("Expense added!")

                # Log the event for tracking
                logger.info(f"Added expense: ${expense_value} | {expense_category} | {expense_description} | {expense_date}")

            except ValueError as e:
                # Show error message and log the failure
                st.error(f"Error: {e}")
                logger.warning(f"Failed to add expense: {e}")
