# 🛒 Price Comparison Tool v2.0

**Smart price comparison and tracking tool** that monitors product prices across multiple e-commerce platforms with AI-powered analysis and automated alerts.

[![GitHub stars](https://img.shields.io/github/stars/mraadeshh/price-comparison?style=social)](https://github.com/mraadeshh/price-comparison)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

### 🔍 **Multi-Platform Search**
- Compare prices across **Amazon, Flipkart, Myntra, and Snapdeal**
- Real-time price extraction with retry logic
- Automatic best deal identification

### 📊 **Price Analytics**
- **Price history tracking** with interactive charts
- **Trend analysis** (increasing/decreasing/stable)
- **Best time to buy** predictions
- Volatility and savings calculations

### 🔔 **Smart Alerts**
- **Email notifications** when prices drop
- Customizable target prices
- Weekly price summaries
- Automated alert checking

### 🤖 **Background Automation**
- Scheduled price updates every 6 hours
- Automatic alert monitoring
- Weekly summary emails
- Old data cleanup

### 🌐 **REST API**
- Full API access with rate limiting
- Search, compare, and track products
- Comprehensive documentation
- 100 requests/hour per IP

### 📈 **Advanced Analysis**
- Price trend predictions
- Platform comparison
- Savings calculator
- Interactive Plotly charts

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/mraadeshh/price-comparison.git
cd price-comparison
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your settings (email credentials, etc.)
```

5. **Run the application:**
```bash
python app.py
```

6. **Open browser:**
```
http://localhost:5000
```

---

## 📁 Project Structure

```
price-comparison/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── scraper.py               # Basic web scraper
├── advanced_scraper.py      # Multi-platform scraper
├── database.py              # Database operations
├── price_analyzer.py        # Price analysis & predictions
├── email_alerts.py          # Email notification system
├── scheduler.py             # Background task scheduler
├── api.py                   # REST API endpoints
├── requirements.txt         # Python dependencies
├── API_DOCUMENTATION.md     # API docs
├── static/
│   ├── css/
│   │   └── style.css       # Modern UI styling
│   └── js/
│       └── main.js         # Frontend logic
├── templates/
│   └── index.html          # Main web interface
└── README.md
```

---

## 🎯 Usage

### Web Interface

1. **Search Products:**
   - Enter product name in search box
   - View prices from all platforms
   - Best deal highlighted automatically

2. **Set Price Alerts:**
   - Click on product
   - Set target price
   - Enter email for notifications

3. **View Analytics:**
   - Check price history charts
   - See trend analysis
   - Get buying recommendations

### API Usage

**Search Products:**
```bash
curl "http://localhost:5000/api/v1/search?q=laptop"
```

**Set Price Alert:**
```bash
curl -X POST http://localhost:5000/api/v1/alert \
  -H "Content-Type: application/json" \
  -d '{"product_id":123,"target_price":40000,"email":"you@email.com"}'
```

**Get Price History:**
```bash
curl "http://localhost:5000/api/v1/product/123/history?days=30"
```

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference.

---

## ⚙️ Configuration

Edit `.env` file:

```env
# Email for alerts
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Flask settings
SECRET_KEY=your-secret-key
DEBUG=True

# Scraping settings
SCRAPE_TIMEOUT=10
MAX_RETRIES=3
```

### Gmail Setup for Alerts

1. Enable 2-factor authentication
2. Generate app password: [Google Account Settings](https://myaccount.google.com/apppasswords)
3. Use app password in `.env`

---

## 🤖 Background Scheduler

Run automated tasks:

```bash
python scheduler.py
```

**Scheduled Tasks:**
- ✅ Check price alerts every hour
- ✅ Update tracked products every 6 hours
- ✅ Send weekly summaries (Mondays 9 AM)
- ✅ Cleanup old data (Sundays 2 AM)

---

## 🔧 Advanced Features

### Price Analysis
```python
from price_analyzer import PriceAnalyzer

analyzer = PriceAnalyzer()

# Get trend analysis
trend = analyzer.get_price_trend(product_id=123, days=30)

# Get buying recommendation
recommendation = analyzer.predict_best_time_to_buy(product_id=123)

# Compare platforms
comparison = analyzer.compare_platforms("laptop")
```

### Custom Scraping
```python
from advanced_scraper import AdvancedScraper

scraper = AdvancedScraper()
results = scraper.search_all_platforms("smartphone")
```

---

## 📊 Supported Platforms

| Platform | Status | Features |
|----------|--------|----------|
| Amazon | ✅ Active | Price, Rating, Image |
| Flipkart | ✅ Active | Price, Rating |
| Myntra | ✅ Active | Price (Fashion) |
| Snapdeal | ✅ Active | Price |

---

## 🛠️ Tech Stack

- **Backend:** Python 3.8+, Flask
- **Scraping:** BeautifulSoup4, Requests, Selenium
- **Database:** SQLite (easily upgradable to PostgreSQL)
- **Analysis:** Pandas, Plotly
- **Scheduling:** Schedule library
- **Frontend:** HTML5, CSS3, JavaScript
- **Charts:** Chart.js, Plotly

---

## 🚧 Roadmap

- [ ] Add more platforms (eBay, Walmart)
- [ ] Mobile app (React Native)
- [ ] User authentication system
- [ ] Chrome extension
- [ ] Price prediction ML model
- [ ] Social sharing features
- [ ] Wishlist management
- [ ] Browser notifications

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🐛 Known Issues

- Some platforms may block scraping (use VPN/proxies)
- Dynamic content requires Selenium (slower)
- Rate limiting on frequent requests

---

## 💡 Tips

1. **For better scraping:** Use residential proxies
2. **For production:** Switch to PostgreSQL
3. **For scaling:** Deploy with Gunicorn + Nginx
4. **For monitoring:** Add Sentry error tracking

---

## 📧 Contact

**Ansh Roy**
- GitHub: [@mraadeshh](https://github.com/mraadeshh)
- Email: anshroykings@gmail.com

---

## 🙏 Acknowledgments

- BeautifulSoup4 for web scraping
- Flask for web framework
- Plotly for interactive charts
- All contributors and users

---

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

**Built with ❤️ by Ansh Roy**
