# Skill: web_scraping

## Purpose
Extract data from websites using curl, Python (BeautifulSoup, requests), or headless browsers.

## When to use
- Extracting structured data from web pages
- Downloading content from URLs
- Parsing HTML tables, lists, or specific elements
- Crawling multiple pages for data collection
- When no API is available for the data source

## How to execute

**Simple page fetch:**
```bash
curl -sL "https://example.com" | head -100
```

**Extract all links from a page:**
```bash
pip install beautifulsoup4 requests --quiet && python3 -c "
import requests
from bs4 import BeautifulSoup

r = requests.get('https://example.com')
soup = BeautifulSoup(r.text, 'html.parser')
for a in soup.find_all('a', href=True):
    print(a['href'], '-', a.get_text(strip=True)[:80])
"
```

**Extract a table to CSV:**
```bash
python3 -c "
import requests, csv, os
from bs4 import BeautifulSoup

r = requests.get('https://example.com/data-page')
soup = BeautifulSoup(r.text, 'html.parser')
table = soup.find('table')

if not table:
    print('No table found')
    exit(1)

rows = []
for tr in table.find_all('tr'):
    cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
    rows.append(cells)

os.makedirs('./output', exist_ok=True)
with open('./output/scraped_data.csv', 'w', newline='') as f:
    csv.writer(f).writerows(rows)
print(f'Extracted {len(rows)} rows to ./output/scraped_data.csv')
"
```

**Extract specific elements by CSS selector:**
```bash
python3 -c "
import requests
from bs4 import BeautifulSoup

r = requests.get('https://example.com')
soup = BeautifulSoup(r.text, 'html.parser')

# Adjust selector to match the target page
items = soup.select('div.item h2')
for i, item in enumerate(items, 1):
    print(f'{i}. {item.get_text(strip=True)}')
"
```

**Scrape with headers (avoid blocks):**
```bash
python3 -c "
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-US,en;q=0.9',
}
r = requests.get('https://example.com', headers=headers, timeout=15)
r.raise_for_status()

soup = BeautifulSoup(r.text, 'html.parser')
title = soup.find('title')
print(f'Title: {title.get_text() if title else \"N/A\"}')
print(f'Status: {r.status_code}')
print(f'Size: {len(r.text)} bytes')
"
```

**Scrape multiple pages:**
```bash
python3 -c "
import requests, json, time, os
from bs4 import BeautifulSoup

base_url = 'https://example.com/page/'
all_data = []

for page in range(1, 6):  # Pages 1-5
    r = requests.get(f'{base_url}{page}', timeout=15)
    if r.status_code != 200:
        print(f'Page {page}: HTTP {r.status_code}')
        break
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.select('.item')
    for item in items:
        all_data.append({
            'title': item.select_one('h2').get_text(strip=True) if item.select_one('h2') else '',
            'desc': item.select_one('p').get_text(strip=True) if item.select_one('p') else '',
        })
    print(f'Page {page}: {len(items)} items')
    time.sleep(1)  # Be respectful

os.makedirs('./output', exist_ok=True)
with open('./output/scraped.json', 'w') as f:
    json.dump(all_data, f, indent=2)
print(f'Total: {len(all_data)} items saved')
"
```

**Download a file:**
```bash
curl -sL "https://example.com/data.csv" -o ./data/downloaded.csv
echo "Downloaded: $(wc -l < ./data/downloaded.csv) lines, $(wc -c < ./data/downloaded.csv) bytes"
```

**Extract JSON-LD / structured data:**
```bash
python3 -c "
import requests, json
from bs4 import BeautifulSoup

r = requests.get('https://example.com')
soup = BeautifulSoup(r.text, 'html.parser')
for script in soup.find_all('script', type='application/ld+json'):
    data = json.loads(script.string)
    print(json.dumps(data, indent=2))
"
```

## Output contract
- stdout: extracted data or confirmation
- exit_code 0: success
- exit_code 1: page not found, parse error, or blocked

## Evaluate output
If 403/429: site is blocking — add headers, reduce rate, or use a different approach.
If empty results: inspect the HTML — the selector might not match (page may use JS rendering).
Always add `time.sleep()` between requests to avoid overwhelming the server.
For JS-rendered pages: consider using `playwright` or `selenium` if available.
