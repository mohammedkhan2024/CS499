# visualization.py
# This file provides the data visualization components of the Family Expense Tracker app.
# It includes a pie chart showing expenses by category, a bar chart showing total daily
# expenses over time, and a CSV download option for all logged expense data.

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def render_visualization(session_state):
    tracker = session_state.expense_tracker
    expenses = tracker.expense_list

    # Section 1 – Pie Chart for Expense Categories
    st.markdown("### 📊 Expense Breakdown by Category")

    if not expenses:
        # Show a message if no data is available yet
        st.info("No expenses to visualize yet.")
        return

    # Aggregate expense values by category
    data = {}
    for expense in expenses:
        if expense.category in data:
            data[expense.category] += expense.value
        else:
            data[expense.category] = expense.value

    # Create a DataFrame for the pie chart
    df_pie = pd.DataFrame.from_dict(data, orient='index', columns=['Amount']).reset_index()
    df_pie.rename(columns={'index': 'Category'}, inplace=True)

    # Generate pie chart
    fig1, ax1 = plt.subplots()
    ax1.pie(df_pie['Amount'], labels=df_pie['Category'], autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio makes the pie a circle
    st.pyplot(fig1)

    # Section 2 – Bar Chart for Daily Totals
    st.markdown("### 📅 Expenses Over Time (Bar Chart)")

    # Prepare data for the bar chart (sum amounts per date)
    df_bar = pd.DataFrame([{
        "Date": expense.date,
        "Amount": expense.value
    } for expense in expenses])

    df_bar = df_bar.groupby("Date").sum().reset_index()

    # Generate bar chart using seaborn
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.barplot(x="Date", y="Amount", data=df_bar, ax=ax2)
    ax2.set_title("Total Expenses Per Day")
    ax2.set_ylabel("Amount ($)")
    ax2.set_xlabel("Date")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    # Section 3 – CSV Download
    st.markdown("### 📄 Download Your Expense Data")

    # Convert expense list to DataFrame for download
    df_export = pd.DataFrame([{
        "Date": expense.date,
        "Category": expense.category,
        "Amount": expense.value,
        "Description": expense.description
    } for expense in expenses])

    # Convert DataFrame to CSV and encode
    csv = df_export.to_csv(index=False).encode('utf-8')

    # Display download button
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='expense_data.csv',
        mime='text/csv'
    )