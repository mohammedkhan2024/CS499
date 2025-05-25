# overview.py
# This file displays a summary of the current state of the tracker.
# It lists family members and their earnings, all logged expenses,
# and calculates totals for income, expenses, and the remaining balance.

import streamlit as st
import time
from datetime import datetime, timedelta

def render_overview(session_state):
    tracker = session_state.expense_tracker  # Access the main tracker object from session

    # Section 1 – Family Members
    st.markdown("### 👥 Family Members")
    if tracker.members:
        for member in tracker.members:
            # Display member details with earning status
            st.write(
                f"👤 **{member.name}** — ${member.earnings} "
                f"({ 'Earning' if member.earning_status else 'Not Earning' })"
            )
    else:
        # Message when no members have been added yet
        st.info("No family members added yet.")

    st.markdown("---")

    # Section 2 – Expenses
    st.markdown("### 💼 Expenses")
    if tracker.expense_list:
        for expense in tracker.expense_list:
            # Display each recorded expense
            st.write(
                f"🗓️ {expense.date} — **{expense.category}** — "
                f"${expense.value} ({expense.description})"
            )
    else:
        # Message when no expenses are recorded
        st.info("No expenses recorded yet.")

    st.markdown("---")

    # Section 3 – Financial Summary
    st.markdown("### 📈 Financial Summary")

    # Calculate and display key financial metrics
    total_earnings = tracker.calculate_total_earnings()
    total_expenses = tracker.calculate_total_expenditure()
    balance = total_earnings - total_expenses

    # Use columns to display summary metrics side by side
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Earnings", f"${total_earnings}")
    col2.metric("Total Expenses", f"${total_expenses}")
    col3.metric("Balance", f"${balance}")

    st.markdown("---")

    # Section 4 – Weekly Budget Tracker
    st.markdown("### 📅 Weekly Budget Tracker")

    # Calculate total spending this week and compare to budget
    weekly_total = tracker.get_total_expense_this_week()
    weekly_limit = session_state.weekly_budget_limit
    remaining = weekly_limit - weekly_total

    # Define and format the date range being tracked
    today = datetime.today().date()
    week_start = today - timedelta(days=6)
    week_end = today
    formatted_start = week_start.strftime("%A, %b %d")
    formatted_end = week_end.strftime("%A, %b %d")

    # Show the active week range being evaluated
    st.markdown(f"🗓️ **Tracking expenses from:** {formatted_start} — {formatted_end}")

    # Display weekly budget metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Weekly Limit", f"${weekly_limit}")
    col2.metric("Spent This Week", f"${weekly_total}")
    col3.metric("Remaining", f"${remaining}")

    # Progress bar visualization of spending relative to budget
    st.markdown("#### 📊 Budget Usage")
    progress_ratio = weekly_total / weekly_limit if weekly_limit > 0 else 0
    progress_ratio = min(progress_ratio, 1.0)  # Prevent overflow
    st.progress(progress_ratio)

    # Feedback based on whether budget is being followed
    if remaining > 0:
        st.success("🎯 Great job! You're staying within your weekly budget.")
    else:
        st.warning("⚠️ You've gone over your weekly budget. Let's aim lower next week!")

    st.markdown("---")

    # Section 5 – Budget Performance Gamification
    st.markdown("### 🏆 Budget Performance")

    # Get daily spending grouped by date
    spending_by_date = tracker.get_spending_by_date()

    # Set the per-day budget limit (hardcoded)
    daily_budget_limit = 50

    # Count how many days the user stayed under daily limit
    under_budget_days = [date for date, total in spending_by_date.items() if total <= daily_budget_limit]
    streak = len(under_budget_days)

    # Session flag to avoid re-showing badge pop-up
    if "streak_badge_shown" not in session_state:
        session_state.streak_badge_shown = False

    # Show badge if user has reached a streak
    if streak >= 3:
        if not session_state.streak_badge_shown:
            st.balloons()  # Badge pop-up animation 
            st.success(f"🔥 Amazing! You've had {streak} days under ${daily_budget_limit}!")
            st.markdown("🏅 **You’ve earned the 'Budget Boss' badge!**")
            session_state.streak_badge_shown = True  # Mark badge as shown
        else:
            # Simple message if badge was already shown
            st.info(f"🏅 You're still holding your Budget Boss badge with {streak} great days!")
    elif streak > 0:
        # Motivational message for small streaks
        st.info(f"👍 You're doing well! {streak} days under your daily budget.")
        session_state.streak_badge_shown = False  # Reset if not at badge level
    else:
        # Encouragement to start fresh
        st.warning("💸 Let's aim to stay under budget tomorrow!")
        session_state.streak_badge_shown = False
