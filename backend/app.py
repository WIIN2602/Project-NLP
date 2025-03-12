from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from wordcloud import WordCloud
from io import BytesIO
from sklearn.feature_extraction.text import TfidfVectorizer
from pythainlp.summarize import summarize
import base64
from scraping.thestandard import scrape_thestandard
from scraping.matichon import scrape_matichon
from scraping.tna import scrape_tna

app = Flask(__name__)
CORS(app)


def connect_db():  # Connect to MySQL
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="nlp_project",
        charset="utf8mb4",
        connect_timeout=10
    )


@app.route('/process_news', methods=['POST'])  # Process News for Word Cloud
def process_news():
    if request.content_type != 'application/json':
        return jsonify({"error": "Invalid Content-Type. Expected 'application/json'"}), 415

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    news_id = data.get("id")
    content = data.get("content")
    print(f"get this content from index:\n {content}")
    if not news_id or not content:
        return jsonify({"error": "Missing 'id' or 'content'"}), 400

    font_path = "fonts/Mitr-Regular.ttf"
    reg = r"[ก-๙a-zA-Z']+"

    # Generate Word Cloud
    wordcloud = WordCloud(
        font_path=font_path,
        background_color="white",
        max_words=2000,
        height=2000,
        width=4000,
        regexp=reg
    ).generate(content)

    # Convert image to base64
    img_io = BytesIO()
    wordcloud.to_image().save(img_io, format="PNG")
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.read()).decode()
    print(f"send word cloud to index successfully")
    return jsonify({"wordcloud": img_base64})


@app.route('/extract_keywords', methods=['POST'])
def extract_keywords():
    if request.content_type != 'application/json':
        return jsonify({"error": "Invalid Content-Type. Expected 'application/json'"}), 415

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    news_id = data.get("id")
    content = data.get("content", "")
    print(f"Get this content from index:\n{content}")
    if not news_id or not content:
        return jsonify({"error": "Missing 'id' or 'content'"}), 400

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2), token_pattern=r'[ก-๙0-9]+')
    tfidf_matrix = vectorizer.fit_transform([content])

    # Extract top 5 keywords
    feature_array = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]
    sorted_keywords = sorted(zip(feature_array, scores),
                             key=lambda x: x[1], reverse=True)
    top_keywords = [word for word, score in sorted_keywords[:5]]
    print(f"send keyword to index successfully")
    return jsonify({"keywords": top_keywords})


@app.route('/summarize_news', methods=['POST'])
def summarize_news():
    if request.content_type != 'application/json':
        return jsonify({"error": "Invalid Content-Type. Expected 'application/json'"}), 415

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    news_id = data.get("id")
    content = data.get("content")
    print(f"Get this content from index:\n{content}")
    if not news_id or not content:
        return jsonify({"error": "Missing 'id' or 'content'"}), 400

    # Summarize content
    summary_sentences = summarize(content, n=3)  # Get 3 key sentences
    summary_text = " ".join(summary_sentences)
    print(f"send summarize text to index successfully")
    return jsonify({"summary": summary_text})


@app.route('/fetch_news', methods=['POST'])
def fetch_news():
    data = request.get_json()
    news_type = data.get("type", "all")
    publisher = data.get("publisher", "all")
    year = data.get("year", "all")

    scraped_news = []  # Store scraped news

    # Check and call relevant scrapers
    if publisher in ["thestandard", "all"]:
        scraped_news += scrape_thestandard(news_type, year)

    if publisher in ["matichon", "all"]:
        scraped_news += scrape_matichon(news_type, year)

    if publisher in ["tna", "all"]:
        scraped_news += scrape_tna(news_type, year)

    # Insert scraped news into MySQL
    conn = connect_db()
    cursor = conn.cursor()

    inserted_news = []  # Store inserted news to return

    for news in scraped_news:
        if not isinstance(news, dict):  # Ensure it's a dictionary
            print(f"Skipping invalid news format: {news}")
            continue

        title = news.get("title", "Unknown Title")
        link = news.get("link", "")
        date = news.get("date", "Unknown Date")
        content = news.get("content", "No Content")
        publisher = news.get("publisher", "Unknown Publisher")
        news_type = news.get("type", "Unknown Type")

        cursor.execute(
            "SELECT id FROM news WHERE title = %s AND link = %s", (title, link))
        existing_news = cursor.fetchone()

        if not existing_news:
            cursor.execute("""
                INSERT INTO news (title, publisher, type, date, content, link)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (title, publisher, news_type, date, content, link))
            news_id = cursor.lastrowid
        else:
            news_id = existing_news[0]

        # Append inserted news data (including ID) to return to frontend
        inserted_news.append({
            "id": news_id,  # Include ID
            "title": title,
            "link": link,
            "date": date,
            "content": content,
            "publisher": publisher,
            "type": news_type
        })

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"news": inserted_news})  # Send back the inserted news


if __name__ == '__main__':
    app.run(debug=False)
