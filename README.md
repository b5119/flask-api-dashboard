# Flask API Dashboard Web Application

A comprehensive web application built with Flask that integrates multiple APIs into a beautiful, interactive dashboard. This project combines all our previous API integrations into one unified web interface.

## 🎯 Project Overview

This Flask web application provides:
- **Real-time Dashboard** with live API data
- **News Feed** from multiple sources
- **Weather Information** with forecasts
- **Cryptocurrency Tracker** with portfolio management
- **GitHub Repository Explorer**
- **Notification Center** for sending emails/SMS
- **User-friendly Interface** with responsive design
- **RESTful API Endpoints** for all features

## 🌟 Features

### 1. Dashboard Home
- Overview of all services
- Quick stats and summaries
- Recent updates feed
- Customizable widgets

### 2. News Center
- Browse news by category
- Search functionality
- Save favorite articles
- Multiple news sources

### 3. Weather Station
- Current weather conditions
- 7-day forecast
- Multiple locations
- Weather alerts
- Air quality index

### 4. Crypto Portfolio
- Live cryptocurrency prices
- Portfolio tracker
- Price alerts
- Historical charts
- Profit/loss calculator

### 5. GitHub Explorer
- Repository search
- Analytics and statistics
- Trending repositories
- Contributor insights
- Star history

### 6. Notification Hub
- Send emails
- Send SMS messages
- Message templates
- Scheduled notifications
- Delivery status

## 🚀 Technology Stack

### Backend
- **Flask** - Web framework
- **Flask-SQLAlchemy** - Database ORM
- **Flask-Login** - User authentication
- **Flask-WTF** - Forms and CSRF protection
- **APScheduler** - Background tasks

### Frontend
- **Bootstrap 5** - CSS framework
- **Chart.js** - Data visualization
- **Font Awesome** - Icons
- **jQuery** - DOM manipulation
- **AJAX** - Async data loading

### APIs
- NewsAPI, OpenWeatherMap, CoinGecko
- GitHub API, SendGrid, Twilio

## 📁 Project Structure

```
flask-api-dashboard/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── news.py
│   │   ├── weather.py
│   │   ├── crypto.py
│   │   ├── github.py
│   │   └── notifications.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── news.html
│   │   ├── weather.html
│   │   ├── crypto.html
│   │   ├── github.html
│   │   └── notifications.html
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── img/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── news_api.py
│   │   ├── weather_api.py
│   │   ├── crypto_api.py
│   │   ├── github_api.py
│   │   └── notification_api.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── migrations/
├── instance/
│   └── config.py
├── tests/
├── config.py
├── requirements.txt
├── run.py
├── .env.example
├── .gitignore
└── README.md
```

## 🔧 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/flask-api-dashboard.git
cd flask-api-dashboard
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 5. Initialize database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run the application
```bash
python run.py
# or
flask run
```

Visit `http://localhost:5000` in your browser.

## 🔐 Environment Variables

Create a `.env` file with the following:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_APP=run.py
FLASK_ENV=development

# Database
DATABASE_URL=sqlite:///app.db

# API Keys
NEWSAPI_KEY=your_newsapi_key
OPENWEATHER_API_KEY=your_openweather_key
GITHUB_TOKEN=your_github_token
SENDGRID_API_KEY=your_sendgrid_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_number
```

## 📊 Features in Detail

### Dashboard Overview
- Real-time data from all APIs
- Customizable widget layout
- Quick actions menu
- Activity timeline
- System health indicators

### News Features
- Filter by category, source, date
- Full-text search
- Article bookmarking
- Share to social media
- RSS feed generation

### Weather Features
- Current conditions with icons
- Hourly and daily forecasts
- Weather maps
- Location management
- Weather alerts

### Crypto Features
- Live price updates (WebSocket)
- Portfolio management
- Price alerts
- Interactive charts
- Market trends

### GitHub Features
- Repository search
- Detailed analytics
- Commit history visualization
- Contributor rankings
- Issue tracking

### Notification Features
- Email composer with templates
- SMS sender
- Bulk messaging
- Scheduled sends
- Delivery tracking

## 🎨 UI/UX Features

- **Responsive Design** - Works on desktop, tablet, mobile
- **Dark Mode** - Toggle between light/dark themes
- **Real-time Updates** - AJAX polling and WebSocket support
- **Loading States** - Skeleton screens and spinners
- **Error Handling** - User-friendly error messages
- **Accessibility** - WCAG 2.1 compliant
- **Progressive Web App** - Installable on mobile devices

## 🔌 API Endpoints

### REST API
```
GET  /api/news              - Get news articles
GET  /api/weather/:city     - Get weather data
GET  /api/crypto/:coin      - Get crypto prices
GET  /api/github/:repo      - Get repository info
POST /api/notifications     - Send notification
```

### WebSocket Events
```
connect    - Client connection
news       - Live news updates
crypto     - Live price updates
weather    - Weather updates
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_api.py
```

## 🚢 Deployment

### Heroku
```bash
heroku create your-app-name
heroku config:set FLASK_ENV=production
git push heroku main
heroku run flask db upgrade
```

### Docker
```bash
docker build -t flask-dashboard .
docker run -p 5000:5000 flask-dashboard
```

### Production Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set strong `SECRET_KEY`
- [ ] Enable HTTPS
- [ ] Set up proper logging
- [ ] Configure CORS if needed
- [ ] Set up monitoring (Sentry, etc.)
- [ ] Configure CDN for static files

## 📈 Performance

- **Caching** - Redis for API response caching
- **Rate Limiting** - Prevent API abuse
- **Background Tasks** - Celery for heavy operations
- **Database Optimization** - Indexes and query optimization
- **CDN** - Static file delivery
- **Compression** - Gzip responses

## 🔒 Security

- CSRF protection with Flask-WTF
- SQL injection prevention with SQLAlchemy
- XSS protection with Jinja2 escaping
- Secure password hashing with Werkzeug
- Environment variable protection
- Rate limiting on API endpoints
- HTTPS enforcement in production

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

Your Name - [GitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Flask documentation
- Bootstrap team
- All API providers
- Open source community

---

⭐ **Star this repo if you find it useful!**

## 📸 Screenshots

![Dashboard](screenshots/dashboard.png)
![News Feed](screenshots/news.png)
![Weather Station](screenshots/weather.png)
![Crypto Portfolio](screenshots/crypto.png)

## 🗺️ Roadmap

- [ ] User authentication and profiles
- [ ] Data export to PDF
- [ ] Mobile app (React Native)
- [ ] Real-time chat with WebSocket
- [ ] Advanced analytics dashboard
- [ ] Integration with more APIs
- [ ] Machine learning predictions
- [ ] Multi-language support