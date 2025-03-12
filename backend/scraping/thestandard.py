import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

VALID_TYPES = ["politics", "sport", "world"]
ENTERTAINMENT_URL = "https://thestandard.co/category/culture/tv-entertainment/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Define fixed pages for each year
PAGE_NUMBERS = {
    "politics": {2025: 1, 2024: 100, 2023: 550, 2022: 1120},
    "sport": {2025: 1, 2024: 60, 2023: 330, 2022: 570},
    "world": {2025: 1, 2024: 60, 2023: 180, 2022: 390},
    "entertainment": {2025: 1, 2024: 20, 2023: 130, 2022: 210}
}


def convert_thai_month(month):
    """Convert Thai month name to numerical month string."""
    return (month.replace("มกราคม", "01")
                 .replace("กุมภาพันธ์", "02")
                 .replace("มีนาคม", "03")
                 .replace("เมษายน", "04")
                 .replace("พฤษภาคม", "05")
                 .replace("มิถุนายน", "06")
                 .replace("กรกฎาคม", "07")
                 .replace("สิงหาคม", "08")
                 .replace("กันยายน", "09")
                 .replace("ตุลาคม", "10")
                 .replace("พฤศจิกายน", "11")
                 .replace("ธันวาคม", "12"))


def convert_date(date_str):
    datetime = date_str
    datetime = convert_thai_month(datetime)
    day, month, year = datetime.split(" ")
    day = day if int(day) >= 10 else f"0{day}"
    date_format = f'{year}-{month}-{day} 00:00:00'
    return date_format


def clean_text(text):
    """Remove unwanted characters and format the text properly."""
    return text.replace(",", " ").replace('"', " ").strip()


def extract_content(link):
    """
    Fetch and extract the full content of a news article.
    """
    try:
        news_response = requests.get(link, headers=HEADERS)
        if news_response.status_code != 200:
            return "❌ ไม่สามารถเข้าถึงเนื้อหาข่าว"

        news_soup = BeautifulSoup(news_response.text, 'html.parser')
        content_tag = news_soup.find('div', class_='entry-content')

        if not content_tag:
            return "❌ ไม่พบเนื้อหาข่าว"

        content_texts = []
        paragraphs = content_tag.find_all('p')

        for p in paragraphs:
            span_tag = p.find('span', style=True)
            if span_tag:
                content_texts.append(clean_text(span_tag.text.strip()))
            else:
                content_texts.append(clean_text(p.text.strip()))

        return "\n".join(content_texts) if content_texts else "❌ ไม่พบเนื้อหาข่าว"

    except Exception as e:
        return f"⚠️ Error: {str(e)}"


def get_news(category, year):
    """
    Fetch news articles for a given category and year with fixed page numbers and content.
    """
    news_data = []

    # Correctly map 'foreign' to 'world'
    category = "world" if category == "foreign" else category

    # Get predefined page number for the given year & category
    page = PAGE_NUMBERS.get(category, {}).get(year, 1)

    # Build URL based on category
    if category == "entertainment":
        url = f"{ENTERTAINMENT_URL}page/{page}/"
    else:
        url = f"https://thestandard.co/category/news/{category}/page/{page}/"

    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"⚠️ Cannot access {url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("div", class_="news-item")

    if not articles:
        return []  # Stop if no articles found

    for article in articles:
        title_tag = article.find("h3", class_="news-title")
        link_tag = article.find("a", href=True)
        date_tag = article.find("div", class_="date")

        if not title_tag or not link_tag:
            continue

        title = clean_text(title_tag.text.strip())
        link = link_tag["href"]
        date = clean_text(date_tag.text.strip()) if date_tag else "Unknown"
        date_obj = convert_date(date_tag.text.strip()
                                ) if date_tag else "Unknown"
        year_match = re.search(r"(\d{4})", date)
        news_year = year_match.group(1) if year_match else "Unknown"

        # Filter by year if specified
        if year != "all" and news_year != str(year):
            continue

        # Extract full news content
        content = extract_content(link)

        news_data.append({
            "title": title,
            "link": link,
            "date": date_obj,
            "content": content,
            "publisher": "thestandard",
            "type": category
        })

    return news_data


def scrape_thestandard(news_type="all", year="all"):
    """
    Scrapes news from The Standard based on category and year with fixed page numbers.
    """
    print(
        f"Scraping news type: {news_type}, Year: {year}, from Publisher: the standard")

    # Correctly map 'foreign' to 'world'
    if news_type == "all":
        categories = VALID_TYPES + ["entertainment"]
    else:
        categories = [news_type.replace("foreign", "world")]

    # Convert year to integer if not "all"
    year = int(year) if year != "all" else "all"

    news_data = []
    for category in categories:
        news_data.extend(get_news(category, year))

    return news_data
