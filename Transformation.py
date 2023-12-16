import sqlite3

import sqlite3

def mirroring():
    conn = sqlite3.connect('alerts.db')
    cursor = conn.cursor()

    # Create a new table to store the copied data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mrr_alert (
            date TEXT,
            time TEXT,
            place TEXT,
            alert_type TEXT
        )
        
    ''')
    cursor.execute('''
        INSERT INTO mrr_alert (date, time, place, alert_type)
        SELECT date, time, place, alert_type FROM alerts
    ''')
    conn.commit()
    conn.close()

def staging():
    conn = sqlite3.connect('alerts.db')
    cursor = conn.cursor()

    # Fetch rows from the 'alerts' table
    cursor.execute('SELECT date, time, place, alert_type FROM mrr_alert')
    rows = cursor.fetchall()

    # Create a new table 'places' to store the split places
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stg_alert (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
            date date,
            time time,
            place TEXT,
            alert_type integer
        )
    ''')

    # Iterate through each row in 'alerts' table
    for row in rows:
        date, time, places, alert_type = row
        date = date.replace("היום", "").strip()
        if alert_type is not None:
         alert_type = alert_type.replace("ירי רקטות וטילים", "1")
         alert_type = alert_type.replace("חדירת כלי טיס עוין", "2")
        # Split places by comma and insert into 'places' table
        for place in places.split(','):
            cursor.execute('''
                INSERT INTO stg_alert (date, time, place, alert_type) VALUES (?, ?, ?, ?)
            ''', (date, time, place.strip(), alert_type))

    conn.commit()
    conn.close()
def dw():
    conn = sqlite3.connect('alerts.db')
    cursor = conn.cursor()

    # Fetch rows from the 'alerts' table
    cursor.execute('SELECT date, time, place, alert_type FROM mrr_alert')
    rows = cursor.fetchall()

    # Create a new table 'places' to store the split places
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stg_alert (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
            date date,
            time time,
            place TEXT,
            alert_type integer
        )
    ''')
# Call the function to split places and insert into the 'places' table
#mirroring();
#staging();
#dw();



