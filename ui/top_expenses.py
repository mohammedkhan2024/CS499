import streamlit as st
from datetime import datetime
from models.expense import Expense

def render_top_expenses(session_state, n=3):
    """
    Displays the top N expenses in the Family Expense Tracker.
    
    Parameters:
    - session_state: Streamlit's session state holding the tracker object.
    - n: Number of top expenses to display (default is 3).
    """
    tracker = session_state.expense_tracker
    
    # Get raw expense tuples from DB, convert to Expense objects for UI
    db_expenses = tracker.db.get_expenses() if hasattr(tracker, 'db') else []
    # Build Expense objects for all expenses
    expenses = [
        Expense(value=row[1], category=row[2], description=row[3], date=datetime.fromisoformat(row[4]).date()) 
        for row in db_expenses
    ]

    # Refresh the heap with current data and get top N expenses
    tracker.expense_heap = tracker.expense_heap or ExpenseHeap()
    tracker.rebuild_expense_heap()
    top_expenses = tracker.get_top_expenses(n)

    st.markdown(f"### 🏅 Top {n} Expenses")

    if top_expenses:
        for expense in top_expenses:
            st.write(
                f"🗓️ {expense.date} — {expense.category} — "
                f"${expense.value} ({expense.description})"
            )
    else:
        st.info("No expenses recorded yet.")
