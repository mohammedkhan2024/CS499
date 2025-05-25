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

# Import modular UI components
from ui.member_form import render_member_form
from ui.expense_form import render_expense_form
from ui.overview import render_overview
from ui.visualization import render_visualization

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

elif selected == "Data Overview":
    # Check if members exist before showing the overview
    if not expense_tracker.members:
        st.info(
            "Start by adding family members to track your expenses together! "
            "Currently, no members have been added. Get started by clicking the 'Add Member' "
            "from the Data Entry Tab."
        )
    else:
        render_overview(session_state)
        
# Render the graphs for visualization of expenses
elif selected == "Data Visualization":
    render_visualization(session_state)
