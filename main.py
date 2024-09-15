# main_script.py
from email_alert import send_email_alert  #  email alert function
from metadata_scanner import scan_downloads_folder  # metadata scanning script
from db_connection import setup_database  # database setup function
import time

def main():
    # Initialize and set up the database
    db = setup_database()
    
    # Monitor the downloads folder for duplicates
    try:
        while True:
            scan_downloads_folder(db)
            time.sleep(10)  # Check every 10 seconds
    except KeyboardInterrupt:
        print("Stopping the script...")
    finally:
        db.close()  # Ensure the database connection is closed on exit

if __name__ == "__main__":
    main()
print("hello")