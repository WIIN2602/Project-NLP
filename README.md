# NLP_PROJECT

Team member 

65160031 Kotchamonwan Somboonkul

65160056 Sunita Sathianjarukarn

65160272 Chanakarn Patinung

65160282 Wasupakkanut Wattanakul
 
65160283 Weeradech Taengon

# Web Summary Thai News

## Project Overview
The Web Summary Thai News project is designed to collect, process, and summarize Thai news articles using NLP (Natural Language Processing) techniques. The system extracts keywords, generates word clouds, and stores articles in a MySQL database. The project is structured into backend and frontend components to ensure a smooth and efficient workflow.

## Project Structure
```
project_root/
├── backend/
│   ├── data/  # Directory for storing news data in CSV format
│   ├── fonts/ # Fonts used in the word cloud generation process
│   ├── push_data2mysql/
│   │   ├── csv2sql.py  # Converts CSV files into SQLite format
│   │   ├── insert.py  # Inserts data from SQLite into MySQL
│   ├── venv/   # Python virtual environment
│   ├── app.py  # Main backend file that acts as an API endpoint
│   ├── requirements.txt # Required Python libraries
│
├── frontend/
│   ├── extract_keywords.php # Extracts keywords from news articles
│   ├── fetch_news.php  # Fetches all news articles from MySQL
│   ├── get_image.php # Displays the word cloud image
│   ├── index.php # Main frontend webpage
│   ├── process_news.php # Handles the word cloud processing
│   ├── summarize_news.php # Generates news summaries
│
├── .gitignore
├── Project_Document.md # Documentation file for the project
├── README.md # Project introduction and setup guide
```

## Backend Functionality
### 1. **CSV to SQLite Conversion (csv2sql.py)**
This script loads news data from CSV files, processes the Thai date format, and inserts the formatted data into an SQLite database.
- Handles different date formats from multiple publishers (e.g., Matichon, The Standard, TNA).
- Converts Thai Buddhist Era years to the Gregorian calendar.
- Stores data with fields such as title, publisher, date, content, and link.

### 2. **SQLite to MySQL Data Migration (insert.py)**
- Transfers data from SQLite to MySQL.
- Creates the `news` table in MySQL if it does not exist.
- Stores additional fields such as tags, summary, and word cloud images.

### 3. **Flask API (app.py)**
Provides API endpoints for:
- Processing news articles to generate word clouds.
- Extracting keywords using TF-IDF.
- Summarizing news content.

## Frontend Functionality
### 1. **Fetching News (fetch_news.php)**
Retrieves all news articles from the MySQL database and returns them in JSON format for display on the web interface.

### 2. **Extracting Keywords (extract_keywords.php)**
- Sends a request to the Flask API to extract keywords from a news article.
- Updates the `tag` field in the MySQL database with the extracted keywords.

### 3. **Processing Word Clouds (process_news.php)**
- Requests the Flask API to generate a word cloud image based on article content.
- Updates the MySQL database with the generated image.

### 4. **Summarizing News (summarize_news.php)**
- Calls the Flask API to generate a summary of the news article.
- Updates the `summary` field in the database with the generated content.

### 5. **Web Interface (index.php)**
- Displays all news articles with filters for type, publisher, and date.
- Provides buttons to generate word clouds, extract keywords, and summarize articles.
- Shows images of generated word clouds and extracted keywords.

## Setup Guide
### 1. **Install Dependencies**
```bash
pip install -r backend/requirements.txt
```

### 2. **Start XAMPP Services**
- Open XAMPP.
- Start **Apache** and **MySQL**.

### 3. **Create MySQL Database**
- Open phpMyAdmin (`http://localhost/phpmyadmin/`).
- Create a database named `nlp_project`.
- Execute the following SQL command to create the `news` table:
```sql
CREATE TABLE news (
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title TEXT COLLATE utf8mb4_unicode_520_ci NOT NULL,
    publisher VARCHAR(255) COLLATE utf8mb4_unicode_ci NOT NULL,
    type TEXT COLLATE utf8mb4_unicode_520_ci NOT NULL,
    tag TEXT COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
    date DATETIME NOT NULL,
    content TEXT COLLATE utf8mb4_unicode_520_ci NOT NULL,
    link TEXT COLLATE utf8mb4_unicode_520_ci NOT NULL,
    image LONGBLOB DEFAULT NULL,
    summary TEXT COLLATE utf8mb4_unicode_520_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 4. **Load Data into SQLite**
```bash
python backend/push_data2mysql/csv2sql.py
```

### 5. **Migrate Data to MySQL**
```bash
python backend/push_data2mysql/insert.py
```

### 6. **Start the Flask API Server**
```bash
python backend/app.py
```

### 7. **Run the Frontend**
- Move the `frontend/` folder to `htdocs/` in XAMPP.
- Open a browser and go to:
```
http://localhost/NLP_PROJECT/frontend/index.php
```

## API Endpoints
### **`GET /fetch_news`**
Retrieves all stored news articles from MySQL.

### **`POST /process_news`**
Generates a word cloud for a news article.

### **`POST /extract_keywords`**
Extracts the most relevant keywords from an article.

### **`POST /summarize_news`**
Summarizes an article into a few sentences.

## Features
✔ Thai date conversion to standard format
✔ News data storage in MySQL
✔ Word cloud generation
✔ Keyword extraction
✔ Summarization of news articles
✔ Interactive web interface

## Troubleshooting
### MySQL Connection Issues
- Ensure XAMPP's MySQL service is running.
- Check database credentials in `backend/app.py` and `frontend/fetch_news.php`.

### Flask API Not Running
- Ensure Flask is installed (`pip install flask`).
- Check for port conflicts (default: 5000).

## Future Enhancements
- Improve NLP techniques for better keyword extraction.
- Implement user authentication.
- Enhance UI for a better user experience.

---
This document serves as a complete guide to setting up and understanding the project.

