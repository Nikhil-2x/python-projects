# User Authentication System

This is a Python-based user authentication system that uses MySQL for the backend database. It supports user registration, login, logout, password management, account lock/unlock, and activity tracking. The project is designed to be modular and uses secure password hashing with the `bcrypt` library. Environment variables are managed using a `.env` file to store sensitive credentials securely.

## Features

1. **User Registration**
   - Register a new user with a username and password.
   - Passwords are securely hashed using `bcrypt`.

2. **User Login**
   - Authenticate users using their username and password.
   - Prevents login if the account is locked or temporarily locked.
   - Logs each login attempt (successful or failed) into a login history table.

3. **User Logout**
   - Logout currently logged-in users.

4. **View All Users (Admin)**
   - Admins can view all registered users, their login status, and lock status.

5. **Lock/Unlock User Accounts (Admin)**
   - Admins can lock or unlock user accounts manually.

6. **View Login History (Admin)**
   - Displays a history of all login attempts with timestamps and statuses.

7. **Password Management**
   - Users can change their password securely.

8. **Reset Failed Login Attempts (Admin)**
   - Admins can reset the failed login attempts for a user.

9. **Account Lock Status**
   - Users can check their account lock status and unlock times if applicable.

10. **Auto Logout Inactive Users (Admin)**
    - Automatically logs out users inactive for a specified duration.

## Requirements

- Python 3.x
- MySQL server
- Required Python libraries:
  - `pymysql`
  - `bcrypt`
  - `python-dotenv`
  - `cryptography`

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your_username/user-authentication-system.git
   cd user-authentication-system
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the MySQL database**:
   - Create a new MySQL database.
   - Update the `.env` file with your database credentials:
     ```plaintext
     MYSQL_HOST=localhost
     MYSQL_USER=your_username
     MYSQL_PASSWORD=your_password
     MYSQL_DATABASE=your_database
     ```
   - The `.env` file is ignored by Git to keep credentials secure.

5. **Initialize the database**:
   Run the script to create the required tables:
   ```bash
   python main.py
   ```

## Usage

Run the program using:
```bash
python main.py
```

Follow the on-screen menu to use the system:
- Register new users
- Log in and out
- Manage accounts (Admin)
- View login history and other features

## Project Structure

```
user-authentication-system/
├── .env                 # Environment variables for database credentials
├── main.py              # Main program file
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── venv/                # Virtual environment directory
```

## Security Features

- **Password Hashing**: All passwords are hashed using `bcrypt`.
- **Account Locking**: Accounts are locked after 3 failed login attempts for 5 minutes.
- **Environment Variables**: Sensitive credentials are stored in a `.env` file.

```
Feel free to contribute by submitting issues or pull requests to improve this project!
