import csv
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin




URL = "https://books.toscrape.com/catalogue/page-1.html"  # Replace with the actual URL you want to scrape

MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
}




def scrape_page(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    books = []
    for article in soup.select("article.product_pod"):
        title = article.h3.a["title"]
        price = float(article.select_one("p.price_color").text.replace("£", ""))
        rating_word = article.select_one("p.star-rating")["class"][1]
        books.append({
            "title": title,
            "price_gbp": price,
            "rating": MAP.get(rating_word, 0),
        })

    next_link = soup.select_one("li.next a")
    next_url = urljoin(url, next_link["href"]) if next_link else None
    return books, next_url


def main():
    all_books = []
    url = URL
    while url:
        print(f"Scraping {url}")
        books, url = scrape_page(url)
        all_books.extend(books)
        time.sleep(0.5)  # be polite to the server

    with open("books.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price_gbp", "rating"])
        writer.writeheader()
        writer.writerows(all_books)

    print(f"Saved {len(all_books)} books to books.csv")


if __name__ == "__main__":
    main()
