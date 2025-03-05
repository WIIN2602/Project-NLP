import sqlite3
import mysql.connector

# Connect to SQLite
sqlite_conn = sqlite3.connect("news.db")
sqlite_cursor = sqlite_conn.cursor()
sqlite_cursor.execute(
    "SELECT title, publisher, type, date, content, link FROM news")
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
    id INT(100) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL COMMENT 'news name',
    publisher VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Publisher of news',
    type TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL COMMENT 'news type',
    tag TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NULL COMMENT 'news tags',
    date DATETIME NOT NULL COMMENT 'Date and time the news was released',
    content TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL COMMENT 'news content',
    link TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL COMMENT 'link to original',
    image LONGBLOB NULL COMMENT 'word cloud of news',
    summary TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NULL COMMENT 'Summarized Content'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;
"""
mysql_cursor.execute(create_table_sql)

# Insert Data into MySQL (Skipping `id` and adding default `tag`, `image`, `summary` as empty string)
for row in news_data:
    # (title, publisher, type, date, content, link)
    title, publisher, news_type, date, content, link = row
    mysql_cursor.execute("""
        INSERT INTO news (title, publisher, type, tag, date, content, link, image, summary)
        VALUES (%s, %s, %s, '', %s, %s, %s, '', '')
    """, (title, publisher, news_type, date, content, link))

mysql_conn.commit()
mysql_conn.close()
sqlite_conn.close()

print("✅ SQLite data successfully synced to MySQL!")
