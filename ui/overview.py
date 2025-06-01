# overview.py
# This file displays a summary of the current state of the tracker.
# It lists family members and their earnings, all logged expenses,
# and calculates totals for income, expenses, and the remaining balance.

import streamlit as st
import time
from datetime import datetime, timedelta
from ui.filter_form import render_filter_form
from utils.actions import Action

def get_week_range(selected_date):
    """Given a date, returns the Monday and Sunday of that week."""
    start_of_week = selected_date - timedelta(days=selected_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week

def get_month_range(selected_date):
    """Given a date, returns the first and last day of that month."""
    start_of_month = selected_date.replace(day=1)
    if start_of_month.month == 12:
        next_month = start_of_month.replace(year=start_of_month.year + 1, month=1)
    else:
        next_month = start_of_month.replace(month=start_of_month.month + 1)
    end_of_month = next_month - timedelta(days=1)
    return start_of_month, end_of_month

def render_overview(session_state, filtered_expenses=None):
    tracker = session_state.expense_tracker  # Access the main tracker object from session

    # Use filtered expenses if given, else all expenses
    expenses = filtered_expenses if filtered_expenses is not None else tracker.expense_list

    # Section 1 – Family Members
    st.markdown("### 👥 Family Members")
    if tracker.members:
        for idx, member in enumerate(tracker.members):
            # Two columns: one for info, one for delete button
            col1, col2 = st.columns([8, 1])
            with col1:
                st.write(
                    f"👤 **{member.name}** — ${member.earnings} "
                    f"({'Earning' if member.earning_status else 'Not Earning'})"
                )
            with col2:
                # Delete button for member
                if st.button("❌", key=f"del_member_{idx}"):
                    # Record delete member action for undo
                    action = Action(
                        action_type="delete_member",
                        item={
                            "name": member.name,
                            "earning_status": member.earning_status,
                            "earnings": member.earnings
                        }
                    )
                    session_state.undo_stack.append(action)
                    session_state.redo_stack.clear()

                    # Delete member and rerun app
                    tracker.delete_family_member(member)
                    st.experimental_rerun()
    else:
        # Message when no members have been added yet
        st.info("No family members added yet.")

    st.markdown("---")

    # Section 2 – Expenses
    st.markdown("### 💼 All Expenses")

    # Show the filter UI so users can select filtering options
    render_filter_form(session_state)

    # Get filters from session state or set defaults
    filters = session_state.get("filters", {
        "start_date": datetime.today().date() - timedelta(days=30),
        "end_date": datetime.today().date(),
        "categories": ["Food", "Utilities", "Transport", "Other"],
        "min_amount": 0,
        "max_amount": 10000,
    })

    # Apply filters 
    expenses = tracker.filter_expenses(
        filters["start_date"],
        filters["end_date"],
        filters["categories"],
        filters["min_amount"],
        filters["max_amount"]
    )

    if expenses:
        for idx, expense in enumerate(expenses):
            # Two columns: expense details and delete button
            col1, col2 = st.columns([9, 1])
            with col1:
                st.write(
                    f"🗓️ {expense.date} — **{expense.category}** — "
                    f"${expense.value} ({expense.description})"
                )
            with col2:
                # Delete button for expense
                if st.button("❌", key=f"del_expense_{idx}"):
                    # Record delete expense action for undo
                    action = Action(
                        action_type="delete_expense",
                        item={
                            "value": expense.value,
                            "category": expense.category,
                            "description": expense.description,
                            "date": expense.date
                        }
                    )
                    session_state.undo_stack.append(action) # Push undo action
                    session_state.redo_stack.clear() # Clear redo stack on new action

                    # Delete expense and rebuild heap for sync
                    tracker.delete_expense(expense)
                    tracker.rebuild_expense_heap()
                    st.experimental_rerun()
    else:
        # Message when no expenses are recorded
        st.info("No expenses recorded yet.")

    st.markdown("---")

    # Section 3 – Financial Summary
    st.markdown("### 📈 Financial Summary")

    # Calculate and display key financial metrics
    total_earnings = tracker.calculate_total_earnings()
    total_expenses = sum(expense.value for expense in expenses)  # filtered expenses here
    balance = total_earnings - total_expenses

    # Use columns to display summary metrics side by side
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Earnings", f"${total_earnings}")
    col2.metric("Total Expenses", f"${total_expenses}")
    col3.metric("Balance", f"${balance}")

    st.markdown("---")

    # Section 4 – Weekly Budget Tracker
    st.markdown("### 📅 Weekly Budget Tracker")

    week_start, week_end = get_week_range(session_state.get("selected_week_date", datetime.today().date()))
    selected_week_date = st.date_input("Select a date within the week:", session_state.get("selected_week_date", datetime.today().date()), key="week_selector")
    session_state.selected_week_date = selected_week_date
    week_start, week_end = get_week_range(selected_week_date)

    weekly_limit = session_state.weekly_budget_limit
    weekly_total = sum(
        expense.value for expense in tracker.expense_list
        if week_start <= expense.date <= week_end
    )
    remaining = weekly_limit - weekly_total

    # Show the active week range being evaluated
    st.markdown(f"🗓️ **Tracking expenses from:** {week_start.strftime('%A, %b %d')} — {week_end.strftime('%A, %b %d')}")

    # Display weekly budget metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Weekly Limit", f"${weekly_limit}")
    col2.metric("Spent This Week", f"${weekly_total}")
    col3.metric("Remaining", f"${remaining}")

    # Progress bar visualization of spending relative to budget
    st.markdown("###### 📊 Weekly Budget Usage")
    progress_ratio = weekly_total / weekly_limit if weekly_limit > 0 else 0
    progress_ratio = min(progress_ratio, 1.0)  # Prevent overflow
    st.progress(progress_ratio)

    # Feedback based on whether budget is being followed
    if remaining > 0:
        st.success("🎯 Great job! You're staying within your weekly budget.")
    else:
        st.warning("⚠️ You've gone over your weekly budget. Let's aim lower next week!")

    st.markdown("---")

    # Section 5 – Monthly Budget Tracker
    st.markdown("### 📅 Monthly Budget Tracker")

    month_start, month_end = get_month_range(session_state.get("selected_month_date", datetime.today().date()))
    selected_month_date = st.date_input("Select a date within the month:", session_state.get("selected_month_date", datetime.today().date()), key="month_selector")
    session_state.selected_month_date = selected_month_date
    month_start, month_end = get_month_range(selected_month_date)

    monthly_limit = session_state.monthly_budget_limit
    monthly_total = sum(
        expense.value for expense in tracker.expense_list
        if month_start <= expense.date <= month_end
    )
    remaining_monthly = monthly_limit - monthly_total

    # Show the active month range being evaluated
    st.markdown(f"🗓️ **Tracking expenses from:** {month_start.strftime('%A, %b %d')} — {month_end.strftime('%A, %b %d')}")

    # Display monthly budget, amount spent, and remaining in three side by side metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Monthly Limit", f"${monthly_limit}")
    col2.metric("Spent This Month", f"${monthly_total}")
    col3.metric("Remaining", f"${remaining_monthly}")

    # Insert the monthly spending overview here
    monthly_spending = tracker.get_spending_by_month()

    if monthly_spending:
        # Calculate total spent this month 
        total_spent_this_month = sum(monthly_spending.values())

        # Assume monthly_limit is available from session state
        monthly_limit = session_state.monthly_budget_limit

        # Calculate progress ratio (spent / limit)
        progress_ratio = total_spent_this_month / monthly_limit if monthly_limit > 0 else 0
        progress_ratio = min(progress_ratio, 1.0)

        # Show progress bar with usage visualization
        st.markdown("###### 📊 Monthly Budget Usage")
        progress_ratio_month = monthly_total / monthly_limit if monthly_limit > 0 else 0
        progress_ratio_month = min(progress_ratio_month, 1.0)
        st.progress(progress_ratio_month)


    # Display feedback message based on whether user is over or under budget
    if remaining_monthly < 0:
        st.warning("⚠️ You've exceeded your monthly budget!")
    else:
        st.success("👍 You're within your monthly budget.")

    st.markdown("---")

    # Section 6 – Budget Performance Gamification
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
