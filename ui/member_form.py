# member_form.py
# This file defines the UI component for adding a family member.
# It renders a Streamlit form where users can enter a member's name,
# earning status, and earnings. It handles form submission and validation.

import streamlit as st
from utils.validation import validate_member_name, validate_earnings  # Validation functions for input
from utils.logger import logger  # Logger for tracking form actions
from utils.actions import Action  # For undo/redo action tracking

def render_member_form(session_state):
    # Section title
    st.markdown("### 👤 Add Family Member")

    # Collapsible section for the input form
    with st.expander("Add Family Member"):
        # Use columns to organize layout
        col1, col2 = st.columns(2)

        with col1:
            # Input field for member name
            member_name = st.text_input("Name").title()

        with col2:
            # Checkbox to determine if the member is earning income
            earning_status = st.checkbox("Earning Status")

        # Default earnings to 0 unless checkbox is selected
        earnings = 0
        if earning_status:
            # If earning, allow input for earnings amount
            earnings = st.number_input("Earnings", min_value=0, value=0)
        else:
            earnings = 0  # Explicit default when not earning

        # Handle form submission
        if st.button("Add Member"):
            try:
                # Validate name and earnings inputs
                validate_member_name(member_name)
                validate_earnings(earnings)

                # Add the new family member via tracker method which saves to DB
                session_state.expense_tracker.add_family_member(
                    member_name, earning_status, earnings
                )

                # Record this addition as an undoable action
                action = Action(
                    action_type="add_member",
                    item={
                        "name": member_name,
                        "earning_status": earning_status,
                        "earnings": earnings,
                    }
                )
                # Push the action onto the undo stack
                session_state.undo_stack.append(action)
                # Clear redo stack since new action invalidates future redos
                session_state.redo_stack.clear()

                # Clear cached members list in tracker to force UI refresh from DB
                if hasattr(session_state.expense_tracker, 'members'):
                    session_state.expense_tracker.members = []

                # Show confirmation message to user
                st.success("Family member added!")

                # Log the addition event
                logger.info(f"Added member: {member_name}, Earnings: {earnings}, Earning status: {earning_status}")

            except ValueError as e:
                # Show error message and log warning on validation failure
                st.error(f"Error: {e}")
                logger.warning(f"Failed to add member: {e}")
