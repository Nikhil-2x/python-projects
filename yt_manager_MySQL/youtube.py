import pymysql
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MySQL Database Configuration
db_config = {
    "host": os.getenv("MYSQL_HOST"),  # e.g. "localhost" or the server address
    "user": os.getenv("MYSQL_USER"),  # your MySQL username
    "password": os.getenv("MYSQL_PASSWORD"),  # your MySQL password
    "database": os.getenv("MYSQL_DATABASE"),  # your database name
}

# Establish the MySQL connection
def connect_to_db():
    """Establishes a connection to the MySQL database."""
    try:
        connection = pymysql.connect(**db_config)
        #print("Connected to the database.")
        return connection
    except pymysql.MySQLError as e:
        print("Error connecting to the database:", e)
        return None

# Create table if not exists
def create_table():
    connection = connect_to_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS videos (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        time VARCHAR(255) NOT NULL
                    )
                ''')
                connection.commit()
                print("Table created successfully")
        except pymysql.MySQLError as e:
            print("Error creating table:", e)
        finally:
            connection.close()

# CRUD functions

def list_all_youtube_videos():
    connection = connect_to_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM videos")
                # print("\n")
                # print("*" * 70)
                # for row in cursor.fetchall():
                #     print(row)
                # print("\n")
                # print("*" * 70)
                
                rows = cursor.fetchall()
                
                 # Print header
                print("+----+---------------------------+---------------------+")
                print("| id | name                      | time                |")
                print("+----+---------------------------+---------------------+")
                
                # Print each row with wider columns
                for row in rows:
                    print(f"| {row[0]:<2} | {row[1]:<25} | {row[2]:<19} |")
                
                print("+----+---------------------------+---------------------+")
                
        except pymysql.MySQLError as e:
            print("Error fetching records:", e)
        finally:
            connection.close()

def add_youtube_video(name, time):
    connection = connect_to_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO videos (name, time) VALUES (%s, %s)"
                cursor.execute(sql, (name, time))
                connection.commit()
                print("Video details added successfully")
        except pymysql.MySQLError as e:
            print("Error adding record:", e)
        finally:
            connection.close()

def update_youtube_video(id, name, time):
    connection = connect_to_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE videos SET name = %s, time = %s WHERE id = %s"
                cursor.execute(sql, (name, time, id))
                connection.commit()
                print("Video details updated successfully")
        except pymysql.MySQLError as e:
            print("Error updating record:", e)
        finally:
            connection.close()

def delete_youtube_video(id):
    connection = connect_to_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM videos WHERE id = %s"
                cursor.execute(sql, (id,))
                connection.commit()
                print("Video details deleted successfully")
        except pymysql.MySQLError as e:
            print("Error deleting record:", e)
        finally:
            connection.close()

# Main function to interact with the user
def main():
    # Create the table
    create_table()

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
        
    # Close connection to MySQL
    # con.close()

if __name__ == "__main__":
    main()
