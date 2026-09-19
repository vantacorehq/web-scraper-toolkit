import requests from bs4 import BeautifulSoup import csv
def scrape_hackernews(): url = "https://news.ycombinator.com/" response = requests.get(url) soup = BeautifulSoup(response.text, "html.parser")
titles = soup.find_all("span", class_="titleline")

results = []
for title in titles:
    link = title.find("a")
    if link:
        results.append({
            "title": link.text,
            "url": link.get("href")
        })

with open("headlines.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "url"])
    writer.writeheader()
    writer.writerows(results)

print(f"Saved {len(results)} headlines to headlines.csv")
if name == "main": scrape_hackernews()
 import requests from bs4 import BeautifulSoup import csv
def scrape_hackernews(): url = "https://news.ycombinator.com/" response = requests.get(url) soup = BeautifulSoup(response.text, "html.parser")
titles = soup.find_all("span", class_="titleline")

results = []
for title in titles:
    link = title.find("a")
    if link:
        results.append({
            "title": link.text,
            "url": link.get("href")
        })

with open("headlines.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "url"])
    writer.writeheader()
    writer.writerows(results)

print(f"Saved {len(results)} headlines to headlines.csv")
if __name__ =="__main__": scrape_hackernews() 
