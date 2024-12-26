import sqlite3

con = sqlite3.connect('yt_manager.db')

cursor = con.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                time TEXT NOT NULL
               )
''')

# con.commit()

def list_all_youtube_videos():
    cursor.execute("SELECT * FROM videos")
    rows = cursor.fetchall()
    print("\n")
    # print("*" * 70)
    # for row in cursor.fetchall():
    #     print(row)
    # print("\n")
    # print("*" * 70)
    
    #2nd way of printing the records by designing lol            
    # Print header
    print("+----+---------------------------+---------------------+")
    print("| id | name                      | time                |")
    print("+----+---------------------------+---------------------+")
    
    # Print each row with wider columns
    for row in rows:
        print(f"| {row[0]:<2} | {row[1]:<25} | {row[2]:<19} |")
    
    print("+----+---------------------------+---------------------+")

def add_youtube_video(name, time):
    cursor.execute("INSERT INTO videos (name, time) VALUES (?, ?)", (name, time))
    con.commit()
    print("Video details added successfully")

def update_youtube_video(id, name, time):
    cursor.execute("UPDATE videos SET name = ?, time = ? WHERE id = ?",(name, time, id))
    con.commit()
    print("Video details updated successfully")

def delete_youtube_video(id):
    cursor.execute("DELETE FROM videos WHERE id = ?", (id,))
    con.commit()
    print("Video details deleted successfully")


def main():
    while True:
        print("\n Youtube Manager | Choose an option:")
        print("1. List all youtube videos")
        print("2. Add a youtube video")
        print("3. Update a youtube video details")
        print("4. Delete a youtube video")
        print("5. Exit the application")
        input_option = input("Enter your choice: ")
        
        if input_option == "1":
            list_all_youtube_videos()
        elif input_option == "2":
            name = input("Enter the name of the video: ")
            time = input("Enter the duration of the video: ")
            add_youtube_video(name, time)
        elif input_option == "3":
            id = input("Enter the video number to be updated: ")
            name = input("Enter the name of the video: ")
            time = input("Enter the duration of the video: ")
            update_youtube_video(id, name, time)
        elif input_option == "4":
            id = input("Enter the video number to be deleted: ")
            delete_youtube_video(id)
        elif input_option == "5":
            print("Exiting the application")
            break
        else:
            print("Invalid option. Please try again")
        
    
    con.close()

if __name__ == "__main__":
    main()
