import json

def load_data():
    try:
        with open("youtube.txt", "r") as file:
            return json.load(file)
            
    except FileNotFoundError:
        return []

def save_data(videos):
    with open("youtube.txt", "w") as file:
        json.dump(videos, file)

def list_all_youtube_videos(videos):
    print("\n")
    print("*" * 70)
    for index, video in enumerate(videos, start=1):
        print(f"{index}. {video['name']} - {video['time']}")
    print("\n")
    print("*" * 70)

def add_youtube_video(videos):
    name = input("Enter the name of the video: ")
    time = input("Enter the duration of the video: ")
    videos.append({"name": name, "time": time})
    save_data(videos)

def delete_youtube_video(videos):
    list_all_youtube_videos(videos)
    index = int(input("Enter the video number to be deleted: "))
    if 1 <= index <= len(videos):
        del videos[index-1]
        save_data(videos)
    else:
        print("Invalid index. Please try again")

def update_youtube_video(videos):
    list_all_youtube_videos(videos)
    index = int(input("Enter the video number to be updated: "))    
    if 1 <= index <= len(videos):
        name = input("Enter the name of the video: ")
        time = input("Enter the duration of the video: ")
        videos[index-1] = {"name": name, "time": time}
        save_data(videos)
    else:
        print("Invalid index. Please try again")

def main():
    videos=load_data()
    while True:
        print("\n Youtube Manager | Choose an option:")
        print("1. List all youtube videos")
        print("2. Add a youtube video")
        print("3. Delete a youtube video")
        print("4. Update a youtube video details")
        print("5. Exit the application")
        input_option = input("Enter your choice: ")
        
        match input_option:
            case "1":
                list_all_youtube_videos(videos)
            case "2":  
                add_youtube_video(videos)
            case "3":
                delete_youtube_video(videos)
            case "4":
                update_youtube_video(videos)
            case "5":
                print("Exiting the application")
                break
            case _:
                print("Invalid option. Please try again")
                continue
            
if __name__ == "__main__":
    main()