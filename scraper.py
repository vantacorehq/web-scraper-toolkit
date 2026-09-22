"""
web-scraper-toolkit
--------------------
Собирает заголовки и ссылки постов с главной страницы
https://news.ycombinator.com и сохраняет результат в CSV-файл.

Как это работает (коротко, чтобы объяснить клиенту):
1. Скачиваем HTML-страницу обычным HTTP-запросом (requests).
2. С помощью BeautifulSoup находим в HTML все посты и достаём
   из них заголовок и ссылку.
3. Записываем список постов в CSV-файл, который можно открыть
   в Excel/Google Sheets.

Использование:
    python scraper.py
    python scraper.py --pages 3 --output hn_data.csv
"""

import argparse
import csv
import sys
import time
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://news.ycombinator.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PortfolioScraperBot/1.0)"
}
REQUEST_TIMEOUT = 10  # секунд


def fetch_page(url: str) -> str:
    """Скачивает HTML-страницу по ссылке и возвращает её как текст."""
    response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()  # выбросит ошибку, если сервер ответил не 200 OK
    return response.text


def parse_stories(html: str) -> list[dict]:
    """Находит в HTML посты и возвращает список словарей {title, link}."""
    soup = BeautifulSoup(html, "html.parser")
    stories = []

    for row in soup.select("tr.athing"):
        title_tag = row.select_one("span.titleline > a")
        if not title_tag:
            continue  # пропускаем строки, где не нашли заголовок

        title = title_tag.get_text(strip=True)
        link = title_tag.get("href", "")

        # У постов вида "Ask HN" ссылка внутренняя (относительная),
        # поэтому достраиваем её до полного адреса.
        if link.startswith("item?"):
            link = BASE_URL + link

        stories.append(
            {
                "title": title,
                "link": link,
                "scraped_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            }
        )

    return stories


def get_next_page_url(html: str) -> str | None:
    """Ищет на странице ссылку 'More' для перехода на следующую страницу."""
    soup = BeautifulSoup(html, "html.parser")
    more_link = soup.select_one("a.morelink")
    if more_link and more_link.get("href"):
        return BASE_URL + more_link["href"]
    return None


def save_to_csv(stories: list[dict], output_path: str) -> None:
    """Сохраняет список постов в CSV-файл."""
    fieldnames = ["title", "link", "scraped_at"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stories)


def scrape_pages(num_pages: int, delay: float) -> list[dict]:
    """Собирает посты с нужного количества страниц HN."""
    all_stories: list[dict] = []
    url = BASE_URL

    for page_num in range(1, num_pages + 1):
        print(f"Скачиваю страницу {page_num}: {url}")

        try:
            html = fetch_page(url)
        except requests.RequestException as e:
            print(f"Не удалось скачать страницу: {e}", file=sys.stderr)
            break

        stories = parse_stories(html)
        print(f"  Найдено постов: {len(stories)}")
        all_stories.extend(stories)

        if page_num == num_pages:
            break

        next_url = get_next_page_url(html)
        if not next_url:
            print("Больше страниц нет, останавливаюсь.")
            break

        url = next_url
        time.sleep(delay)  # небольшая пауза, чтобы не спамить сервер запросами

    return all_stories


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape Hacker News into a CSV file.")
    parser.add_argument("--pages", type=int, default=1, help="Сколько страниц собрать (по умолчанию 1)")
    parser.add_argument("--output", type=str, default="hn_data.csv", help="Имя выходного CSV-файла")
    parser.add_argument("--delay", type=float, default=1.0, help="Пауза между запросами страниц, сек")
    args = parser.parse_args()

    stories = scrape_pages(args.pages, args.delay)

    if not stories:
        print("Не удалось собрать ни одного поста.", file=sys.stderr)
        sys.exit(1)

    save_to_csv(stories, args.output)
    print(f"\nГотово! Сохранено {len(stories)} постов в файл: {args.output}")


if __name__ == "__main__":
    main()
