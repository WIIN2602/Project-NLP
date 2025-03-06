from flask import Flask, request, jsonify
import pymysql
from pythainlp.corpus import thai_stopwords, thai_words
from wordcloud import WordCloud
from io import BytesIO
# import pandas as pd
from pythainlp.tokenize import word_tokenize, syllable_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import re
from pythainlp.summarize import summarize

stop_words = set(thai_stopwords())  # Thai stop words
valid_thai_words = set(thai_words())  # Thai dictionary words

# Manually remove common but non-informative words
manual_stopwords = set(["มาก", "แล้ว", "วันที่", "ใช่",
                        "ไม่เลย", "คือ", "อีก", "และ",
                        "เพราะ", "ด้วย", "ค่ะ", "ครับ",
                        "หรือ", "อย่าง", "ธันวา", "เรียก", 
                        "ปี", "วัย", "ล้าน", "3", "000", ""])

app = Flask(__name__)


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
    title = data.get("title")
    content = data.get("content")

    if not news_id or not content:
        return jsonify({"error": "Missing 'id' or 'content'"}), 400

    font_path = "fonts/Mitr-Regular.ttf"
    reg = r"[ก-๙a-zA-Z']+"

    # Tokenize content
    content_tokens = word_tokenize(content)

    # Remove stop words
    filtered_tokens = [
        word for word in content_tokens if word not in stop_words and word.strip()]

    # Select only 2-syllable words with error handling
    two_syllable_words = []
    for word in filtered_tokens:
        try:
            if len(word) > 1 and len(syllable_tokenize(word)) == 2:
                two_syllable_words.append(word)
        except Exception as e:
            print(f"Error processing word '{word}': {e}")

    if not two_syllable_words:
        return jsonify({"error": "No valid words for word cloud"}), 400

    content_text_filtered = " ".join(two_syllable_words)

    # Generate Word Cloud
    wordcloud = WordCloud(
        stopwords=stop_words,
        font_path=font_path,
        background_color="white",
        max_words=2000,
        height=2000,
        width=4000,
        regexp=reg
    ).generate(content_text_filtered)

    # Convert to image
    img_io = BytesIO()
    wordcloud.to_image().save(img_io, format="PNG")
    img_blob = img_io.getvalue()

    # Update database with the new image
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE news SET image=%s WHERE id=%s", (img_blob, news_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Processed successfully!", "id": news_id})


# Extract Keywords using TF-IDF (Title weighting + 2-syllable filter + dictionary check)
@app.route('/extract_keywords', methods=['POST'])
def extract_keywords():
    if request.content_type != 'application/json':
        return jsonify({"error": "Invalid Content-Type. Expected 'application/json'"}), 415

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    news_id = data.get("id")
    title = data.get("title", "")
    content = data.get("content", "")

    if not news_id or not content:
        return jsonify({"error": "Missing 'id' or 'content'"}), 400

    # Combine title and content, repeating the title to give it more weight
    combined_text = (title + " ") * 3 + content

    # Convert text to lowercase
    combined_text = combined_text.lower()

    # TF-IDF Vectorization with bigram support
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),  # Extracts unigrams and bigrams
        token_pattern=r'[ก-๙0-9]+',
    )
    tfidf_matrix = vectorizer.fit_transform([combined_text])

    # Extract feature names (words/phrases) and their scores
    feature_array = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]

    # Create dictionary of words/phrases and scores
    word_score_dict = dict(zip(feature_array, scores))

    # Filter only meaningful words: words must be in the Thai dictionary or be bigrams
    valid_keywords = {}
    for word, score in word_score_dict.items():
        try:
            if word in valid_thai_words or " " in word:
                if len(syllable_tokenize(word)) <= 4 and word not in manual_stopwords:
                    valid_keywords[word] = score
        except Exception as e:
            print(f"Error processing word '{word}': {e}")

    # Sort words/phrases by score in descending order
    sorted_keywords = sorted(valid_keywords.items(),
                             key=lambda x: x[1], reverse=True)

    # Select top 5 keywords
    top_keywords = [word for word, score in sorted_keywords[:5]]
    keywords_str = ", ".join(top_keywords)

    # Update database with extracted keywords
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE news SET tag=%s WHERE id=%s",
                   (keywords_str, news_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Keywords extracted successfully!", "id": news_id, "keywords": top_keywords})


@app.route('/summarize_news', methods=['POST'])
def summarize_news():
    if request.content_type != 'application/json':
        return jsonify({"error": "Invalid Content-Type. Expected 'application/json'"}), 415

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    news_id = data.get("id")
    title = data.get("title")
    content = data.get("content")

    if not news_id or not content:
        return jsonify({"error": "Missing 'id' or 'content'"}), 400

    # Summarize the content using TextRank
    summary_sentences = summarize(content, n=3)  # Get 3 key sentences
    summary_text = " ".join(summary_sentences)

    # Update database with summary
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE news SET summary=%s WHERE id=%s",
                   (summary_text, news_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Summary generated successfully!", "id": news_id, "summary": summary_text})


if __name__ == '__main__':
    app.run(debug=True)
