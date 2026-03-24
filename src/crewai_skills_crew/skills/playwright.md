# Skill: playwright

## Purpose
Automate browser interactions — testing, scraping JS-rendered pages, taking screenshots, filling forms, and generating PDFs using Playwright.

## When to use
- Testing web applications end-to-end
- Scraping pages that require JavaScript rendering (SPAs, dynamic content)
- Taking screenshots or generating PDFs of web pages
- Automating form submissions, clicks, and navigation
- When curl/BeautifulSoup can't get the data (JS-rendered content)

## Prerequisites
- Python 3.8+
- Install: `pip install playwright && playwright install --with-deps chromium`
  - `--with-deps` auto-installs OS-level dependencies (works on Ubuntu/Debian/CentOS/macOS)
  - Only `chromium` is needed for most tasks (smaller than installing all browsers)

## How to execute

**Take a screenshot of a page:**
```bash
pip install playwright --quiet && playwright install --with-deps chromium 2>/dev/null

python3 -c "
from playwright.sync_api import sync_playwright
import os

os.makedirs('./output', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1280, 'height': 720})
    page.goto('https://example.com', wait_until='networkidle')
    page.screenshot(path='./output/screenshot.png', full_page=True)
    browser.close()

print('Screenshot saved to ./output/screenshot.png')
"
```

**Generate a PDF of a page:**
```bash
python3 -c "
from playwright.sync_api import sync_playwright
import os

os.makedirs('./output', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://example.com', wait_until='networkidle')
    page.pdf(path='./output/page.pdf', format='A4', print_background=True)
    browser.close()

print('PDF saved to ./output/page.pdf')
"
```

**Scrape JS-rendered content:**
```bash
python3 -c "
from playwright.sync_api import sync_playwright
import json, os

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://example.com', wait_until='networkidle')

    # Wait for a specific element to appear
    page.wait_for_selector('h1', timeout=10000)

    # Extract text content
    title = page.text_content('h1')
    print(f'Title: {title}')

    # Extract all links
    links = page.eval_on_selector_all('a[href]', '''
        elements => elements.map(el => ({
            text: el.textContent.trim(),
            href: el.href
        }))
    ''')
    for link in links[:20]:
        print(f'  {link[\"href\"]} — {link[\"text\"][:60]}')

    browser.close()
"
```

**Scrape a table from a JS-rendered page:**
```bash
python3 -c "
from playwright.sync_api import sync_playwright
import csv, os

os.makedirs('./output', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://example.com/data', wait_until='networkidle')

    # Extract table data
    rows = page.eval_on_selector_all('table tr', '''
        rows => rows.map(row => {
            const cells = row.querySelectorAll('td, th');
            return Array.from(cells).map(cell => cell.textContent.trim());
        })
    ''')

    with open('./output/table_data.csv', 'w', newline='') as f:
        csv.writer(f).writerows(rows)

    print(f'Extracted {len(rows)} rows to ./output/table_data.csv')
    browser.close()
"
```

**Fill and submit a form:**
```bash
python3 -c "
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://example.com/login', wait_until='networkidle')

    # Fill form fields
    page.fill('input[name=\"username\"]', 'myuser')
    page.fill('input[name=\"password\"]', 'mypass')

    # Click submit
    page.click('button[type=\"submit\"]')

    # Wait for navigation
    page.wait_for_load_state('networkidle')

    # Check result
    if 'dashboard' in page.url:
        print('Login successful!')
        print(f'Current URL: {page.url}')
    else:
        print('Login may have failed')
        print(f'Current URL: {page.url}')
        page.screenshot(path='./output/login_result.png')

    browser.close()
"
```

**Intercept network requests (capture API calls):**
```bash
python3 -c "
from playwright.sync_api import sync_playwright
import json, os

os.makedirs('./output', exist_ok=True)
captured = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Intercept XHR/fetch responses
    def handle_response(response):
        if 'api' in response.url and response.status == 200:
            try:
                body = response.json()
                captured.append({'url': response.url, 'data': body})
            except:
                pass

    page.on('response', handle_response)
    page.goto('https://example.com', wait_until='networkidle')

    # Wait for dynamic content to load
    page.wait_for_timeout(3000)

    with open('./output/api_responses.json', 'w') as f:
        json.dump(captured, f, indent=2)

    print(f'Captured {len(captured)} API responses')
    browser.close()
"
```

**Run an E2E test:**
```bash
python3 -c "
from playwright.sync_api import sync_playwright
import sys

errors = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Test 1: Homepage loads
    page.goto('https://example.com', wait_until='networkidle')
    assert page.title(), 'Page title should not be empty'
    print('✓ Homepage loads')

    # Test 2: Navigation works
    page.click('a[href=\"/about\"]')
    page.wait_for_load_state('networkidle')
    assert '/about' in page.url, f'Expected /about in URL, got {page.url}'
    print('✓ Navigation to /about works')

    # Test 3: Content is visible
    heading = page.text_content('h1')
    assert heading and len(heading) > 0, 'H1 should have content'
    print(f'✓ H1 content: {heading}')

    browser.close()

print('All tests passed!')
"
```

**Wait for specific conditions:**
```bash
python3 -c "
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://example.com')

    # Wait for element to appear
    page.wait_for_selector('.results', state='visible', timeout=15000)

    # Wait for text to appear
    page.wait_for_selector('text=Loading', state='hidden', timeout=15000)

    # Wait for network to be idle
    page.wait_for_load_state('networkidle')

    print('Page fully loaded')
    browser.close()
"
```

**Multiple pages / tabs:**
```bash
python3 -c "
from playwright.sync_api import sync_playwright
import os

os.makedirs('./output', exist_ok=True)
urls = [
    'https://example.com',
    'https://example.org',
    'https://example.net',
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    for i, url in enumerate(urls):
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')
        title = page.title()
        page.screenshot(path=f'./output/page_{i+1}.png')
        print(f'{i+1}. {url} — {title}')
        page.close()

    browser.close()
print('Done')
"
```

## Output contract
- stdout: extracted data, test results, or confirmation
- exit_code 0: success
- exit_code 1: element not found, timeout, or navigation error

## Evaluate output
If "TimeoutError": the selector doesn't match — inspect the page HTML or increase timeout.
If "Browser closed unexpectedly": may need `--with-deps` to install OS libraries.
If content is empty: the page may need more time — add `wait_for_timeout()` or `wait_for_selector()`.
Always use `headless=True` for server/CI environments.
For debugging, save a screenshot before/after critical steps.
