# NLP_PROJECT

65160031 Kotchamonwan Somboonkul

65160056 Sunita Sathianjarukarn

65160272 Chanakarn Patinung

65160282 Wasupakkanut Wattanakul
 
65160283 Weeradech Taengon

Under the topic 
# News Summary Website

## Introduction
This project processes and displays Thai news articles with NLP analysis. It extracts keywords, generates word clouds, and stores news articles in a MySQL database.

## Prerequisites
- XAMPP (Apache, MySQL)
- Python 3.8+
- Flask
- MySQL Connector
- Pandas, WordCloud, PyThaiNLP

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Start XAMPP
- Open XAMPP
- Start **Apache** and **MySQL**

### 3. Create MySQL Database
- Open phpMyAdmin (`http://localhost/phpmyadmin/`)
- Create a database named `nlp_project`
- Run the following SQL command to create the `news` table:
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
    FULLTEXT(title, content, tag)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;
```

### 4. Load Data
- Convert CSV data to SQLite:
```bash
python backend/push_data2mysql/csv2sql.py
```
- Insert data into MySQL:
```bash
python backend/push_data2mysql/insert.py
```

### 5. Start Flask Backend
```bash
python backend/app.py
```

### 6. Open Frontend
- Place the `frontend/` folder inside `htdocs/` of XAMPP
- Open browser and go to:
```
http://localhost/NLP_PROJECT/frontend/index.php
```

## API Endpoints

### `GET /get_news`
Retrieves all news articles from MySQL.

### `POST /process_news`
Processes a news article and generates a word cloud.

## Features
- Converts Thai dates to standard formats
- Stores news in MySQL database
- Generates word cloud images for each news article
- Provides a web interface for browsing and searching news

## Troubleshooting
### MySQL Connection Issues
- Ensure MySQL is running in XAMPP
- Check database name and credentials in `backend/app.py` and `frontend/fetch_news.php`

### Flask API Not Running
- Ensure Flask is installed (`pip install flask`)
- Check port conflicts (default: 5000)

## Future Improvements
- Enhance NLP analysis for better keyword extraction
- Implement user authentication
- Improve UI design

---
This documentation covers the full setup and workflow of the project, ensuring an easy-to-follow guide for deployment and usage.

