# overview.py
# This file displays a summary of the current state of the tracker.
# It lists family members and their earnings, all logged expenses,
# and calculates totals for income, expenses, and the remaining balance.

import streamlit as st
import db
from datetime import datetime, timedelta
from utils.actions import Action
from models.family_member import FamilyMember
from models.expense import Expense

def get_week_range(selected_date):
    """Calculate Monday and Sunday of the week for a given date."""
    start_of_week = selected_date - timedelta(days=selected_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week

def get_month_range(selected_date):
    """Calculate first and last day of the month for a given date."""
    start_of_month = selected_date.replace(day=1)
    if start_of_month.month == 12:
        next_month = start_of_month.replace(year=start_of_month.year + 1, month=1)
    else:
        next_month = start_of_month.replace(month=start_of_month.month + 1)
    end_of_month = next_month - timedelta(days=1)
    return start_of_month, end_of_month

def render_overview(session_state, filtered_expenses=None):
    tracker = session_state.expense_tracker

    # Load family members from DB if not cached
    if not hasattr(tracker, 'members') or not tracker.members:
        db_members = db.get_family_members()
        tracker.members = [FamilyMember.from_db_row(row) for row in db_members]

    members = tracker.members

    st.markdown("### 👥 Family Members")
    if members:
        for idx, member in enumerate(members):
            col1, col2 = st.columns([8, 1])
            with col1:
                st.write(f"👤 **{member.name}** — ${member.earnings} ({'Earning' if member.earning_status else 'Not Earning'})")
            with col2:
                if st.button("❌", key=f"del_member_{idx}"):
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
                    tracker.delete_family_member(member)
                    tracker.members = []  # Clear cache to reload fresh data next render
                    st.experimental_rerun()
    else:
        st.info("No family members added yet.")

    # Load expenses from DB if not cached and no filtered_expenses provided
    if filtered_expenses is None:
        if not hasattr(tracker, 'expense_list') or not tracker.expense_list:
            db_expenses = db.get_expenses()
            tracker.expense_list = [Expense.from_db_row(row) for row in db_expenses]
        filtered_expenses = tracker.expense_list

    st.markdown("### 💼 All Expenses")
    if filtered_expenses:
        for idx, expense in enumerate(filtered_expenses):
            col1, col2 = st.columns([9, 1])
            with col1:
                st.write(f"🗓️ {expense.date} — **{expense.category}** — ${expense.value} ({expense.description})")
            with col2:
                if st.button("❌", key=f"del_expense_{idx}"):
                    action = Action(
                        action_type="delete_expense",
                        item={
                            "value": expense.value,
                            "category": expense.category,
                            "description": expense.description,
                            "date": expense.date
                        }
                    )
                    session_state.undo_stack.append(action)
                    session_state.redo_stack.clear()
                    tracker.delete_expense(expense)
                    tracker.rebuild_expense_heap()
                    tracker.expense_list = []  # Clear cache
                    st.experimental_rerun()
    else:
        st.info("No expenses recorded yet.")

    # Financial Summary
    st.markdown("### 📈 Financial Summary")
    total_earnings = tracker.calculate_total_earnings()
    total_expenses = sum(expense.value for expense in filtered_expenses)
    balance = total_earnings - total_expenses

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Earnings", f"${total_earnings}")
    col2.metric("Total Expenses", f"${total_expenses}")
    col3.metric("Balance", f"${balance}")

    st.markdown("---")

    # Section 4 – Weekly Budget Tracker
    st.markdown("### 📅 Weekly Budget Tracker")
    
    selected_week_date = session_state.get("selected_week_date", datetime.today().date())
    selected_week_date = st.date_input("Select a date within the week:", selected_week_date, key="week_selector")
    session_state.selected_week_date = selected_week_date

    week_start, week_end = get_week_range(selected_week_date)
    weekly_limit = session_state.weekly_budget_limit
    weekly_total = sum(expense.value for expense in tracker.expense_list if week_start <= expense.date <= week_end)
    remaining = weekly_limit - weekly_total

    st.markdown(f"🗓️ **Tracking expenses from:** {week_start.strftime('%A, %b %d')} — {week_end.strftime('%A, %b %d')}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Weekly Limit", f"${weekly_limit}")
    col2.metric("Spent This Week", f"${weekly_total}")
    col3.metric("Remaining", f"${remaining}")

    st.markdown("###### 📊 Weekly Budget Usage")
    progress_ratio = weekly_total / weekly_limit if weekly_limit > 0 else 0
    progress_ratio = min(progress_ratio, 1.0)
    st.progress(progress_ratio)

    if remaining > 0:
        st.success("🎯 Great job! You're staying within your weekly budget.")
    else:
        st.warning("⚠️ You've gone over your weekly budget. Let's aim lower next week!")

    st.markdown("---")

    # Section 5 – Monthly Budget Tracker
    st.markdown("### 📅 Monthly Budget Tracker")

    selected_month_date = session_state.get("selected_month_date", datetime.today().date())
    selected_month_date = st.date_input("Select a date within the month:", selected_month_date, key="month_selector")
    session_state.selected_month_date = selected_month_date

    month_start, month_end = get_month_range(selected_month_date)
    monthly_limit = session_state.monthly_budget_limit
    monthly_total = sum(expense.value for expense in tracker.expense_list if month_start <= expense.date <= month_end)
    remaining_monthly = monthly_limit - monthly_total

    st.markdown(f"🗓️ **Tracking expenses from:** {month_start.strftime('%A, %b %d')} — {month_end.strftime('%A, %b %d')}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Monthly Limit", f"${monthly_limit}")
    col2.metric("Spent This Month", f"${monthly_total}")
    col3.metric("Remaining", f"${remaining_monthly}")

    st.markdown("###### 📊 Monthly Budget Usage")
    progress_ratio_month = monthly_total / monthly_limit if monthly_limit > 0 else 0
    progress_ratio_month = min(progress_ratio_month, 1.0)
    st.progress(progress_ratio_month)

    if remaining_monthly < 0:
        st.warning("⚠️ You've exceeded your monthly budget!")
    else:
        st.success("👍 You're within your monthly budget.")

    st.markdown("---")

    # Budget Performance Gamification
    st.markdown("### 🏆 Budget Performance")
    spending_by_date = tracker.get_spending_by_date()
    daily_budget_limit = 50
    under_budget_days = [date for date, total in spending_by_date.items() if total <= daily_budget_limit]
    streak = len(under_budget_days)

    if "streak_badge_shown" not in session_state:
        session_state.streak_badge_shown = False

    if streak >= 3:
        if not session_state.streak_badge_shown:
            st.balloons()
            st.success(f"🔥 Amazing! You've had {streak} days under ${daily_budget_limit}!")
            st.markdown("🏅 **You’ve earned the 'Budget Boss' badge!**")
            session_state.streak_badge_shown = True
        else:
            st.info(f"🏅 You're still holding your Budget Boss badge with {streak} great days!")
    elif streak > 0:
        st.info(f"👍 You're doing well! {streak} days under your daily budget.")
        session_state.streak_badge_shown = False
    else:
        st.warning("💸 Let's aim to stay under budget tomorrow!")
        session_state.streak_badge_shown = False