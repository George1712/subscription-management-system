import sqlite3
import os
from pathlib import Path

DB_PATH = Path("data") / "subscription_manager.db"

def get_db_connection():
    os.makedirs(DB_PATH.parent, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    conn = get_db_connection()
    try :
        conn.execute("PRAGMA foreign_keys = ON")
        
        # Create members table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE,
                phone TEXT UNIQUE,
                date_joined DATE DEFAULT (date('now')),
                status TEXT DEFAULT 'Active'
            )
        """)

        # Create plans table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                duration_days INTEGER NOT NULL,
                price REAL NOT NULL,
                is_active BOOLEAN DEFAULT TRUE
            )
        """)

        # Create subscriptions table (Many-to-Many relationship between members and plans)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL,
                plan_id INTEGER NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (member_id) REFERENCES members (id) ON DELETE CASCADE,
                FOREIGN KEY (plan_id) REFERENCES plans (id)
            )
        """)

        # Create payments table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subscription_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                payment_date DATE DEFAULT (date('now')),
                notes TEXT,
                FOREIGN KEY (subscription_id) REFERENCES subscriptions (id)
            )
        """)

        # indexes
        conn.execute("CREATE INDEX IF NOT EXISTS idx_members_status ON members(status)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_subscriptions_end_date ON subscriptions(end_date)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_subscriptions_member_id ON subscriptions(member_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_plans_active ON plans(is_active)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_payments_date ON payments(payment_date)")

        default_plans = [
            ("Monthly Basic", "Limited Access", 30, 50.0),
            ("Monthly Premium", "Unlimited Access", 30, 80.0),
            ("Annual Basic", "Limited Access", 365, 500.0),
            ("Annual Premium", "Unlimited Access", 365, 900.0)
        ]
        for name, description, duration_days, price in default_plans:
            conn.execute("""
                INSERT OR IGNORE INTO plans (name, description, duration_days, price)
                VALUES (?, ?, ?, ?)
            """, (name, description, duration_days, price))
        

        conn.commit()
        print("Database initialized successfully")

    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
        conn.rollback()
    finally:
        conn.close()

def execute_query(query, params=None):
    if params == None:
        params = ()
    conn = get_db_connection()
    try :
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.commit()
        return result
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        conn.rollback()
        return []
    finally:
        conn.close()

def execute_insert(query, params=None):
    if params == None:
        params = ()
    conn = get_db_connection()
    try :
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error executing insert: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

if __name__ != "__main__":
    init_database()


