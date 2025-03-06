import pandas as pd
import sqlite3
import re
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, "en_US.UTF-8")

# SQLite Database Connection
db_name = "news.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()
# Create Table if Not Exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS news(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        publisher TEXT NOT NULL,
        type TEXT NOT NULL,
        date DATETIME NOT NULL,
        content TEXT NOT NULL,
        link TEXT NOT NULL
    )
""")

# Function to Convert Thai Date Format to SQLite Standard Date


def convert_thai_date(publisher, thai_date_str):
    if publisher == "matichon":
        # Use Regex to extract the correct date format
        match = re.search(
            r'วันที่ (\d{1,2}) (\S+) (\d{4}) - (\d{2}:\d{2}) น.', thai_date_str)

        if match:
            day, th_month, year, time_part = match.groups()

            year = int(year) - 543

            # Month conversion
            month_mapping = {
                "มกราคม": "January", "กุมภาพันธ์": "February", "มีนาคม": "March",
                "เมษายน": "April", "พฤษภาคม": "May", "มิถุนายน": "June",
                "กรกฎาคม": "July", "สิงหาคม": "August", "กันยายน": "September",
                "ตุลาคม": "October", "พฤศจิกายน": "November", "ธันวาคม": "December"
            }
            # Convert Thai month to English
            month = month_mapping.get(th_month, th_month)

            try:
                # Ensure there are no extra spaces
                date_str = f"{day} {month} {year} {time_part}".strip()

                # Convert to standard datetime format
                date_obj = datetime.strptime(date_str, "%d %B %Y %H:%M")
                return date_obj

            except ValueError as e:
                print(f"❌ Error parsing date {thai_date_str}: {e}")
                return None  # Skip invalid dates
    elif publisher == "thestandard":
        # Use Regex to extract the correct date format
        match = re.search(r'(\d{1,2}) (\S+) (\d{4})', thai_date_str)

        if match:
            day, th_month, year = match.groups()

            year = int(year)

            # Month conversion
            month_mapping = {
                "มกราคม": "January", "กุมภาพันธ์": "February", "มีนาคม": "March",
                "เมษายน": "April", "พฤษภาคม": "May", "มิถุนายน": "June",
                "กรกฎาคม": "July", "สิงหาคม": "August", "กันยายน": "September",
                "ตุลาคม": "October", "พฤศจิกายน": "November", "ธันวาคม": "December"
            }
            # Convert Thai month to English
            month = month_mapping.get(th_month, th_month)

            try:
                # Ensure there are no extra spaces
                date_str = f"{day} {month} {year}".strip()

                # Convert to standard datetime format
                date_obj = datetime.strptime(date_str, "%d %B %Y")
                return date_obj

            except ValueError as e:
                print(f"❌ Error parsing date {thai_date_str}: {e}")
                return None  # Skip invalid dates
    elif publisher == "tna":
        # Use Regex to extract the correct date format
        match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', thai_date_str)

        if match:
            day, th_month, year = match.groups()

            year = int(year) - 543

            # Month conversion
            month_mapping = {
                "01": "January", "02": "February", "03": "March",
                "04": "April", "05": "May", "06": "June",
                "07": "July", "08": "August", "09": "September",
                "10": "October", "11": "November", "12": "December"
            }
            # Convert month to full English name
            month = month_mapping.get(th_month, th_month)

            try:
                # Ensure there are no extra spaces
                date_str = f"{day} {month} {year}".strip()

                # Convert to standard datetime format
                date_obj = datetime.strptime(date_str, "%d %B %Y")
                return date_obj

            except ValueError as e:
                print(f"❌ Error parsing date {thai_date_str}: {e}")
                return None  # Skip invalid dates
    print("❌ No match found for date format!")
    return None  # If regex fails, return None


# Load CSV File
csv_files = ["../data/matichon_entertainment_news.csv",
             "../data/matichon_foreign_news.csv",
             "../data/matichon_politics_news.csv",
             "../data/matichon_politics_news_2022.csv",
             "../data/matichon_politics_news_2023.csv",
             "../data/matichon_politics_news_2024.csv",
             "../data/matichon_sport_news.csv",
             "../data/thestandard_entertainment_news_2022-2024.csv",
             "../data/thestandard_entertainment_news_2025.csv",
             "../data/thestandard_foreign_news_2022-2024.csv",
             "../data/thestandard_foreign_news_2025.csv",
             "../data/thestandard_politics_news_2022-2024.csv",
             "../data/thestandard_politics_news_2025.csv",
             "../data/thestandard_sport_news_2022-2024.csv",
             "../data/thestandard_sport_news_2025.csv",
             "../data/tna_entertainment_news_2022.csv",
             "../data/tna_entertainment_news_2023.csv",
             "../data/tna_entertainment_news_2024.csv",
             "../data/tna_foreign_news_2022.csv",
             "../data/tna_foreign_news_2023.csv",
             "../data/tna_foreign_news_2024.csv",
             "../data/tna_foreign_news_2025.csv",
             "../data/tna_politics_news_2022.csv",
             "../data/tna_politics_news_2023.csv",
             "../data/tna_politics_news_2024.csv",
             "../data/tna_politics_news_2025.csv",
             "../data/tna_sport_news_2022.csv",
             "../data/tna_sport_news_2023.csv",
             "../data/tna_sport_news_2024.csv",
             "../data/tna_sport_news_2025.csv",
             ]
for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    csv = csv_file.split('/')
    name = [n for n in csv if n != "data"]
    name = [t.split('_') for t in name]
    file_name = name[1]
    # Insert Data into SQLite
    for index, row in df.iterrows():
        title = row["title"]
        content = row["content"]
        type_news = file_name[1]
        publisher = file_name[0]
        link = row["link"]
        date = convert_thai_date(publisher, row["date"])
        date = date.strftime("%Y-%m-%d %H:%M:%S")
        if date:  # Only insert valid data
            cursor.execute("INSERT INTO news (title, publisher, type, date, content, link) VALUES (?, ?, ?, ?, ?, ?)",
                           (title, publisher, type_news, date, content, link))
        # id INTEGER PRIMARY KEY AUTOINCREMENT,
        # title TEXT NOT NULL,
        # publisher TEXT NOT NULL,
        # type TEXT NOT NULL,
        # date DATETIME NOT NULL,
        # content TEXT NOT NULL,
        # link TEXT NOT NULL
    print(
        f"✅ News from {publisher} type {type_news} in file CSV has been successfully inserted into SQLite!")
# Commit and Close
conn.commit()
conn.close()
