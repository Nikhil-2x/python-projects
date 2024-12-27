# Youtube Video Manager

A robust Python application for managing YouTube videos using MySQL as the backend database. It includes features for adding, updating, deleting, and listing videos, with credentials securely stored in a `.env` file.

## Features

- **List Videos**: View all YouTube videos with their names and durations in a formatted table.
- **Add Video**: Add a new video by entering its name and duration.
- **Update Video**: Modify the name and duration of an existing video.
- **Delete Video**: Remove a video by selecting its ID.

## Requirements

- Python 3.x
- MySQL Server
- Installed Python libraries:
  - `pymysql`
  - `python-dotenv`

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/youtube-video-manager.git
   cd youtube-video-manager
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure the `.env` file:
   - Create a `.env` file in the project directory with the following variables:
     ```env
     MYSQL_HOST=your_mysql_host
     MYSQL_USER=your_mysql_user
     MYSQL_PASSWORD=your_mysql_password
     MYSQL_DATABASE=your_database_name
     ```
5. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. Upon running the application, the necessary database table (`videos`) will be created automatically if it doesn't already exist.
2. Use the menu to interact with the application:

   ```plaintext
   Youtube Manager | Choose an option:
   1. List all youtube videos
   2. Add a youtube video
   3. Update a youtube video details
   4. Delete a youtube video
   5. Exit the application
   ```
3. Video details are stored in a MySQL database, and operations are performed securely using parameterized queries.

## Project Files

- `app.py`: Main application code
- `.env`: Environment file for database credentials
- `requirements.txt`: Python dependencies

## Example Output

When listing videos, the application displays records in a tabular format:

```plaintext
+----+---------------------------+---------------------+
| id | name                      | time                |
+----+---------------------------+---------------------+
| 1  | Example Video 1           | 10:45               |
| 2  | Example Video 2           | 15:30               |
+----+---------------------------+---------------------+
```

## What We Learn From This Project

- **Python-MySQL Integration**: Learn how to connect a Python application to a MySQL database.
- **Using Environment Variables**: Securely manage sensitive information such as database credentials.
- **CRUD Operations**: Implement Create, Read, Update, and Delete functionality with SQL queries.
- **Error Handling**: Manage exceptions during database operations to make the application robust.
- **Virtual Environments**: Understand the importance of isolating project dependencies.

