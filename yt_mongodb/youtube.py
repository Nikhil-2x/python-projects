from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
from tabulate import tabulate
import os
import csv

# Load environment variables from .env file
try:
    load_dotenv()
except Exception as e:
    print(f"Error loading environment variables: {e}")

# Get the MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB using the URI
try:
    client = MongoClient(MONGO_URI)
    db = client["ytmanager"]
    video_collection = db["videos"]
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()


def add_video(name, time):
    try:
        video_collection.insert_one({"name": name, "time": time})
        print("Video added successfully.")
    except Exception as e:
        print(f"Error adding video: {e}")


def list_videos():
    try:
        videos = video_collection.find()
        table = [["ID", "Name", "Time"]]
        for video in videos:
            table.append([str(video["_id"]), video["name"], video["time"]])
        print(tabulate(table, headers="firstrow", tablefmt="grid"))
    except Exception as e:
        print(f"Error listing videos: {e}")


def update_video(video_id, new_name, new_time):
    try:
        result = video_collection.update_one({'_id': ObjectId(video_id)}, {"$set": {"name": new_name, "time": new_time}})
        if result.matched_count > 0:
            print("Video updated successfully.")
        else:
            print("Video not found.")
    except Exception as e:
        print(f"Error updating video: {e}")


def delete_video(video_id):
    try:
        result = video_collection.delete_one({"_id": ObjectId(video_id)})
        if result.deleted_count > 0:
            print("Video deleted successfully.")
        else:
            print("Video not found.")
    except Exception as e:
        print(f"Error deleting video: {e}")


def export_to_csv(file_name):
    try:
        videos = video_collection.find()
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(["ID", "Name", "Time"])  
            for video in videos:
                writer.writerow([video["_id"], video["name"], video["time"]])
        print(f"Data successfully exported to {file_name}")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")


def main():
    while True:
        print("\n Youtube Manager App")
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
