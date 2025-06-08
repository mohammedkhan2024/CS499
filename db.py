import sqlite3

# Define the database filename
DB_FILE = 'family_expense_tracker.db'

def get_connection():
    """
    Create and return a new SQLite database connection.
    Enables foreign key support for relational integrity.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")  # Make sure foreign keys work
    return conn

import sqlite3
#from datetime import datetime

DB_FILE = 'family_expense_tracker.db'  # Database file name

def get_connection():
    """
    Create and return a new SQLite database connection.
    Enables foreign key support for relational integrity.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key constraints
    return conn

def init_db():
    """
    Initialize the database with required tables if they do not exist.
    Creates 'family_members' and 'expenses' tables with appropriate schema.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Create family_members table with id, name, earning status, and earnings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS family_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                earning_status INTEGER NOT NULL,
                earnings REAL NOT NULL
            )
        ''')

        # Create expenses table with id, value, category, description, date, and member_id foreign key
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                member_id INTEGER,
                FOREIGN KEY(member_id) REFERENCES family_members(id) ON DELETE SET NULL
            )
        ''')

        # Commit the schema changes
        conn.commit()

# ----------------------------------
# CRUD Operations for Family Members
# ----------------------------------

def add_family_member(name, earning_status, earnings):
    """
    Add a new family member.
    earning_status should be boolean; stored as INTEGER (1/0) in DB.
    Returns the inserted member's id.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO family_members (name, earning_status, earnings)
            VALUES (?, ?, ?)
        ''', (name, int(earning_status), earnings))
        conn.commit()
        return cursor.lastrowid

def get_family_members():
    """
    Retrieve all family members.
    Returns a list of tuples: (id, name, earning_status, earnings)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, earning_status, earnings FROM family_members')
        return cursor.fetchall()

def update_family_member(member_id, name=None, earning_status=None, earnings=None):
    """
    Update family member fields selectively.
    Only provided fields are updated.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        updates = []
        params = []
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if earning_status is not None:
            updates.append("earning_status = ?")
            params.append(int(earning_status))
        if earnings is not None:
            updates.append("earnings = ?")
            params.append(earnings)
        params.append(member_id)
        sql = f"UPDATE family_members SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(sql, params)
        conn.commit()

def delete_family_member(member_id):
    """
    Delete a family member by id.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM family_members WHERE id = ?', (member_id,))
        conn.commit()

# ----------------------------
# CRUD Operations for Expenses
# ----------------------------

def add_expense(value, category, description, date_str, member_id=None):
    """
    Add a new expense.
    date_str should be in 'YYYY-MM-DD' ISO format.
    member_id is optional foreign key to family_members.
    Returns the inserted expense's id.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (value, category, description, date, member_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (value, category, description, date_str, member_id))
        conn.commit()
        return cursor.lastrowid

def get_expenses():
    """
    Retrieve all expenses.
    Returns a list of tuples: (id, value, category, description, date, member_id)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, value, category, description, date, member_id FROM expenses')
        return cursor.fetchall()

def update_expense(expense_id, value=None, category=None, description=None, date_str=None, member_id=None):
    """
    Update expense fields selectively.
    Only provided fields are updated.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        updates = []
        params = []
        if value is not None:
            updates.append("value = ?")
            params.append(value)
        if category is not None:
            updates.append("category = ?")
            params.append(category)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        if date_str is not None:
            updates.append("date = ?")
            params.append(date_str)
        if member_id is not None:
            updates.append("member_id = ?")
            params.append(member_id)
        params.append(expense_id)
        sql = f"UPDATE expenses SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(sql, params)
        conn.commit()

def delete_expense(expense_id):
    """
    Delete an expense by id.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
