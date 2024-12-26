import pymysql
import bcrypt
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()

db_config = {
    "host": os.getenv("MYSQL_HOST"),  # e.g. "localhost" or the server address
    "user": os.getenv("MYSQL_USER"),  # your MySQL username
    "password": os.getenv("MYSQL_PASSWORD"),  # your MySQL password
    "database": os.getenv("MYSQL_DATABASE"),  # your database name
}

# Database connection
connection = pymysql.connect(**db_config)
cursor = connection.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_logged_in BOOLEAN DEFAULT FALSE,
    is_locked BOOLEAN DEFAULT FALSE,
    failed_attempts INT DEFAULT 0,
    lock_until TIMESTAMP NULL DEFAULT NULL,
    last_active DATETIME DEFAULT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS login_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

connection.commit()

# Utility functions
def print_header(title):
    print("\n" + "=" * 70)
    print(f"{title.center(70)}")
    print("=" * 70)

def confirm_action(message):
    return input(f"{message} (y/n): ").lower() == 'y'

# Features
def register_user():
    print_header("Register New User")
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    # Hash the password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        connection.commit()
        print("\n✅ Registration successful!")
    except pymysql.IntegrityError:
        print("\n❌ Username already exists. Please choose another.")

def login_user():
    print_header("User Login")
    username = input("Enter username: ")
    password = input("Enter password: ")

    cursor.execute("SELECT id, password_hash, is_logged_in, is_locked, lock_until FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        user_id, password_hash, is_logged_in, is_locked, lock_until = result

        if is_locked:
            print("\n❌ Account is locked. Please contact an administrator.")
            cursor.execute("INSERT INTO login_history (username, status) VALUES (%s, 'Failed: Account Locked')", (username,))
            connection.commit()
            return

        if lock_until and lock_until > datetime.now():
            print(f"\n❌ Account is temporarily locked until {lock_until.strftime('%Y-%m-%d %H:%M:%S')}.")
            cursor.execute("INSERT INTO login_history (username, status) VALUES (%s, 'Failed: Account Temporarily Locked')", (username,))
            connection.commit()
            return

        if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            if is_logged_in:
                print("\n✅ User is already logged in.")
                cursor.execute("UPDATE users SET last_active = %s WHERE id = %s", (datetime.now(), user_id))
                connection.commit()
            else:
                cursor.execute("UPDATE users SET is_logged_in = TRUE, failed_attempts = 0, lock_until = NULL, last_active = %s WHERE id = %s", (datetime.now(), user_id,))
                connection.commit()
                print("\n✅ Login successful!")
                cursor.execute("INSERT INTO login_history (username, status) VALUES (%s, 'Successful')", (username,))
                connection.commit()
        else:
            failed_attempts = 1
            cursor.execute("SELECT failed_attempts FROM users WHERE id = %s", (user_id,))
            failed_attempts += cursor.fetchone()[0]
            lock_until = None

            if failed_attempts >= 3:
                lock_until = datetime.now() + timedelta(minutes=5)
                cursor.execute("UPDATE users SET failed_attempts = %s, lock_until = %s WHERE id = %s", (failed_attempts, lock_until, user_id))
                connection.commit()
                print("\n❌ Too many failed attempts. Account temporarily locked.")
            else:
                cursor.execute("UPDATE users SET failed_attempts = %s WHERE id = %s", (failed_attempts, user_id))
                connection.commit()
                print("\n❌ Incorrect password. Try again.")
            cursor.execute("INSERT INTO login_history (username, status) VALUES (%s, 'Failed: Incorrect Password')", (username,))
            connection.commit()
    else:
        print("\n❌ Username not found.")
        cursor.execute("INSERT INTO login_history (username, status) VALUES (%s, 'Failed: Username Not Found')", (username,))
        connection.commit()

def logout_user():
    print_header("User Logout")
    username = input("Enter username: ")

    cursor.execute("SELECT id, is_logged_in FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        user_id, is_logged_in = result
        if is_logged_in:
            cursor.execute("UPDATE users SET is_logged_in = FALSE, last_active =%s WHERE id = %s", (datetime.now(), user_id,))
            connection.commit()
            print("\n✅ Logout successful!")
        else:
            print("\n❌ User is not logged in.")
    else:
        print("\n❌ Username not found.")

def view_all_users():
    print_header("All Registered Users")
    cursor.execute("SELECT id, username, is_logged_in, is_locked FROM users")
    users = cursor.fetchall()

    if users:
        print(f"{'ID':<5}{'Username':<20}{'Logged In':<15}{'Locked':<10}")
        print("-" * 70)
        for user in users:
            print(f"{user[0]:<5}{user[1]:<20}{'Yes' if user[2] else 'No':<15}{'Yes' if user[3] else 'No':<10}")
    else:
        print("\nNo registered users.")

def lock_unlock_user():
    print_header("Lock/Unlock User Account")
    username = input("Enter the username to lock/unlock: ")

    cursor.execute("SELECT id, is_locked FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        user_id, is_locked = result
        new_status = not is_locked
        action = "lock" if new_status else "unlock"

        if confirm_action(f"Do you want to {action} this account?"):
            cursor.execute("UPDATE users SET is_locked = %s WHERE id = %s", (new_status, user_id))
            connection.commit()
            print(f"\n✅ User account has been {action}ed successfully!")
        else:
            print(f"\n{action.capitalize()} action cancelled.")
    else:
        print("\n❌ Username not found.")

def view_login_history():
    print_header("User Login History")
    cursor.execute("SELECT * FROM login_history ORDER BY timestamp DESC")
    logs = cursor.fetchall()

    if logs:
        print(f"{'ID':<5}{'Username':<20}{'Status':<30}{'Timestamp':<25}")
        print("-" * 85)
        for log in logs:
            print(f"{log[0]:<5}{log[1]:<20}{log[2]:<30}{log[3]:<25}")
    else:
        print("\nNo login history available.")
        

def change_password():
    print_header("Change Password")
    username = input("Enter your username: ")
    old_password = input("Enter your current password: ")

    cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        user_id, password_hash = result

        if bcrypt.checkpw(old_password.encode('utf-8'), password_hash.encode('utf-8')):
            new_password = input("Enter your new password: ")
            confirm_password = input("Confirm your new password: ")

            if new_password == confirm_password:
                new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", (new_password_hash, user_id))
                connection.commit()
                print("\n✅ Password changed successfully!")
            else:
                print("\n❌ Passwords do not match. Try again.")
        else:
            print("\n❌ Incorrect current password.")
    else:
        print("\n❌ Username not found.")

def reset_failed_attempts():
    print_header("Reset Failed Login Attempts")
    username = input("Enter the username: ")

    cursor.execute("SELECT id, failed_attempts FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        user_id, failed_attempts = result

        if confirm_action(f"Reset failed login attempts for {username}?"):
            cursor.execute("UPDATE users SET failed_attempts = 0, lock_until = NULL WHERE id = %s", (user_id,))
            connection.commit()
            print("\n✅ Failed login attempts reset successfully!")
        else:
            print("\n❌ Action cancelled.")
    else:
        print("\n❌ Username not found.")

def check_account_status():
    print_header("Check Account Lock Status")
    username = input("Enter your username: ")

    cursor.execute("SELECT is_locked, lock_until FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        is_locked, lock_until = result

        if is_locked:
            print("\n❌ Your account is locked.")
            if lock_until:
                print(f"It will be unlocked on {lock_until.strftime('%Y-%m-%d %H:%M:%S')}.")
        else:
            print("\n✅ Your account is unlocked.")
    else:
        print("\n❌ Username not found.")

def auto_logout_inactive_users():
    print_header("Auto Logout Inactive Users")
    inactivity_duration = int(input("Enter inactivity duration in minutes: "))
    cutoff_time = datetime.now() - timedelta(minutes=inactivity_duration)

    cursor.execute("SELECT id, username FROM users WHERE is_logged_in = TRUE AND last_active < %s", (cutoff_time,))
    inactive_users = cursor.fetchall()

    if inactive_users:
        for user_id, username in inactive_users:
            cursor.execute("UPDATE users SET is_logged_in = FALSE WHERE id = %s", (user_id,))
        connection.commit()
        print("\n✅ All inactive users have been logged out.")
    else:
        print("\n✅ No inactive users found.")
        


# Main menu
def main():
    while True:
        print_header("User Authentication System")
        print("1. Register User")
        print("2. Login User")
        print("3. Logout User")
        print("4. View All Users (Admin)")
        print("5. Lock/Unlock User (Admin)")
        print("6. View Login History (Admin)")
        print("7. Change Password")
        print("8. Reset Failed Login Attempts (Admin)")
        print("9. Check Account Lock Status")
        print("10. Auto Logout Inactive Users (Admin)")
        print("11. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            logout_user()
        elif choice == "4":
            view_all_users()
        elif choice == "5":
            lock_unlock_user()
        elif choice == "6":
            view_login_history()
        elif choice == "7":
            change_password()
        elif choice == "8":
            reset_failed_attempts()
        elif choice == "9":
            check_account_status()
        elif choice == "10":
            auto_logout_inactive_users()
        elif choice == "11":
            print("\n✅ Exiting...")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()