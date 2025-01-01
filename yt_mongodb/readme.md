# YouTube Manager Application  

A Python-based application to manage YouTube video details using MongoDB, with features like CRUD operations, CSV export, and printing the data in tabular format.  

## Features  
- Add, update, and delete video details.  
- View videos in a tabular format using `tabulate`.  
- Export video data to a CSV file.  

## Setup  

### Prerequisites  
- Python 3.x  
- MongoDB Atlas account or local MongoDB setup  

### Installation  
1. Clone the repository:  
   
2. Set up a virtual environment:
    
3. Install dependencies:
    ```bash
    pip install -r requirements.txt  
    ```

4. Create a .env file in the project root and add your MongoDB connection string:
    ```
    MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/<database>?retryWrites=true&w=majority
    ```

5. Create a .gitignore file in the project root to ignore important files from being tracked by GitHub.
    ```
    .venv/
    .env
    ```

### Note:
- Credentials (e.g., MONGO_URI) are securely stored in a .env file.
- Ensure your MongoDB credentials are correct and the cluster is accessible.
- The venv/ directory and .env file are ignored in version control using .gitignore(if you will be uploading it to github).