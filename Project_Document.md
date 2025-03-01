# NLP_PROJECT Documentation

## Project Structure

```
NLP_PROJECT
│── backend
│   │── data
│   │   │── matichon_entertainment_news.csv
│   │   │── matichon_foreign_news.csv
│   │   │── matichon_politics_news.csv
│   │   │── matichon_sport_news.csv
│   │
│   │── fonts
│   │   │── Italianno-Regular.ttf
│   │   │── Mitr-Regular.ttf
│   │
│   │── push_data2mysql
│   │   │── csv2sql.py
│   │   │── insert.py
│   │
│   │── venv
│   │── app.py
│   │── requirements.txt
│
│── frontend
│   │── fetch_news.php
│   │── get_image.php
│   │── index.php
│   │── process_news.php
│
│── .gitignore
│── README.md
```

## File Explanations

### Backend

#### `backend/push_data2mysql/csv2sql.py`
- Reads news data from CSV files in `backend/data/`
- Converts Thai date formats into SQLite standard format
- Stores news data into an SQLite database (`news2.db`)

#### `backend/push_data2mysql/insert.py`
- Fetches data from `news2.db` (SQLite database)
- Connects to MySQL via XAMPP
- Creates a `news` table if not exists
- Inserts data from SQLite into MySQL

#### `backend/app.py`
- Flask API backend for the project
- Provides endpoints to retrieve news (`/get_news`)
- Processes news to generate word clouds (`/process_news`)
- Uses `pymysql` to interact with MySQL database

### Frontend

#### `frontend/fetch_news.php`
- Connects to MySQL database
- Retrieves all news articles
- Outputs news data in JSON format

#### `frontend/get_image.php`
- Retrieves and serves generated word cloud images from MySQL
- Fetches image blob data and returns it as a PNG

#### `frontend/index.php`
- Webpage displaying all news articles
- Provides search and filter functionality
- Loads news from `fetch_news.php`

#### `frontend/process_news.php`
- Fetches all news content from MySQL
- Sends the news content to `backend/app.py` API for processing
- Updates word cloud images for each news entry

### Database Structure

#### MySQL Table Schema
```sql
CREATE TABLE news (
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT 'News Index',
    title VARCHAR(255) COLLATE utf8mb4_unicode_520_ci NOT NULL COMMENT 'News Name',
    type ENUM('Politics', 'Sports', 'Technology', 'Entertainment', 'Other') NOT NULL COMMENT 'News Type',
    tag VARCHAR(255) COLLATE utf8mb4_unicode_520_ci NOT NULL COMMENT 'News Tags',
    date DATETIME NOT NULL COMMENT 'Date and time the news was released',
    content TEXT COLLATE utf8mb4_unicode_520_ci NOT NULL COMMENT 'News Content',
    link VARCHAR(2083) COLLATE utf8mb4_unicode_520_ci NOT NULL COMMENT 'Link to Original',
    image_url VARCHAR(2083) COLLATE utf8mb4_unicode_520_ci NULL COMMENT 'URL of Word Cloud Image',
    FULLTEXT(title, content, tag) -- For full-text search optimization
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;
```