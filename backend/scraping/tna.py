import cloudscraper
from bs4 import BeautifulSoup
import re
from datetime import datetime

VALID_TYPES = ["entertainment", "politics", "sport", "world"]
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Define fixed pages for each year
PAGE_NUMBERS = {
    "entertainment": {2025: 1, 2024: 2, 2023: 30, 2022: 100},
    "politics": {2025: 1, 2024: 200, 2023: 1000, 2022: 1800},
    "sport": {2025: 1, 2024: 30, 2023: 200, 2022: 400},
    "world": {2025: 1, 2024: 200, 2023: 500, 2022: 1000}
}

# Create a CloudScraper session
scraper = cloudscraper.create_scraper()


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
    """Convert Thai date format to MySQL datetime format."""
    if not date_str or not isinstance(date_str, str):
        return "0000-00-00 00:00:00"  # Return default if the input is invalid

    # Convert Thai month names to numbers
    date_str = convert_thai_month(date_str)
    date_parts = date_str.split(" ")

    # Remove empty values
    date_parts = [value.strip() for value in date_parts if value.strip()]

    print(f"DEBUG: date_parts = {date_parts}")  # Debugging output

    if len(date_parts) < 3:  # Ensure we have day, month, and year
        return "0000-00-00 00:00:00"

    try:
        day, month, year = date_parts[:3]  # Extract first 3 elements

        if not year.isdigit():  # Ensure `year` is numeric
            return "0000-00-00 00:00:00"

        # Convert day to 2-digit format
        day = f"{int(day):02d}"

        return f"{year}-{month}-{day} 00:00:00"
    except Exception as e:
        print(f"⚠️ Error in convert_date: {str(e)}")
        return "0000-00-00 00:00:00"


def clean_text(text):
    """Removes unwanted characters and formats text."""
    text = text.replace(",", " ").replace(
        '\n', " ").replace('\r', '').replace('"', '').strip()

    # Remove "-สำนักข่าวไทย" and everything after it
    text = re.sub(r"-สำนักข่าวไทย.*", "", text).strip()

    return text


def convert_thai_date(thai_date):
    """Converts Thai Buddhist year to Gregorian year."""
    if not thai_date or not isinstance(thai_date, str):
        return "Unknown"

    year_match = re.search(r"(\d{4})", thai_date)

    if not year_match:
        return "Unknown"

    try:
        year = int(year_match.group(1))  # Convert to integer
        return year - 543  # Convert Thai Buddhist year to Gregorian
    except ValueError:
        return "Unknown"


def extract_content(link):
    """Fetches and extracts the full content of a news article."""
    try:
        news_response = scraper.get(link, headers=HEADERS)
        if news_response.status_code != 200:
            return "❌ ไม่สามารถเข้าถึงเนื้อหาข่าว"

        news_soup = BeautifulSoup(news_response.text, "html.parser")
        content_tag = news_soup.find("div", class_="entry-content")

        if content_tag:
            paragraphs = content_tag.find_all("p")
            content = "\n".join([p.text.strip()
                                for p in paragraphs if p.text.strip()])
        else:
            content = "❌ ไม่พบเนื้อหาข่าว"

        return clean_text(content)

    except Exception as e:
        return f"⚠️ Error: {str(e)}"


def get_news(category, year):
    """Scrapes news articles for a given category and year with content extraction."""
    news_data = []
    page = PAGE_NUMBERS.get(category, {}).get(year, 1)
    base_url = f"https://tna.mcot.net/category/{category}/page/{page}"

    response = scraper.get(base_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"⚠️ ไม่สามารถเข้าถึง {base_url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article")

    for article in articles:
        title_tag = article.find("h2", class_="entry-title")
        link_tag = article.find("a", href=True)
        date_tag = article.find("div", class_="time")

        if not title_tag or not link_tag:
            continue

        title = clean_text(title_tag.text.strip())
        link = clean_text(link_tag["href"])
        date = clean_text(date_tag.text.strip()) if date_tag else "Unknown"
        date_obj = convert_date(date_tag.text.strip()
                                ) if date_tag else "Unknown"

        # Convert Thai Buddhist year to Gregorian
        year_match = re.search(r"(\d{4})", date)
        news_year = convert_thai_date(date) if year_match else "Unknown"

        # Filter by year
        if year != "all" and news_year != year:
            continue

        # Extract full content
        content = extract_content(link)

        # Append news data as dictionary
        news_data.append({
            "title": title,
            "date": date,
            "year": news_year,
            "content": content,
            "link": link,
            "publisher": "tna",
            "type": category
        })

    return news_data


def scrape_tna(news_type="all", year="all"):
    """Scrapes news from TNA based on category and year."""
    print(
        f"Scraping news type: {news_type}, Year: {year}, from Publisher: tna")

    # Replace "foreign" with "world"
    if news_type != "all":
        categories = [news_type.replace("foreign", "world")]
    else:
        categories = VALID_TYPES

    # Convert year to integer if not "all"
    try:
        year = int(year) if year != "all" and year.isdigit() else "all"
    except ValueError:
        year = "all"

    news_data = []
    for category in categories:
        news_data.extend(get_news(category, year))

    return news_data
