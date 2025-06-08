# visualization.py
# Visualization components of Family Expense Tracker.
# Includes pie chart by category, bar chart by date, and CSV export.

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from models.expense import Expense

def render_visualization(session_state, filtered_expenses=None):
    tracker = session_state.expense_tracker

    # Load expenses from DB if no filtered expenses passed
    if filtered_expenses is None:
        # Fetch all expenses from DB if available
        if hasattr(tracker, 'db'):
            db_expenses = tracker.db.get_expenses()
        else:
            db_expenses = []
        # Convert DB rows to Expense objects for clean attribute access
        expenses = [Expense.from_db_row(row) for row in db_expenses]
    else:
        expenses = filtered_expenses

    st.markdown("### 📊 Expense Breakdown by Category")

    if not expenses:
        st.info("No expenses to visualize yet.")
        return

    # Aggregate total amounts by category
    category_totals = {}
    for expense in expenses:
        category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.value

    # Prepare DataFrame for pie chart
    df_pie = pd.DataFrame.from_dict(category_totals, orient='index', columns=['Amount']).reset_index()
    df_pie.rename(columns={'index': 'Category'}, inplace=True)

    # Plot pie chart of expenses by category
    fig1, ax1 = plt.subplots()
    ax1.pie(df_pie['Amount'], labels=df_pie['Category'], autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio for circle
    st.pyplot(fig1)

    st.markdown("### 📅 Expenses Over Time (Bar Chart)")

    # Aggregate total expenses by date for bar chart
    df_bar = pd.DataFrame([{'Date': expense.date, 'Amount': expense.value} for expense in expenses])
    df_bar = df_bar.groupby('Date').sum().reset_index()

    # Plot bar chart with seaborn
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.barplot(x='Date', y='Amount', data=df_bar, ax=ax2)
    ax2.set_title('Total Expenses Per Day')
    ax2.set_ylabel('Amount ($)')
    ax2.set_xlabel('Date')
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    st.markdown("### 📄 Download Your Expense Data")

    # Prepare CSV export of expenses
    df_export = pd.DataFrame([{
        'Date': expense.date,
        'Category': expense.category,
        'Amount': expense.value,
        'Description': expense.description
    } for expense in expenses])

    csv = df_export.to_csv(index=False).encode('utf-8')

    # Download button for CSV file
    st.download_button(
        label='Download CSV',
        data=csv,
        file_name='expense_data.csv',
        mime='text/csv'
    )
