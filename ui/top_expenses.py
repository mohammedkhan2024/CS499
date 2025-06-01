import streamlit as st

def render_top_expenses(session_state, n=3):
    """
    Displays the top N expenses in the Family Expense Tracker.
    
    Parameters:
    - session_state: Streamlit's session state holding the tracker object.
    - n: Number of top expenses to display (default is 3).
    """
    # Access the tracker object from session state
    tracker = session_state.expense_tracker
    
    # Retrieve the top N expenses using the heap method
    top_expenses = tracker.get_top_expenses(n)

    # Display section title with number of top expenses shown
    st.markdown(f"### 🏅 Top {n} Expenses")

    if top_expenses:
        # Loop through each top expense and display its details
        for expense in top_expenses:
            st.write(
                f"🗓️ {expense.date} — {expense.category} — "
                f"${expense.value} ({expense.description})"
            )
    else:
        # Inform the user if no expenses have been recorded yet
        st.info("No expenses recorded yet.")
