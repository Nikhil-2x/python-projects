# Youtube Video Manager

A simple Python-based console application for managing YouTube videos. It uses a text file (`youtube.txt`) to store video details.

## Features

- **List Videos**: View all YouTube videos with their names and durations in a formatted table.
- **Add Video**: Add a new video by entering its name and duration.
- **Delete Video**: Remove a video by selecting its number.
- **Update Video**: Modify the name and duration of an existing video.

## Requirements

- Python 3.x
- No external libraries
- A text file (`youtube.txt`) for data storage (created automatically if not present).

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/youtube-video-manager.git
   cd youtube-video-manager
   ```
2. Run the application:
   ```bash
   python app.py
   ```
3. Use the menu to list, add, delete, or update videos. All changes are saved automatically.

## Example Menu
```plaintext
Youtube Manager | Choose an option:
1. List all youtube videos
2. Add a youtube video
3. Delete a youtube video
4. Update a youtube video details
5. Exit the application
```

## Project Files

- `app.py`: Main application code
- `youtube.txt`: Text file for storing video data