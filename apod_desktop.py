""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py [apod_date]

Parameters:
  apod_date = APOD date (format: YYYY-MM-DD)
"""
import requests
from datetime import date
import os
import sys
import sqlite3
import image_lib
import inspect

# Global variables
NASA_API_KEY = "VOksU5e2ErzjlgVugyY41hEre9WoQI3xCW3l1a5T"
image_cache_dir = None  # Full path of image cache directory
image_cache_db = None   # Full path of image cache database

def main():
    ## DO NOT CHANGE THIS FUNCTION ##
    # Get the APOD date from the command line
    apod_date = get_apod_date()    

    # Get the path of the directory in which this script resides
    script_dir = get_script_dir()

    # Initialize the image cache
    init_apod_cache(script_dir)

    # Add the APOD for the specified date to the cache
    apod_id = add_apod_to_cache(apod_date)

    # Get the information for the APOD from the DB
    apod_info = get_apod_info(apod_id)

    # Set the APOD as the desktop background image
    if apod_id != 0:
        image_lib.set_desktop_background_image(
            apod_info['D:\\script templates\\image_cache\\apod_cache.dbthon'])

def get_apod_date():
    """Gets the APOD date
     
    The APOD date is taken from the first command line parameter.
    Validates that the command line parameter specifies a valid APOD date.
    Prints an error message and exits script if the date is invalid.
    Uses today's date if no date is provided on the command line.

    Returns:
        date: APOD date
    """
    if len(sys.argv) > 1:
        try:
            apod_date = date.fromisoformat(sys.argv[1])
        except ValueError:
            print("Invalid date. Date format: YYYY-MM-DD")
            sys.exit(1)
    else:
        apod_date = date.today()

    return apod_date

def get_script_dir():
    """Determines the path of the directory in which this script resides

    Returns:
        str: Full path of the directory in which this script resides
    """
    ## DO NOT CHANGE THIS FUNCTION ##
    script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
    return os.path.dirname(script_path)


def init_apod_cache(parent_dir):
    """Initializes the image cache by:
    - Determining the paths of the image cache directory and database,
    - Creating the image cache directory if it does not already exist,
    - Creating the image cache database if it does not already exist.
    
    The image cache directory is a subdirectory of the specified parent directory.
    The image cache database is a sqlite database located in the image cache directory.

    Args:
        parent_dir (str): Full path of parent directory    
    """
    global image_cache_dir
    global image_cache_db

    # Determine the path of the image cache directory
    image_cache_dir = os.path.join(parent_dir, "image_cache")

    # Create the image cache directory if it does not already exist
    if not os.path.exists(image_cache_dir):
        os.makedirs(image_cache_dir)

    # Determine the path of image cache DB
    image_cache_db = os.path.join(image_cache_dir, "apod_cache.db")

    # Create the DB if it does not already exist
    if not os.path.exists(image_cache_db):
        conn = sqlite3.connect(image_cache_db)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE apod_images (
                id INTEGER PRIMARY KEY,
                date TEXT UNIQUE,
                title TEXT,
                explanation TEXT,
                file_path TEXT,
                sha256 TEXT
            )
        """)
        conn.commit()
        conn.close()


def add_apod_to_cache(apod_date):
    """Adds the APOD image from a specified date to the image cache.
     
    The APOD information and image file is downloaded from the NASA API.
    If the APOD is not already in the DB, the image file is saved to the 
    image cache and the APOD information is added to the image cache DB.

    Args:
        apod_date (date): Date of the APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if a new APOD is added to the
        cache successfully or if the APOD already exists in the cache. Zero, if unsuccessful.
    """
    print("APOD date:", apod_date.isoformat())
    # Download the APOD information from the NASA API
    api_url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={apod_date.isoformat()}"
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Error: Failed to download APOD from {api_url}")
        return 0

    apod_data = response.json()
    print(f"Retrieved APOD title: {apod_data['title']}")

    # Download the APOD image
    image_url = apod_data['url']
    response = requests.get(image_url)
    if response.status_code != 200:
        print(f"Error: Failed to download image from {image_url}")
        return 0

    # Check whether the APOD already exists in the image cache
    conn = sqlite3.connect("D:\\script templates\\image_cache\\apod_cache.db")
    c = conn.cursor()
    c.execute("SELECT * FROM apod_images WHERE date=?",
              (apod_date.isoformat(),))
    existing_record = c.fetchone()

    if existing_record:
        print("APOD already in cache:", existing_record)
        record_id = existing_record[0]
    else:
        # Save the APOD file to the image cache directory
        image_filename = os.path.basename(image_url)
        image_path = os.path.join(
            "D:\\script templates\\image_cache", image_filename)
        with open(image_path, "wb") as f:
            f.write(response.content)


        # Connect to the database
        conn = sqlite3.connect('D:\\script templates\\image_cache\\apod_cache.db')
        c = conn.cursor()
        # Add the APOD information to the DB
        c.execute("INSERT INTO apod_images (date, title, explanation, url, filename) VALUES (?, ?, ?, ?, ?)",
                  (apod_date.isoformat(), apod_data['title'], apod_data['explanation'], apod_data['url'], image_filename))
        conn.commit()
        record_id = c.lastrowid
        print("Added new APOD to cache:", record_id)

    conn.close()
    return record_id


