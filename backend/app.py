from flask import Flask, request, jsonify
import pymysql
from pythainlp.corpus import thai_stopwords
from wordcloud import WordCloud
from io import BytesIO
import pandas as pd
from pythainlp.tokenize import word_tokenize


stop_words = set(thai_stopwords())

app = Flask(__name__)

# เชื่อมต่อฐานข้อมูล MySQL


def connect_db():
    return pymysql.connect(host="localhost",
                           port=3306,
                           user="root",
                           password="",
                           database="nlp_project",
                           charset="utf8mb4",
                           connect_timeout=10)

# API ดึงข่าวทั้งหมดจากฐานข้อมูล


@app.route('/get_news', methods=['GET'])
def get_news():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, title, type, tag, date, content, link FROM news")
    news = cursor.fetchall()
    conn.close()

    news_list = []
    for row in news:
        news_list.append({
            "id": row[0],
            "title": row[1],
            "type": row[2],
            "tag": row[3],
            "date": row[4].strftime('%Y-%m-%d %H:%M:%S'),
            "content": row[5],
            "link": row[6]
        })
    return jsonify(news_list)

# API วิเคราะห์ข่าวและอัปเดต Tag


@app.route('/process_news', methods=['POST'])
def process_news():
    if request.content_type != 'application/json':
        return jsonify({"error": "Invalid Content-Type. Expected 'application/json'"}), 415

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    news_id = data.get("id")
    content = data.get("content")

    if not news_id or not content:
        return jsonify({"error": "Missing 'id' or 'content'"}), 400

    # Tokenize ข้อความภาษาไทย
    font_path = "fonts/Mitr-Regular.ttf"
    reg = r"[ก-๙a-zA-Z']+"

    content_tokens = word_tokenize(content)
    stop_words = list(thai_stopwords())
    content_tokens_rm_stopword = [
        token for token in content_tokens if token not in stop_words]
    content_tokens_text_rm_stopword = " ".join(content_tokens_rm_stopword)

    # Generate Word Cloud
    wordcloud = WordCloud(
        stopwords=stop_words,
        font_path=font_path,
        background_color="white",
        max_words=2000,
        height=2000,
        width=4000,
        regexp=reg
    ).generate(content_tokens_text_rm_stopword)

    # แปลงภาพเป็น BLOB
    img_io = BytesIO()
    wordcloud.to_image().save(img_io, format="PNG")
    img_blob = img_io.getvalue()

    # คัดเลือกคำสำคัญ
    words = content.split()
    keywords = [w for w in words if w not in stop_words][:5]
    keywords_str = ", ".join(keywords)

    # อัปเดตข้อมูลลง MySQL
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE news SET image=%s WHERE id=%s", (img_blob, news_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Processed successfully!", "id": news_id})


if __name__ == '__main__':
    app.run(debug=True)
