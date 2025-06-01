import streamlit as st
from datetime import datetime, timedelta

def render_filter_form(session_state):
    st.markdown("###### 🔎 Filter Expenses")

    # Define default values for filters, used on reset or initial load
    default_start = datetime.today().date() - timedelta(days=30)  # 30 days ago
    default_end = datetime.today().date()  # today
    default_categories = ["Food", "Utilities", "Transport", "Other"]
    default_min_amount = 0
    default_max_amount = 10000

    # Create columns for horizontal layout with specified relative widths
    col_reset, col_start, col_end, col_cat, col_min, col_max = st.columns([2, 2, 2, 4, 1.5, 1.5])

    # Place the Reset Filters button in the first column
    with col_reset:
        if st.button("Reset Filters"):
            # Reset filter values in session state to defaults
            session_state.filters = {
                "start_date": default_start,
                "end_date": default_end,
                "categories": default_categories,
                "min_amount": default_min_amount,
                "max_amount": default_max_amount,
            }
            # Refresh the app immediately to update UI with reset values
            st.experimental_rerun()

    # Retrieve current filter values from session state or empty dict if none set
    filters = session_state.filters if "filters" in session_state else {}

    # Date input for start date placed in second column
    with col_start:
        start_date = st.date_input(
            "Start Date",
            value=filters.get("start_date", default_start)
        )

    # Date input for end date placed in third column
    with col_end:
        end_date = st.date_input(
            "End Date",
            value=filters.get("end_date", default_end)
        )

    # Multi-select for categories placed in wider fourth column
    with col_cat:
        categories = default_categories
        selected_categories = st.multiselect(
            "Categories",
            categories,
            default=filters.get("categories", default_categories)
        )

    # Numeric input for minimum amount placed in fifth column
    with col_min:
        min_amount = st.number_input(
            "Min Amount",
            min_value=0,
            value=filters.get("min_amount", default_min_amount)
        )

    # Numeric input for maximum amount placed in sixth column
    with col_max:
        max_amount = st.number_input(
            "Max Amount",
            min_value=0,
            value=filters.get("max_amount", default_max_amount)
        )

    # Update session state filters with current input values
    session_state.filters = {
        "start_date": start_date,
        "end_date": end_date,
        "categories": selected_categories,
        "min_amount": min_amount,
        "max_amount": max_amount,
    }
