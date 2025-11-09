import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # Database settings
    DATABASE_NAME = 'prices.db'
    
    # Email settings for alerts
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    
    # Scraping settings
    SCRAPE_TIMEOUT = 10
    MAX_RETRIES = 3
    
    # Supported platforms
    PLATFORMS = ['Amazon', 'Flipkart', 'Myntra', 'Snapdeal']
    
    # Price alert settings
    ALERT_CHECK_INTERVAL = 3600  # Check every hour
    PRICE_DROP_THRESHOLD = 5  # Alert if price drops by 5% or more
    
    # API settings
    API_RATE_LIMIT = 100  # requests per hour
