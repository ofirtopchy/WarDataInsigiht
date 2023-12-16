import os
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd



def create_database():
    try:
        print("Current working directory:", os.getcwd())

        # Get the full path for the database file
        db_path = os.path.abspath(os.path.join(os.getcwd(), 'alerts.db'))

        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Create a table to store alert data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                date TEXT,
                time TEXT,
                place TEXT,
                alert_type TEXT,
                insert_time time,
                PRIMARY KEY (date, time, place)
            )
        ''')
        print("Table created successfully")

        conn.commit()
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()


def insert_alert_to_database(date, time, place, alert_type):
    try:
        conn = sqlite3.connect(os.path.abspath('alerts.db'))
        cursor = conn.cursor()
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        # Insert the alert data into the database
        cursor.execute('''
            INSERT INTO alerts (date, time, place, alert_type,insert_time) VALUES (?, ?, ?, ?,?)
        ''', (date, time, place, alert_type,current_datetime))

        print("Data inserted successfully")

        conn.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        conn.close()


def scrape_alarm_data():
    url = "https://www.oref.org.il/12481-he/Pakar.aspx"

    # Configure Selenium options to run headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Launch a browser using Selenium
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Wait for the dynamic content to load (adjust the sleep duration as needed)
    driver.implicitly_wait(5)

    # Get the page source after JavaScript has executed
    html_content = driver.page_source

    # Parse HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Print current working directory
    print("Current working directory:", os.getcwd())

    # Print whether 'alerts.db' file is present
    print("Is 'alerts.db' file present:", os.path.isfile('alerts.db'))

    # Find the parent element with class 'ah-notifications'
    notifications_parent = soup.find('div', class_='ah-notifications')

    if notifications_parent:
        # Find all elements with class 'alert_table' and 'alert_type_' within the notifications parent
        alert_tables = notifications_parent.select('[class*="alert_table"]')

        date_element = notifications_parent.find('h3', class_='alertTableDate')
        date_text = date_element.text.strip() if date_element else "N/A"

        # Iterate over each alert table
        for alert_table in alert_tables:
            # Extract date from the text content of h3 element
            # Extract alert type
            alert_type_element = alert_table.find('h4', class_='alertTableCategory')
            alert_type = alert_type_element.text.strip() if alert_type_element else "N/A"

            # Find all elements with class 'alertDetails' within the current alert table
            alert_details = alert_table.find_all('div', class_='alertDetails')

            # Iterate over each alert detail within the current alert table
            for alert_detail in alert_details:
                # Extract data for each alert detail
                time = alert_detail.find('h5', class_='alertTableTime').text.strip()
                place = alert_detail.contents[1].strip() if len(alert_detail.contents) > 1 else ""

                # Print the data for each alert detail
                print(f"Date: {date_text}\nTime: {time}\nPlace: {place}\nAlert Type: {alert_type}\n{'-' * 20}")

                # Insert the alert data into the database
                insert_alert_to_database(date_text, time, place, alert_type)
            break;



    else:
        print("No notifications found.")

    # Close the browser
    driver.quit()


#reading old date
def insert_csv_data_to_database(csv_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Check if the required columns exist
    if 'time' not in df.columns or 'cities' not in df.columns or 'description' not in df.columns or 'date' not in df.columns:
        print("Required columns not found in the CSV file.")
        return

    try:
        conn = sqlite3.connect(os.path.abspath('alerts.db'))
        cursor = conn.cursor()

        # Iterate over rows in the DataFrame
        for index, row in df.iterrows():
            date = row['date']
            time = pd.to_datetime(row['time']).strftime('%H:%M:%S')
            cities = row['cities']
            description = row['description']

            # Insert the alert data into the database
            cursor.execute('''
                INSERT or ignore INTO alerts (date, time, place, alert_type) VALUES (?, ?, ?, ?)
            ''', (date, time, cities, description))

        print("Data inserted successfully")

    except sqlite3.Error as e:
        print("SQLite error:", e)

    finally:
        conn.commit()
        conn.close()

def insert_csv_data_to_database(csv_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Check if the required columns exist
    if 'time' not in df.columns or 'cities' not in df.columns or 'description' not in df.columns:
        print("Required columns not found in the CSV file.")
        return

    try:
        conn = sqlite3.connect(os.path.abspath('alerts.db'))
        cursor = conn.cursor()

        # Iterate over rows in the DataFrame
        for index, row in df.iterrows():
            # Extract the date part from the 'time' column
            date = pd.to_datetime(row['time']).strftime('%Y-%m-%d')
            time = pd.to_datetime(row['time']).strftime('%H:%M:%S')
            cities = row['cities']
            description = row['description']

            # Insert the alert data into the database
            cursor.execute('''
                INSERT or ignore INTO alerts (date, time, place, alert_type) VALUES (?, ?, ?, ?)
            ''', (date, time, cities, description))

        print("Data inserted successfully")

    except sqlite3.Error as e:
        print("SQLite error:", e)

    finally:
        conn.commit()
        conn.close()
def insert_secondary_data_to_database(csv_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path, sep='\t', encoding='utf-16-le')

    # Print column names to check if 'Latitude1' is present
    print("Column Names:", df.columns)

    # Check if the required columns exist
    if 'Latitude1' not in df.columns or 'Longitude1' not in df.columns or 'יישוב' not in df.columns or 'שם מחוז' not in df.columns:
        print("Required columns not found in the CSV file.")
        return

    try:
        conn = sqlite3.connect(os.path.abspath('alerts.db'))
        cursor = conn.cursor()

        # Create a table to store alert data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS location_places (
                Latitude INTEGER,
                Longitude INTEGER,
                name TEXT,
                area TEXT,
                PRIMARY KEY (Latitude, Longitude)
            )
        ''')

        # Iterate over rows in the DataFrame
        for index, row in df.iterrows():
            # Extract the date part from the 'time' column
            Latitude = row['Latitude1']
            Longitude = row['Longitude1']
            name = row['יישוב']
            area = row['שם מחוז']

            # Insert the alert data into the database
            cursor.execute('''
                INSERT OR IGNORE INTO location_places (Latitude, Longitude, name, area) VALUES (?, ?, ?, ?)
            ''', (Latitude, Longitude, name, area))

        print("Data inserted successfully")

    except sqlite3.Error as e:
        print("SQLite error:", e)

    finally:
        conn.commit()
        conn.close()

if __name__ == "__main__":
    # Get the current date and time for logging

    now = datetime.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

    with open('/Users/ofirtopchy/Desktop/logfile.log', 'a') as log_file:
        log_file.write(f"Script executed successfully at: {current_datetime}\n")
        log_file.write('-' * 50 + '\n')

    # # missing data
    # csv_file_path = '/Users/ofirtopchy/Desktop/alarm.csv'
    # # Insert CSV data into the database
    # insert_csv_data_to_database(csv_file_path)

    # # secondary data
    # csv_file_path = '/Users/ofirtopchy/Desktop/Israel_Map_Dots_data.csv'
    # # Insert CSV data into the database
    # insert_secondary_data_to_database(csv_file_path)
