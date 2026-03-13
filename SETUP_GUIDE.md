# API Hub — Dark Glass Terminal Dashboard

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

A multi-API intelligence dashboard built with Flask, featuring the **Dark Glass Terminal** design system — a dark, glassmorphic UI with cyan/magenta/amber accents, monospace typography, and a persistent command shell.

---

## Features

### Intelligence Dashboard (Overview)
- Live metric cards: latest news count, temperature, BTC price, trending repos
- Sparkline graphs per metric
- 2×2 panel grid: news widget, weather widget, crypto widget, GitHub widget
- Live ticker bar with BTC price and weather city
- Auto-refresh every 5 minutes

### Global News Center
- Global trending news from 13 countries
- Local news via GPS auto-detection (Nominatim reverse geocoding)
- 7 categories: General, Business, Technology, Entertainment, Health, Science, Sports
- Real-time search with 500ms debounce
- Load More pagination

### Weather Station
- GPS auto-detection for your city
- Save unlimited cities to localStorage
- Current conditions: temperature, humidity, wind, pressure, feels like, hi/lo, sunrise/sunset
- 5-day forecast with daily summary cards

### Crypto Tracker
- Live prices for top 50 cryptocurrencies (CoinGecko, no key required)
- Portfolio management with real-time P/L calculations
- Price alerts (above/below target)
- Trending coins tab
- Auto-refresh every 60 seconds

### GitHub Explorer
- Search millions of public repositories
- Trending repos: daily, weekly, monthly
- Browse by programming language
- Save favorite repositories to localStorage
- Full repository details: stars, forks, issues, license, topics

---

## Design System — Dark Glass Terminal

### Colour Palette
| Token | Value | Role |
|-------|-------|------|
| `--bg-void` | `#05071a` | Page background |
| `--bg-base` | `#0a0e27` | Base layer |
| `--bg-panel` | `#0f1535` | Cards and panels |
| `--cyan` | `#00f0ff` | Primary accent |
| `--green` | `#00ff41` | Positive / success |
| `--magenta` | `#ff00ff` | Secondary accent |
| `--amber` | `#ffb700` | Warning / highlight |
| `--red` | `#ff3355` | Negative / error |

### Typography
- **UI:** Space Grotesk
- **Mono:** Fira Code

### Shell Chrome
- Persistent topbar: logo, command palette, live clock
- Collapsible sidebar: navigation, API status indicators
- Live ticker bar at the bottom
- Toast notification system (`showToast(msg, type)`)
- Global `Utils` object: `timeAgo()`, `formatDate()`, `formatNum()`

---

## Quick Start

### 1. Clone & setup
```bash
git clone https://github.com/b5119/flask-api-dashboard.git
cd flask-api-dashboard
python -m venv venv
source venv/bin/activate       # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

### 2. Get free API keys
| API | Time | Link |
|-----|------|------|
| NewsAPI | 2 min | https://newsapi.org/register |
| OpenWeatherMap | 2 min | https://openweathermap.org/api |
| GitHub Token | 1 min, optional | https://github.com/settings/tokens |
| CoinGecko | — | No key needed |

### 3. Create `.env`
```env
SECRET_KEY=your-secret-key
NEWSAPI_KEY=your_newsapi_key
OPENWEATHER_API_KEY=your_openweathermap_key
GITHUB_TOKEN=optional_github_token
FLASK_ENV=development
```

### 4. Run
```bash
python run.py
```

Visit **http://localhost:5000**

---

## Project Structure
```
flask-api-dashboard/
├── app/
│   ├── __init__.py              # Application factory
│   ├── api/                     # External API service wrappers
│   │   ├── news_api.py
│   │   ├── weather_api.py
│   │   ├── crypto_api.py
│   │   └── github_api.py
│   ├── routes/                  # Flask route controllers
│   │   ├── main.py              # Dashboard + /health + /dashboard/data
│   │   ├── news.py
│   │   ├── weather.py
│   │   ├── crypto.py
│   │   └── github.py
│   ├── templates/               # Jinja2 templates
│   │   ├── base.html            # DGT shell: topbar, sidebar, ticker, Utils
│   │   ├── index.html           # Intelligence Dashboard
│   │   ├── news.html            # Global News Center
│   │   ├── weather.html         # Weather Station
│   │   ├── crypto.html          # Crypto Tracker
│   │   └── github.html          # GitHub Explorer
│   ├── static/
│   │   └── css/
│   │       └── dark-glass-terminal.css   # Full DGT design system
│   └── utils/
│       ├── __init__.py
│       ├── logger.py            # Structured logging
│       └── rate_limit.py        # Flask-Limiter (200/day, 50/hour)
├── logs/
│   └── dashboard.log
├── config.py
├── run.py
├── requirements.txt
├── README.md
└── IMPROVEMENTS.md
```

---

## Tech Stack

### Backend
| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.0 | Web framework |
| Flask-Limiter | — | Rate limiting |
| Requests | 2.31 | HTTP client |
| Python-dotenv | 1.0 | Environment config |

### Frontend
| Library | Purpose |
|---------|---------|
| Dark Glass Terminal CSS | Custom DGT design system |
| jQuery 3.7.1 | DOM + AJAX |
| Space Grotesk / Fira Code | Typography (Google Fonts) |

### APIs
| API | Free Limit | Key Required |
|-----|-----------|--------------|
| NewsAPI | 100 req/day | Yes |
| OpenWeatherMap | 1,000 req/day | Yes |
| CoinGecko | Unlimited | No |
| GitHub | 60 req/hr (5K with token) | Optional |

---

## Data Persistence

All user data is stored in **localStorage** — no database or authentication required.

| Page | localStorage Keys |
|------|-------------------|
| Weather | `weather_saved_cities`, `weather_default_city` |
| Crypto | `crypto_portfolio`, `crypto_alerts` |
| GitHub | `github_favorites`, `github_search_count` |

---

## Health Check
```bash
curl http://localhost:5000/health
```
```json
{
  "status": "ok",
  "apis": { "news": "ok", "weather": "ok", "crypto": "ok", "github": "ok" }
}
```

---

## Roadmap

### Completed
- Dark Glass Terminal design system across all 5 pages
- Live Intelligence Dashboard with sparklines
- Global + local news with GPS detection
- Weather with saved cities and 5-day forecast
- Crypto portfolio with real-time P/L
- GitHub explorer with favorites and repo details
- Structured logging and rate limiting
- jQuery + Utils loaded globally via base.html

### Planned
- Browser push notifications for price alerts
- Portfolio export to CSV
- Dark/light theme toggle
- WebSocket real-time price stream
- User authentication + cloud-sync

---

## Author

**Frank Bwalya**
- GitHub: [b5119](https://github.com/b5119)
- Email: bwalyafrank61@gmail.com

---

## Acknowledgements

- [NewsAPI](https://newsapi.org) — News data
- [OpenWeatherMap](https://openweathermap.org) — Weather data
- [CoinGecko](https://coingecko.com) — Crypto data
- [GitHub API](https://docs.github.com/en/rest) — Repository data
- [Nominatim](https://nominatim.org) — Reverse geocoding

---
