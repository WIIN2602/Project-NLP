from flask import Flask, request, jsonify
import pymysql
from pythainlp.corpus import thai_stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io

# ใช้ PyThaiNLP สำหรับ Stopwords ภาษาไทย
stop_words = set(thai_stopwords())

app = Flask(__name__)

# ฟังก์ชันเชื่อมต่อ MySQL


def connect_db():
    return pymysql.connect(host="localhost", port=3306, user="root", password="", database="nlp_project", charset="utf8mb4")

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

# API ประมวลผลข่าวและสร้าง Word Cloud


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

    # คัดเลือกคำสำคัญ
    words = content.split()
    keywords = [w for w in words if w not in stop_words][:5]
    keywords_str = ", ".join(keywords)

    # สร้าง Word Cloud
    font_path = "fonts/THSarabunNew.ttf"  # ต้องมีฟอนต์อยู่ที่นี่
    wordcloud = WordCloud(font_path=font_path,
                          background_color="white").generate(content)

    # แปลงภาพเป็น BLOB
    img_io = io.BytesIO()
    wordcloud.to_image().save(img_io, format="PNG")
    img_blob = img_io.getvalue()

    # อัปเดตข้อมูลลง MySQL
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE news SET tag=%s, image=%s WHERE id=%s",
                   (keywords_str, img_blob, news_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Processed successfully!", "id": news_id, "keywords": keywords_str})


if __name__ == '__main__':
    app.run(debug=True)
