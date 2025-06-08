# expense_form.py
# This file defines the UI component for logging expenses.
# It provides a form for users to enter expense value, category,
# description, and date. It also handles the submission and displays success or error messages.

import streamlit as st
from utils.validation import validate_expense_value, validate_category 
from utils.logger import logger  
from utils.actions import Action 

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

                # Add the expense to the tracker 
                session_state.expense_tracker.add_expense(
                    expense_value, expense_category, expense_description, expense_date
                )

                # Create an action object representing this addition for undo/redo
                action = Action(action_type="add_expense", item={
                    "value": expense_value,
                    "category": expense_category,
                    "description": expense_description,
                    "date": expense_date
                })
                # Push the action onto the undo stack
                session_state.undo_stack.append(action)

                # Clear the redo stack as new action invalidates future redos
                session_state.redo_stack.clear()

                # Clear cached expense list in tracker so UI reloads fresh data from DB
                if hasattr(session_state.expense_tracker, 'expense_list'):
                    session_state.expense_tracker.expense_list = []

                # Show success message to user
                st.success("Expense added!")

                # Log the addition event
                logger.info(f"Added expense: ${expense_value} | {expense_category} | {expense_description} | {expense_date}")

            except ValueError as e:
                # Show error message and log warning in case of validation failure
                st.error(f"Error: {e}")
                logger.warning(f"Failed to add expense: {e}")
