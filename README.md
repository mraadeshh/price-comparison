# 🛒 Price Comparison Tool

Smart price comparison and tracking tool that monitors product prices across multiple e-commerce platforms.

## ✨ Features

- 🔍 **Multi-Platform Search** - Compare prices across Amazon, Flipkart, and more
- 📊 **Price History** - Track price changes over time with visual graphs
- 🔔 **Price Alerts** - Get notified when prices drop
- 💾 **Database Storage** - Historical price data for analysis
- 🌐 **Web Interface** - Easy-to-use web dashboard

## 🚀 Tech Stack

- **Backend:** Python, Flask
- **Scraping:** BeautifulSoup4, Requests
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Visualization:** Chart.js

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/mraadeshh/price-comparison.git
cd price-comparison
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open browser and visit: `http://localhost:5000`

## 📁 Project Structure

```
price-comparison/
├── app.py                 # Main Flask application
├── scraper.py            # Web scraping logic
├── database.py           # Database operations
├── requirements.txt      # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css    # Styling
│   └── js/
│       └── main.js      # Frontend logic
├── templates/
│   └── index.html       # Main page
└── README.md
```

## 🎯 Usage

1. Enter product name or URL in the search box
2. View prices from different platforms
3. Track price history with graphs
4. Set price alerts for your desired products

## 🔧 Configuration

Edit `config.py` to customize:
- Supported e-commerce platforms
- Scraping intervals
- Alert thresholds

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📝 License

MIT License - feel free to use this project for learning and development.

## 👨‍💻 Author

**Ansh Roy** - [GitHub](https://github.com/mraadeshh)

---

⭐ Star this repo if you find it helpful!
