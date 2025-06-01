# app.py
# This is the main entry point for the Family Expense Tracker application.
# It sets up the Streamlit interface, manages session state, handles navigation,
# and renders each UI section including member input, expense entry, financial overview,
# and visual analytics. It also provides a sidebar for budget limit configuration
# and initializes stateful tracking like budget performance.

import streamlit as st
from models.tracker import FamilyExpenseTracker
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from pathlib import Path
from datetime import datetime, timedelta

# Import modular UI components
from ui.member_form import render_member_form
from ui.expense_form import render_expense_form
from ui.overview import render_overview
from ui.visualization import render_visualization
from ui.filter_form import render_filter_form
from ui.top_expenses import render_top_expenses

# Configure the Streamlit page title and icon
st.set_page_config(page_title="Family Expense Tracker", page_icon="💰")
st.title("")  # Clear the default Streamlit title

# Load CSS from styles/main.css
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"

with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

    # Header for clarity
    st.markdown(
        """
        <div style='text-align: center; padding: 30px 0 10px 0;'>
            <h1 style='color: #2b7de9; font-size: 3rem;'>💰 Family Expense Tracker</h1>
            <p style='font-size: 18px; color: #4a4a4a; margin-top: -10px;'>
                Easily manage your family's income and expenses in one place.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Initialize session state for persistent user data
session_state = st.session_state

# Initialize undo and redo stacks to keep track of actions
if "undo_stack" not in session_state:
    session_state.undo_stack = []

if "redo_stack" not in session_state:
    session_state.redo_stack = []

# Undo button in sidebar
if st.sidebar.button("Undo"):
    if session_state.undo_stack:
        # Pop the last action from the undo stack
        last_action = session_state.undo_stack.pop()

        if last_action.action_type == "add_expense":
            # Undo adding an expense, basically find the expense object and remove it
            item = last_action.item
            to_delete = None
            for exp in session_state.expense_tracker.expense_list:
                if (exp.value == item["value"] and exp.category == item["category"]
                    and exp.description == item["description"] and exp.date == item["date"]):
                    to_delete = exp
                    break
            if to_delete:
                session_state.expense_tracker.delete_expense(to_delete)
                
                # Rebuild heap to keep it in sync
                session_state.expense_tracker.rebuild_expense_heap()
        
        # Handle undo for deleting an expense
        elif last_action.action_type == "delete_expense":
            item = last_action.item
            session_state.expense_tracker.add_expense(
                item["value"], item["category"], item["description"], item["date"]
            )
            session_state.expense_tracker.rebuild_expense_heap()

        # Handle undo for adding a member
        elif last_action.action_type == "add_member":
            # Undo adding a member, basically find the member object and remove it
            item = last_action.item
            to_delete = None
            for member in session_state.expense_tracker.members:
                if (member.name == item["name"] and
                    member.earning_status == item["earning_status"] and
                    member.earnings == item["earnings"]):
                    to_delete = member
                    break
            if to_delete:
                session_state.expense_tracker.delete_family_member(to_delete)
        
        # Handle undo for deleting a member
        elif last_action.action_type == "delete_member":
            item = last_action.item
            session_state.expense_tracker.add_family_member(
                item["name"], item["earning_status"], item["earnings"]
            )
        # Push the undone action onto the redo stack for possible redo
        session_state.redo_stack.append(last_action)

    else:
        # Inform the user if there is nothing to undo
        st.sidebar.info("Nothing to undo.")

# Redo button in sidebar
if st.sidebar.button("Redo"):
    if session_state.redo_stack:
        # Pop the last action from the redo stack
        action = session_state.redo_stack.pop()

        if action.action_type == "add_expense":
            # Redo adding an expense by re-adding it
            item = action.item
            session_state.expense_tracker.add_expense(
                item["value"], item["category"], item["description"], item["date"]
            )

            # Rebuild heap after redo add
            session_state.expense_tracker.rebuild_expense_heap()

        # Redo deleting an expense
        elif action.action_type == "delete_expense":
            item = action.item
            to_delete = None
            # Find matching expense to delete
            for exp in session_state.expense_tracker.expense_list:
                if (exp.value == item["value"] and exp.category == item["category"]
                    and exp.description == item["description"] and exp.date == item["date"]):
                    to_delete = exp
                    break
            if to_delete:
                session_state.expense_tracker.delete_expense(to_delete)
                session_state.expense_tracker.rebuild_expense_heap()

        # Redo adding a member
        elif action.action_type == "add_member":
            # Redo adding a member by re-adding it
            item = action.item
            session_state.expense_tracker.add_family_member(
                item["name"], item["earning_status"], item["earnings"]
            )

        elif action.action_type == "delete_member":
            item = action.item
            to_delete = None
            # Find member to delete
            for member in session_state.expense_tracker.members:
                if (member.name == item["name"] and member.earning_status == item["earning_status"]
                    and member.earnings == item["earnings"]):
                    to_delete = member
                    break
            if to_delete:
                session_state.expense_tracker.delete_family_member(to_delete)

        # Push redone action back onto undo stack
        session_state.undo_stack.append(action)

    else:
        # Inform the user if there is nothing to redo
        st.sidebar.info("Nothing to redo.")

# Create the FamilyExpenseTracker object only once per session
if "expense_tracker" not in session_state:
    session_state.expense_tracker = FamilyExpenseTracker()

# Set up the top navigation menu
selected = option_menu(
    menu_title=None,
    options=["Data Entry", "Data Overview", "Data Visualization"],
    icons=[
        "pencil-fill",
        "clipboard2-data",
        "bar-chart-fill",
    ],  # Uses Bootstrap icons
    orientation="horizontal",
)

# Access the tracker object for use throughout this file
expense_tracker = session_state.expense_tracker

# Session state flag to prevent showing the badge multiple times
if "streak_badge_shown" not in session_state:
    session_state.streak_badge_shown = False

# Render the appropriate screen based on the selected menu option
if selected == "Data Entry":
    render_member_form(session_state)        # Form to add family members
    render_expense_form(session_state)       # Form to add expenses

    # Sidebar input for setting weekly budget
    st.sidebar.markdown("### 🔧 Budget Settings")
    if "weekly_budget_limit" not in session_state:
        session_state.weekly_budget_limit = 350  # Default value

    session_state.weekly_budget_limit = st.sidebar.number_input(
        "Set your weekly budget limit ($)",
        min_value=0,
        value=session_state.weekly_budget_limit,
        step=10
    )

    # Monthly budget setting added below weekly budget input
    if "monthly_budget_limit" not in session_state:
        session_state.monthly_budget_limit = 1500  # Default monthly budget

    # Add a number input widget to sidebar to let user set their monthly budget
    session_state.monthly_budget_limit = st.sidebar.number_input(
        "Set your monthly budget limit ($)",
        min_value=0,
        value=session_state.monthly_budget_limit,
        step=50
    )


elif selected == "Data Overview":

    # Pass filtered expenses to the overview render function
    render_overview(session_state)

    # Render top expenses
    render_top_expenses(session_state, n=5)
        
# Render the graphs for visualization of expenses
elif selected == "Data Visualization":
    render_visualization(session_state)
