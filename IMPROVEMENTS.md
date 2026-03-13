# API Hub — Improvements & Changelog

## v2.0 — Dark Glass Terminal Redesign (March 2026)

This release replaced the entire frontend with the Dark Glass Terminal (DGT) design system and fixed several data-loading issues that prevented API responses from rendering.

---

### Design System — Dark Glass Terminal

Replaced Bootstrap 5 + purple gradient glassmorphism with a fully custom design system.

| Before | After |
|--------|-------|
| Bootstrap 5 | Custom DGT CSS (`dark-glass-terminal.css`) |
| Purple gradient background | Void-black layered backgrounds |
| Poppins font | Space Grotesk (UI) + Fira Code (mono) |
| White cards with blur | Dark glass panels with neon accents |
| Bootstrap nav | Persistent shell sidebar + topbar |
| No global utilities | `Utils.timeAgo()`, `Utils.formatDate()`, `Utils.formatNum()` |
| No global notifications | `showToast(msg, type)` available on all pages |

Shell chrome added to `base.html`:
- Topbar with logo, command palette, live clock
- Collapsible sidebar with navigation and API status indicators
- Live ticker bar at the bottom
- Global jQuery 3.7.1 and Utils object loaded for all pages

---

### Pages Rewritten

All 5 templates fully rewritten to extend `base.html`.

**index.html — Intelligence Dashboard**
- 4 metric cards with SVG sparklines: news count, temperature, BTC price, trending repos
- 2x2 panel grid: latest news, current weather, top cryptos, trending repos
- Live ticker showing BTC and weather city
- Welcome toast on load

**weather.html — Weather Station**
- DGT search bar with SEARCH, MY LOCATION, SAVE buttons
- Saved cities as chip elements (localStorage)
- Current conditions panel: big icon, large temp, detail grid, sunrise/sunset bar
- 5-day forecast in fc-grid layout

**news.html — Global News Center**
- Mode toggle: Global Trending / Local News
- Global controls: search, category select, country select (13 countries)
- Local controls: GPS detection via Nominatim reverse geocoding
- Article cards with image, source badge, timeAgo, title, description
- Load More pagination

**crypto.html — Crypto Tracker**
- 4 tabs: Live Prices, My Portfolio, Trending, Alerts
- Live prices table: top 50 by market cap with coin images, 24h/7d change, market cap
- Portfolio: add holdings, real-time P/L calculations, remove holdings
- Alerts: above/below price targets stored in localStorage
- Trending: CoinGecko trending coins grid
- Auto-refreshes every 60 seconds

**github.html — GitHub Explorer**
- 5 tabs: Trending, Favorites, Languages, Results, Details
- Trending repos with daily/weekly/monthly filter
- Search with quick-filter buttons (Popular, Recent, JS, PY, TS, RS, GO, ML)
- Favorites saved to localStorage
- Full repo details: stats, topics, license, homepage link

---

### Infrastructure Added

- `app/utils/logger.py` — structured rotating file logger, outputs to `logs/dashboard.log`
- `app/utils/rate_limit.py` — Flask-Limiter, 200 req/day + 50 req/hour per IP
- `/health` endpoint returning JSON API status

---

### Bug Fixes

**Jinja2 TemplateSyntaxError: Missing end of comment tag**
CSS ID selectors written as `{#element{` were parsed as Jinja2 comment tags.
Fixed by adding a space: `{ #element {`.

**ReferenceError: $ is not defined**
jQuery was missing from `base.html`. Added to `<head>` before all page scripts.

**ReferenceError: Utils is not defined**
The `Utils` object (`timeAgo`, `formatDate`, `formatNum`) was referenced in all page
templates but never defined. Added to `base.html` immediately after jQuery.

**SyntaxError: unexpected token: string literal (weather.html)**
City-chip onclick handlers used curly/smart quotes (U+2018/U+2019) from copy-paste,
breaking JS string concatenation. Fixed by converting to data-attribute pattern:
`data-city="'+c+'"` with `onclick="loadWeather(this.dataset.city)"`.

**SyntaxError: unexpected token: string literal (github.html)**
Same smart-quote issue on the repo card VIEW DETAILS button and the
`data-repo-json` attribute. Fixed using `data-owner`/`data-repo` attributes
and `data-repo-json` with `&quot;` encoding.

---

### Feature Comparison

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Design | Bootstrap + purple gradient | Dark Glass Terminal |
| News countries | US only | 13 countries |
| News modes | Single feed | Global + Local with GPS |
| Crypto | Price table only | Portfolio, P/L, alerts, trending |
| Weather | Manual search | GPS detection + saved cities |
| GitHub | Trending + search | + Favorites, language browser, full details |
| Data persistence | Partial | localStorage across all pages |
| Notifications | None | Global toast system |
| Logging | None | Structured rotating file log |
| Rate limiting | None | Flask-Limiter on all routes |
| Health check | None | `/health` endpoint |

---

## v1.0 — Initial Release

- Flask application factory with Blueprint-based routing
- 4 API integrations: NewsAPI, OpenWeatherMap, CoinGecko, GitHub
- Bootstrap 5 glassmorphism UI with purple gradient
- Basic news filtering by category
- Weather search by city name
- Crypto price table (top coins)
- GitHub trending and repository search
- localStorage for weather saved cities and crypto portfolio

---

## Planned — v2.1

- Crypto price history charts (Chart.js)
- Browser push notifications for price alerts
- Portfolio export to CSV
- WebSocket real-time price stream
- User authentication with cloud-sync preferences
- Skeleton loader states for slow connections
- Language color dots on GitHub repo cards
- Mobile sidebar overlay fix
