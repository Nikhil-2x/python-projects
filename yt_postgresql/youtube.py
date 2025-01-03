import psycopg2
from psycopg2.extras import RealDictCursor
import csv
from tabulate import tabulate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# PostgreSQL Connection URL
POSTGRES_URL = os.getenv("POSTGRES_URL")

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(POSTGRES_URL, cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Connected to PostgreSQL database.")
except Exception as e:
    print(f"Error connecting to PostgreSQL: {e}")
    exit()

# Ensure the table exists
def create_table():
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                time VARCHAR(50) NOT NULL
            );
        """)
        conn.commit()
    except Exception as e:
        print(f"Error creating table: {e}")

# Add a new video
def add_video(name, time):
    try:
        cursor.execute("INSERT INTO videos (name, time) VALUES (%s, %s)", (name, time))
        conn.commit()
        print("Video added successfully.")
    except Exception as e:
        print(f"Error adding video: {e}")

# List all videos
def list_videos():
    try:
        cursor.execute("SELECT * FROM videos")
        videos = cursor.fetchall()
        table = [["ID", "Name", "Time"]]
        for video in videos:
            table.append([video["id"], video["name"], video["time"]])
        print(tabulate(table, headers="firstrow", tablefmt="grid"))
    except Exception as e:
        print(f"Error listing videos: {e}")

# Update a video
def update_video(video_id, new_name, new_time):
    try:
        cursor.execute(
            "UPDATE videos SET name = %s, time = %s WHERE id = %s",
            (new_name, new_time, video_id)
        )
        conn.commit()
        if cursor.rowcount > 0:
            print("Video updated successfully.")
        else:
            print("Video not found.")
    except Exception as e:
        print(f"Error updating video: {e}")

# Delete a video
def delete_video(video_id):
    try:
        cursor.execute("DELETE FROM videos WHERE id = %s", (video_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print("Video deleted successfully.")
        else:
            print("Video not found.")
    except Exception as e:
        print(f"Error deleting video: {e}")

# Export data to CSV
def export_to_csv(file_name):
    try:
        cursor.execute("SELECT * FROM videos")
        videos = cursor.fetchall()
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(["ID", "Name", "Time"])
            for video in videos:
                writer.writerow([video["id"], video["name"], video["time"]])
        print(f"Data successfully exported to {file_name}")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")

# Main program
def main():
    create_table()
    while True:
        print("\nYoutube Manager App")
        print("1. List all videos")
        print("2. Add a new video")
        print("3. Update a video")
        print("4. Delete a video")
        print("5. Export as a CSV file")
        print("6. Exit the app")
        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                list_videos()
            elif choice == '2':
                name = input("Enter the video name: ")
                time = input("Enter the video time: ")
                add_video(name, time)
            elif choice == '3':
                video_id = input("Enter the video ID to update: ")
                name = input("Enter the updated video name: ")
                time = input("Enter the updated video time: ")
                update_video(video_id, name, time)
            elif choice == '4':
                video_id = input("Enter the video ID to delete: ")
                delete_video(video_id)
            elif choice == '5':
                file_name = input("Enter the file name (with .csv extension): ")
                export_to_csv(file_name)
            elif choice == '6':
                print("Exiting the app. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Critical error: {e}")
