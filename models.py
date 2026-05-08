import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = "expenses.db"

def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create expenses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendor TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        receipt_image_path TEXT,
        extracted_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

class Expense:
    """Expense record model."""
    
    def __init__(self, vendor, amount, date, category, description="", receipt_image_path="", extracted_text=""):
        self.vendor = vendor
        self.amount = amount
        self.date = date
        self.category = category
        self.description = description
        self.receipt_image_path = receipt_image_path
        self.extracted_text = extracted_text
    
    def save(self):
        """Save expense to database."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO expenses (vendor, amount, date, category, description, receipt_image_path, extracted_text)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (self.vendor, self.amount, self.date, self.category, self.description, self.receipt_image_path, self.extracted_text))
        conn.commit()
        expense_id = cursor.lastrowid
        conn.close()
        return expense_id
    
    @staticmethod
    def get_all():
        """Retrieve all expenses."""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
        expenses = cursor.fetchall()
        conn.close()
        return expenses
    
    @staticmethod
    def get_by_id(expense_id):
        """Retrieve expense by ID."""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        expense = cursor.fetchone()
        conn.close()
        return expense
    
    @staticmethod
    def update(expense_id, vendor, amount, date, category, description):
        """Update an expense record."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE expenses 
        SET vendor=?, amount=?, date=?, category=?, description=?
        WHERE id=?
        """, (vendor, amount, date, category, description, expense_id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete(expense_id):
        """Delete an expense."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_summary_by_category():
        """Get expense totals by category."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT category, SUM(amount) as total, COUNT(*) as count
        FROM expenses
        GROUP BY category
        ORDER BY category
        """)
        summary = cursor.fetchall()
        conn.close()
        return summary
