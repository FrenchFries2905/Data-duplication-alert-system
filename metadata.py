import hashlib
import mysql.connector
import os
import time

# Connect to MySQL database
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Adeen@2905",
    database="file_metadata_db"
)

cursor = db.cursor()

def get_file_metadata(file_path):
    """Extracts metadata for a given file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    file_hash = sha256_hash.hexdigest()
    
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    
    return file_name, file_size, file_hash, file_path

def insert_metadata(file_name, file_size, file_hash, file_path):
    """Inserts file metadata into MySQL database"""
    sql = "INSERT INTO file_metadata (file_name, file_size, sha256_hash, file_path) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (file_name, file_size, file_hash, file_path))
    db.commit()

def scan_downloads_folder(folder_path):
    """Scans the Downloads/ folder and processes all files"""
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_name, file_size, file_hash, file_path = get_file_metadata(file_path)

            # Check if the file hash already exists in the database (to avoid duplicates)
            cursor.execute("SELECT * FROM file_metadata WHERE sha256_hash = %s", (file_hash,))
            if cursor.fetchone():
                print(f"Duplicate found: {file_name}")
            else:
                insert_metadata(file_name, file_size, file_hash, file_path)
                print(f"File {file_name} metadata inserted into the database.")

# Specify the Downloads folder path
downloads_folder = os.path.expanduser("~/Downloads")

# Continuous loop to keep checking the folder
while True:
    scan_downloads_folder(downloads_folder)
    # Sleep for 10 seconds before checking again
    time.sleep(10)

# Close the database connection when the script ends (though it won't end in this case)
db.close()
