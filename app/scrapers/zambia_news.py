"""
Zambia local news scraper — runs every 30 minutes via APScheduler.
Scrapes: Lusaka Times, Zambia Daily Mail, Mwebantu
Stores results in app/data/zambia_news.json
"""
import json, os, time, logging
from datetime import datetime
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
DATA_FILE = os.path.join(DATA_DIR, 'zambia_news.json')
os.makedirs(DATA_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}
TIMEOUT = 12

SOURCES = [
    {
        'name': 'Lusaka Times',
        'url': 'https://www.lusakatimes.com/',
        'article_selector': 'article.jeg_post',
        'title_selector': 'h3.jeg_post_title a',
        'img_selector': 'div.jeg_thumb img',
        'time_selector': 'div.jeg_meta_date a',
        'category': 'zambia',
    },
    {
        'name': 'Zambia Daily Mail',
        'url': 'https://www.daily-mail.co.zm/',
        'article_selector': 'article',
        'title_selector': 'h2 a, h3 a',
        'img_selector': 'img.attachment-medium',
        'time_selector': 'time',
        'category': 'zambia',
    },
    {
        'name': 'Mwebantu',
        'url': 'https://www.mwebantu.com/',
        'article_selector': 'article',
        'title_selector': 'h2 a, h3 a',
        'img_selector': 'img',
        'time_selector': 'time, .entry-date',
        'category': 'zambia',
    },
]


def scrape_source(source):
    articles = []
    try:
        resp = requests.get(source['url'], headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = soup.select(source['article_selector'])[:12]

        for item in items:
            try:
                title_el = item.select_one(source['title_selector'])
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                url = title_el.get('href', '')
                if not url.startswith('http'):
                    from urllib.parse import urljoin
                    url = urljoin(source['url'], url)

                img_el = item.select_one(source['img_selector'])
                img = ''
                if img_el:
                    img = (img_el.get('data-src') or
                           img_el.get('data-lazy-src') or
                           img_el.get('src') or '')
                    if img and not img.startswith('http'):
                        from urllib.parse import urljoin
                        img = urljoin(source['url'], img)

                time_el = item.select_one(source['time_selector'])
                pub_time = ''
                if time_el:
                    pub_time = (time_el.get('datetime') or
                                time_el.get_text(strip=True) or '')

                if title and url and len(title) > 10:
                    articles.append({
                        'title': title,
                        'url': url,
                        'urlToImage': img,
                        'publishedAt': pub_time or datetime.utcnow().isoformat(),
                        'source': {'name': source['name']},
                        'description': '',
                        'category': source['category'],
                        'scraped_at': datetime.utcnow().isoformat(),
                    })
            except Exception as e:
                logger.debug(f"Error parsing article from {source['name']}: {e}")
                continue

        logger.info(f"Scraped {len(articles)} articles from {source['name']}")
    except Exception as e:
        logger.warning(f"Failed to scrape {source['name']}: {e}")
    return articles


def run_scraper():
    logger.info("Running Zambia news scraper...")
    all_articles = []
    for source in SOURCES:
        articles = scrape_source(source)
        all_articles.extend(articles)
        time.sleep(1.5)

    # Deduplicate by URL
    seen = set()
    unique = []
    for a in all_articles:
        if a['url'] not in seen:
            seen.add(a['url'])
            unique.append(a)

    result = {
        'articles': unique,
        'total': len(unique),
        'last_updated': datetime.utcnow().isoformat(),
        'sources': [s['name'] for s in SOURCES],
    }
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    logger.info(f"Scraper done: {len(unique)} articles saved")
    return result


def get_cached_articles():
    """Return cached articles, triggering a fresh scrape if cache is stale."""
    if not os.path.exists(DATA_FILE):
        return run_scraper()
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        last = datetime.fromisoformat(data.get('last_updated', '2000-01-01'))
        age_minutes = (datetime.utcnow() - last).total_seconds() / 60
        if age_minutes > 35:
            return run_scraper()
        return data
    except Exception:
        return run_scraper()
