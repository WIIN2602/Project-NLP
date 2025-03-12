import cloudscraper
from bs4 import BeautifulSoup
import re
from datetime import datetime

VALID_TYPES = ["entertainment", "politics", "sport", "foreign"]
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Define fixed pages for each year
PAGE_NUMBERS = {
    "entertainment": {2025: 1, 2024: 200, 2023: 800, 2022: 1000},
    "politics": {2025: 1, 2024: 1000, 2023: 3000, 2022: 5000},
    "sport": {2025: 1, 2024: 200, 2023: 1300, 2022: 2500},
    "foreign": {2025: 1, 2024: 200, 2023: 800, 2022: 1300}
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
    datetime = date_str
    datetime = convert_thai_month(datetime)
    date = datetime.split(" ")
    day = date[1]
    month = date[2]
    year = int(date[3])-543
    time = date[5]
    day = day if int(day) >= 10 else f"0{day}"
    date_format = f'{year}-{month}-{day} {time}:00'
    return date_format


def clean_text(text):
    """Cleans text by removing unwanted characters."""
    return text.replace(",", " ").replace('"', " ").strip()


def convert_thai_date(thai_date):
    """Converts Thai Buddhist calendar years to Gregorian calendar years."""
    year_match = re.search(r"(\d{4})", thai_date)
    return int(year_match.group(1)) - 543 if year_match else None


def extract_content(link):
    """Fetches and extracts the full content of a news article."""
    try:
        news_response = scraper.get(link)
        news_soup = BeautifulSoup(news_response.text, "html.parser")

        content_tag = news_soup.find("div", class_="td-post-content")
        if content_tag:
            paragraphs = content_tag.find_all("p", style=False)
            content = "\n".join([p.text.strip()
                                for p in paragraphs if p.text.strip()])
        else:
            content = "❌ ไม่พบเนื้อหาข่าว"

        return clean_text(content)

    except Exception as e:
        return f"⚠️ Error: {str(e)}"


def get_news(category, year):
    """Fetch news articles for a given category and year with fixed page numbers and content extraction."""
    news_data = []
    page = PAGE_NUMBERS.get(category, {}).get(year, 1)
    base_url = f"https://www.matichon.co.th/{category}/page/{page}"

    response = scraper.get(base_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"⚠️ ไม่สามารถเข้าถึง {base_url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("div", class_="item-details")

    for article in articles:
        title_tag = article.find("h3", class_="entry-title td-module-title")
        link_tag = article.find("a", href=True)
        date_tag = article.find(
            "time", class_="entry-date updated td-module-date")

        if not title_tag or not link_tag:
            continue

        title = clean_text(title_tag.text.strip())
        link = clean_text(link_tag["href"])
        date = clean_text(date_tag.text.strip()) if date_tag else "Unknown"
        date_obj = convert_date(date_tag.text.strip()
                                ) if date_tag else "Unknown"
        # Extract year from date and convert from Buddhist to Gregorian
        year_match = re.search(r"(\d{4})", date)
        news_year = convert_thai_date(date) if year_match else "ไม่พบปี"

        # Filter articles based on the requested year
        if year != "all" and news_year != year:
            continue

        # Extract full content from the article page
        content = extract_content(link)

        # Append news data in list format as per your original requirement
        news_data.append({
            "title": title,
            "date": date_obj,
            "year": news_year,
            "content": content,
            "link": link,
            "publisher": "matichon",
            "type": category
        })

    return news_data


def scrape_matichon(news_type="all", year="all"):
    """Scrapes news from Matichon based on category and year."""
    print(
        f"Scraping news type: {news_type}, Year: {year}, from Publisher: matichon")

    # Convert "all" to the list of all valid categories
    categories = VALID_TYPES if news_type == "all" else [news_type]

    # Convert year to integer if not "all"
    year = int(year) if year != "all" else "all"

    news_data = []
    for category in categories:
        news_data.extend(get_news(category, year))

    return news_data
