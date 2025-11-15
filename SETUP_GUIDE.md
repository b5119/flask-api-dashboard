# 🚀 API Hub - Quick Setup Guide

Get your dashboard running in **5 minutes**! Follow these simple steps.

## 📋 Prerequisites

- Python 3.8+ installed
- Internet connection

## 🔑 Step 1: Get Your FREE API Keys

### 1️⃣ News API (Required)
**Time:** 2 minutes | **Cost:** FREE

1. Visit: https://newsapi.org/register
2. Enter your email and name
3. Click "Submit"
4. Copy your API key from the confirmation page
5. ✅ **Save it** - You'll need it for the `.env` file

### 2️⃣ OpenWeatherMap API (Required)
**Time:** 2 minutes | **Cost:** FREE

1. Visit: https://openweathermap.org/api
2. Click "Sign Up" (top right)
3. Create account with email
4. Go to "API keys" tab
5. Copy the default API key (or create new one)
6. ⏰ **Note:** Key activation takes 10-15 minutes
7. ✅ **Save it** - You'll need it for the `.env` file

### 3️⃣ GitHub Token (Optional)
**Time:** 1 minute | **Cost:** FREE

**Without token:** 60 requests/hour ✅ Sufficient for personal use
**With token:** 5,000 requests/hour

To get a token (optional):
1. Visit: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name: `API Hub Dashboard`
4. Select scopes: `public_repo` (read public repositories)
5. Click "Generate token"
6. ✅ **Save it** immediately (shown only once!)

### 4️⃣ Crypto API (No key needed!)
**CoinGecko API** - Works out of the box! ✨

---

## ⚙️ Step 2: Configure Your Dashboard

### Create `.env` file

In your project root, create a file named `.env`:

```bash
# Required API Keys
NEWSAPI_KEY=your_newsapi_key_here
OPENWEATHER_API_KEY=your_openweathermap_key_here

# Optional (GitHub works without token, but with limits)
GITHUB_TOKEN=your_github_token_here

# Flask Configuration
SECRET_KEY=your-super-secret-random-key-change-this
FLASK_ENV=development
```

### Example `.env` file:
```bash
NEWSAPI_KEY=abc123def456ghi789jkl012mno345pqr678
OPENWEATHER_API_KEY=xyz789abc123def456ghi789jkl012mno3
GITHUB_TOKEN=ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890
SECRET_KEY=my-super-secret-key-12345
FLASK_ENV=development
```

---

## 🏃 Step 3: Install & Run

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Initialize Database (Optional)
```bash
flask init_db
```

### Start the Dashboard
```bash
python run.py
```

### Open in Browser
Visit: **http://localhost:5000** 🎉

---

## ✨ Features You Can Use NOW

### 🌤️ Weather Station
- **Auto-location detection** - Click "My Location" to use GPS
- **Save favorite cities** - One-click access to saved locations
- **5-day detailed forecast** - Temperature, humidity, wind
- **No manual API needed** - Uses browser geolocation

### 📰 News Center
- Browse by category (tech, business, sports, etc.)
- Filter by country
- Real-time headlines
- Save favorite articles

### 💰 Crypto Tracker
- Live prices for 100+ cryptocurrencies
- 24-hour price changes
- Trending coins
- Market cap rankings
- **No API key required** - Uses free CoinGecko API

### 🐙 GitHub Explorer
- Search repositories
- Trending repos by language
- Repository analytics
- Contributor insights
- **Works without token** - 60 requests/hour is plenty

---

## 🎯 Usage Tips

### Weather Station
1. **First time:** Allow browser location access for auto-detection
2. **Save cities:** Search for a city → Click "Save" → Quick access next time
3. **Default city:** Last searched city becomes your default

### Optimal API Key Usage
- **News API:** 100 requests/day (FREE tier) = Check news 4x/day
- **Weather API:** 1,000 calls/day (FREE tier) = Check every 2 minutes!
- **GitHub:** 60/hour without token = 1 request/minute
- **Crypto:** Unlimited (FREE) = No worries!

---

## 🆘 Troubleshooting

### "API key not found" error
1. Check `.env` file exists in project root
2. Verify key names match exactly: `NEWSAPI_KEY`, `OPENWEATHER_API_KEY`
3. Restart Flask server after editing `.env`

### Weather API not working
- Wait 10-15 minutes after getting key (activation time)
- Test key: `https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_KEY`

### Can't detect my location
- Allow browser location permission
- Use manual city search instead
- Check browser console for errors

### News not loading
- Verify API key is active on newsapi.org
- Check you haven't exceeded 100 requests/day
- Try different category/country

---

## 🎨 Customization

### Change Default City
Edit `app/templates/weather.html`:
```javascript
const DEFAULT_CITY = 'YourCity';  // Line 150
```

### Add More News Categories
Edit `app/routes/news.py`:
```python
categories = ['your-category', ...]  // Add to list
```

---

## 📊 API Limits Summary

| API | Free Tier | Upgrade Cost | What You Get |
|-----|-----------|--------------|--------------|
| NewsAPI | 100 req/day | $449/month | Unlimited requests |
| OpenWeather | 1,000 req/day | $40/month | Unlimited requests |
| GitHub | 60 req/hour | FREE with token | 5,000 req/hour |
| CoinGecko | Unlimited | FREE forever | ❤️ Always free |

**💡 Tip:** Free tiers are MORE than enough for personal use!

---

## 🚀 You're All Set!

Your dashboard is now ready to use with:
- ✅ Live weather with geolocation
- ✅ Real-time news from multiple sources
- ✅ Cryptocurrency price tracking
- ✅ GitHub repository explorer

**Enjoy your API Hub! 🎉**

Need help? Check the [GitHub Issues](https://github.com/b5119/flask-api-dashboard/issues)