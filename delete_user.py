"""
Delete a user and all their associated data from the database.
"""
import sqlite3

db_path = '/Users/homebase/projects/innerwork/db/innerwork.db'
email = 'elliott.w.lee@gmail.com'

def delete_user(email):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"Searching for user: {email}")
    
    # Get user ID
    cursor.execute("SELECT id, name FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    
    if not user:
        print(f"❌ User {email} not found in database.")
        conn.close()
        return
    
    user_id, name = user
    print(f"✓ Found user: {name} (ID: {user_id})")
    
    # Delete all related data
    tables = [
        ('progress', 'user_id'),
        ('purchases', 'user_id'),
        ('enrollments', 'user_id'),
        ('chat_history', 'user_id'),
    ]
    
    for table, column in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {column} = ?", (user_id,))
            count = cursor.fetchone()[0]
            if count > 0:
                cursor.execute(f"DELETE FROM {table} WHERE {column} = ?", (user_id,))
                print(f"✓ Deleted {count} record(s) from {table}")
        except sqlite3.OperationalError as e:
            print(f"  (No {table} table or records)")
    
    # Delete user
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    print(f"✓ Deleted user account: {email}")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ User {email} and all associated data have been removed.")
    print(f"You can now register a new account with this email.")

if __name__ == '__main__':
    delete_user(email)
