# member_form.py
# This file defines the UI component for adding a family member.
# It renders a Streamlit form where users can enter a member's name,
# earning status, and earnings. It handles form submission and validation.

import streamlit as st
from utils.validation import validate_member_name, validate_earnings  # Validation functions for input
from utils.logger import logger  # Logger for tracking form actions

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
            earnings = 0  # Redundant but makes logic explicit

        # Handle form submission
        if st.button("Add Member"):
            try:
                # Validate name and earnings
                validate_member_name(member_name)
                validate_earnings(earnings)

                # Add the new family member to the tracker stored in session
                session_state.expense_tracker.add_family_member(
                    member_name, earning_status, earnings
                )

                # Show confirmation message
                st.success("Family member added!")

                # Log the event
                logger.info(f"Added member: {member_name}, Earnings: {earnings}, Earning status: {earning_status}")

            except ValueError as e:
                # Show error message and log it
                st.error(f"Error: {e}")
                logger.warning(f"Failed to add member: {e}")
