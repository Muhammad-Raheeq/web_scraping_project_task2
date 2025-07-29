import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv
def get_headlines_for_date(date_str):
    url = f"https://www.africanews.com/{date_str}/"
    headers = {"User-Agent": "Chrome"}
    try:
        res = requests.get(url, headers=headers, timeout=1)
        soup = BeautifulSoup(res.text, "html.parser")
        headlines = []
        for h2 in soup.find_all("h2"):
            a = h2.find("a")
            if a and a.text.strip():
                title = a.text.strip()
                link = a['href']
                full_link = link if link.startswith("http") else "https://www.africanews.com" + link
                headlines.append((title, full_link))  
        return headlines
    except Exception as e:
        return []
start_date = datetime(2015, 12, 21)
end_date = datetime.today()
print(end_date)
with open("africanews.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Date", "Headline", "URL", "Description"])
    day_count = (end_date - start_date).days
    print(day_count)
    for n in range(day_count):
        current_date = start_date + timedelta(n)
        date_path = current_date.strftime("%Y/%m/%d")
        headlines = get_headlines_for_date(date_path)
        for title, link in headlines:
            writer.writerow([current_date.strftime("%Y-%m-%d"),title,link,title ])
print("scraping complete headlines saved to 'africanews.csv'.")