def add_apod_to_db(title, explanation, file_path, sha256):
    """Adds specified APOD information to the image cache DB.
     
    Args:
        title (str): Title of the APOD image
        explanation (str): Explanation of the APOD image
        file_path (str): Full path of the APOD image file
        sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: The ID of the newly inserted APOD record, if successful.  Zero, if unsuccessful       
    """
    try:
        # Open connection to image cache DB
        conn = sqlite3.connect("image_cache.db")
        cursor = conn.cursor()

        # Insert APOD record into DB
        cursor.execute("INSERT INTO apod (title, explanation, file_path, sha256) VALUES (?, ?, ?, ?)",
                       (title, explanation, file_path, sha256))
        record_id = cursor.lastrowid

        # Commit changes and close DB connection
        conn.commit()
        cursor.close()
        conn.close()

        return record_id

    except Exception as e:
        print("Error adding APOD to DB:", e)
        return 0


def get_apod_id_from_db(image_sha256):
    """
    Gets the record ID of the APOD in the cache having a specified SHA-256 hash value
    
    This function can be used to determine whether a specific image exists in the cache.

    Args:
        image_sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if it exists. Zero, if it does not.
    """
    conn = sqlite3.connect("put the database path")
    c = conn.cursor()

    c.execute("""
        SELECT id FROM apod_cache
        WHERE sha256 = ?
    """, (image_sha256,))

    result = c.fetchone()
    if result:
        return result[0]
    else:
        return 0


def determine_apod_file_path(image_title, image_url):
    # Get the file extension from the image URL
    file_extension = os.path.splitext(image_url)[1]
    # Remove leading/trailing spaces from title and replace inner spaces with underscores
    file_name = '_'.join(image_title.strip().split())
    # Remove all non-alphanumeric characters and underscores from file name
    file_name = ''.join(c for c in file_name if c.isalnum() or c == '_')
    # Construct the full file path
    file_path = os.path.join('C:\\temp\\APOD', f'{file_name}{file_extension}')
    return file_path


def get_apod_info(image_id):
    conn = sqlite3.connect("D:\\script templates\\image_cache\\apod_cache.db")
    c = conn.cursor()
    """Gets the title, explanation, and full path of the APOD having a specified
    ID from the DB.

    Args:
        image_id (int): ID of APOD in the DB

    Returns:
        dict: Dictionary of APOD information
    """
    # Query DB for image info
    c.execute("SELECT title, explanation, file_path FROM apod_images WHERE id=?", (image_id,))
    row = c.fetchone()

    if row is not None:
        # Put information into a dictionary
        apod_info = {
            'title': row[0],
            'explanation': row[1],
            'file_path': row[2],
        }
        return apod_info
    else:
        return None


def get_all_apod_titles():
    """Gets a list of the titles of all APODs in the image cache

    Returns:
        list: Titles of all images in the cache
    """
    # Connect to the database
    conn = sqlite3.connect("D:\\script templates\\image_cache\\apod_cache.db")

    # Create a cursor object
    cursor = conn.cursor()

    # Query the database for all APOD titles
    cursor.execute('SELECT title FROM apod_images')

    # Fetch all results as a list of tuples
    results = cursor.fetchall()

    # Extract the titles from the results
    titles = [result[0] for result in results]

    # Close the cursor and connection to the database
    cursor.close()
    conn.close()

    return titles


if __name__ == '__main__':
    main()