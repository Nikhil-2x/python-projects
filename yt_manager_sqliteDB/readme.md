# Youtube Video Manager

A simple Python application to manage YouTube videos using SQLite.

## Features

- Add, update, delete, and list YouTube videos.
- Stores video details (name and duration) in SQLite.

## Requirements

- Python 3.x (SQLite is built-in)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/youtube-video-manager.git
   cd youtube-video-manager
   ```
2. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. The `videos` table is created automatically when the app runs.
2. Use the menu to manage videos:
   ```plaintext
   1. List all videos
   2. Add a video
   3. Update a video
   4. Delete a video
   5. Exit
   ```
3. All operations are saved in the SQLite database.

## Learnings

- Integrating Python with SQLite.
- Implementing CRUD operations.
- Structuring a simple database application.