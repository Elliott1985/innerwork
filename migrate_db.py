"""
Database migration script to add Stripe payment support.
Adds price_cents, duration_label to modules and creates enrollments table.
"""
import sqlite3
import os

db_path = '/Users/homebase/projects/innerwork/db/innerwork.db'

def migrate():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Starting database migration...")
    
    try:
        # Add price_cents column to modules table
        print("Adding price_cents column to modules...")
        cursor.execute("ALTER TABLE modules ADD COLUMN price_cents INTEGER DEFAULT 5900")
        print("✓ Added price_cents column")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("✓ price_cents column already exists")
        else:
            print(f"✗ Error adding price_cents: {e}")
    
    try:
        # Add duration_label column to modules table
        print("Adding duration_label column to modules...")
        cursor.execute("ALTER TABLE modules ADD COLUMN duration_label VARCHAR(50) DEFAULT '4 Modules'")
        print("✓ Added duration_label column")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("✓ duration_label column already exists")
        else:
            print(f"✗ Error adding duration_label: {e}")
    
    try:
        # Create enrollments table
        print("Creating enrollments table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                module_id INTEGER NOT NULL,
                progress INTEGER DEFAULT 0,
                status VARCHAR(20) DEFAULT 'in_progress',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (module_id) REFERENCES modules (id)
            )
        """)
        print("✓ Created enrollments table")
    except sqlite3.OperationalError as e:
        print(f"✗ Error creating enrollments table: {e}")
    
    # Update existing modules with realistic prices
    print("Updating module prices...")
    updates = [
        (4999, "4 Modules", 1),  # I Am Not My Trauma
        (7999, "6 Modules", 2),  # I'm Sorry Is No Longer an Option  
        (6999, "5 Modules", 3),  # Heart & Mind Connection
    ]
    
    for price_cents, duration, module_id in updates:
        try:
            cursor.execute(
                "UPDATE modules SET price_cents = ?, duration_label = ? WHERE id = ?",
                (price_cents, duration, module_id)
            )
            print(f"✓ Updated module {module_id}")
        except Exception as e:
            print(f"✗ Error updating module {module_id}: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Migration completed successfully!")

if __name__ == '__main__':
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        print("Run the app first to create the database.")
    else:
        migrate()
