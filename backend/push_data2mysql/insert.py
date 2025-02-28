import sqlite3
import mysql.connector

# Connect to SQLite
sqlite_conn = sqlite3.connect("news2.db")
sqlite_cursor = sqlite_conn.cursor()
sqlite_cursor.execute(
    "SELECT title, type, date, content, link FROM news")  # Skip ID
news_data = sqlite_cursor.fetchall()

# Connect to XAMPP MySQL (localhost)
mysql_conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="nlp_project"
)
mysql_cursor = mysql_conn.cursor()

# Create Table in MySQL if Not Exists
create_table_sql = """
CREATE TABLE IF NOT EXISTS news (
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT 'news index',
    title TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL COMMENT 'news name',
    type TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL COMMENT 'news type',
    tag TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL COMMENT 'news tags',
    date DATETIME NOT NULL COMMENT 'Date and time the news was released',
    content TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL COMMENT 'news content',
    link TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL COMMENT 'link to original'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;
"""
mysql_cursor.execute(create_table_sql)

# Insert Data into MySQL (Skipping `id` and adding default `tag` as empty string)
for row in news_data:
    mysql_cursor.execute("""
        INSERT INTO news (title, type, date, content, link, tag)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (*row, ""))

mysql_conn.commit()
mysql_conn.close()
sqlite_conn.close()

print("✅ SQLite data successfully synced to MySQL!")
