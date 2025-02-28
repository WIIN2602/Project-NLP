from flask import Flask, request, jsonify
import pymysql
import pythainlp.tokenize
from wordcloud import WordCloud
from io import BytesIO

app = Flask(__name__)

# ฟังก์ชันเชื่อมต่อ MySQL


def connect_db():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="nlp_project",
        charset="utf8mb4"
    )

# API สำหรับสร้าง Word Cloud และบันทึกลง MySQL


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

    content_tokens = pythainlp.tokenize.word_tokenize(content)
    content_tokens_text = " ".join(content_tokens)

    # Generate Word Cloud
    wordcloud = WordCloud(
        font_path=font_path,
        background_color="white",
        max_words=2000,
        height=800,
        width=1600,
        regexp=reg
    ).generate(content_tokens_text)

    # แปลงภาพเป็น BLOB
    img_io = BytesIO()
    wordcloud.to_image().save(img_io, format="PNG")
    img_blob = img_io.getvalue()

    # อัปเดตข้อมูลลง MySQL
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE news SET image=%s WHERE id=%s", (img_blob, news_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Processed successfully!", "id": news_id})


if __name__ == '__main__':
    app.run(debug=True)
