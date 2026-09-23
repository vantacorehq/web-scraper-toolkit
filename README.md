Web Scraper Toolkit
Modular Python scraper built for speed and reliability — pulls structured data from any website, handles pagination and failures automatically, and exports clean results ready to use.
Features
- Smart pagination handling
- Automatic retry on failed requests
- Export to CSV or JSON
- Built for scale — from single pages to full sites
Tech stack
Python · Requests · BeautifulSoup
Status
Actively maintained. Custom builds available for client projects.
Get in touch
Open for freelance work — DM on Twitter for custom scraping & automation projects.
## Usage

```bash
pip install -r requirements.txt
python scraper.py
python scraper.py --pages 3 --output hn_data.csv
```

## Sample output

See [`sample_output.csv`](sample_output.csv) for an example of the collected data.
