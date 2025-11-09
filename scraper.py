import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

class PriceScraper:
    """Web scraper for e-commerce platforms"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def search_product(self, product_name):
        """Search product across multiple platforms"""
        results = []
        
        # Amazon scraping
        amazon_result = self.scrape_amazon(product_name)
        if amazon_result:
            results.append(amazon_result)
        
        # Flipkart scraping
        flipkart_result = self.scrape_flipkart(product_name)
        if flipkart_result:
            results.append(flipkart_result)
        
        return results
    
    def scrape_amazon(self, product_name):
        """Scrape Amazon for product price"""
        try:
            # Format search URL
            search_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find first product
            product = soup.find('div', {'data-component-type': 's-search-result'})
            
            if product:
                # Extract product details
                title = product.find('h2', {'class': 'a-size-mini'})
                price = product.find('span', {'class': 'a-price-whole'})
                link = product.find('a', {'class': 'a-link-normal'})
                
                if title and price:
                    return {
                        'platform': 'Amazon',
                        'product_name': title.text.strip(),
                        'price': float(price.text.replace(',', '').replace('₹', '')),
                        'currency': 'INR',
                        'url': f"https://www.amazon.in{link['href']}" if link else '',
                        'timestamp': datetime.now().isoformat()
                    }
        
        except Exception as e:
            print(f"Amazon scraping error: {e}")
        
        return None
    
    def scrape_flipkart(self, product_name):
        """Scrape Flipkart for product price"""
        try:
            # Format search URL
            search_url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '%20')}"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find first product
            product = soup.find('div', {'class': '_1AtVbE'})
            
            if product:
                # Extract product details
                title = product.find('div', {'class': '_4rR01T'})
                price = product.find('div', {'class': '_30jeq3'})
                link = product.find('a', {'class': '_1fQZEK'})
                
                if title and price:
                    return {
                        'platform': 'Flipkart',
                        'product_name': title.text.strip(),
                        'price': float(price.text.replace(',', '').replace('₹', '')),
                        'currency': 'INR',
                        'url': f"https://www.flipkart.com{link['href']}" if link else '',
                        'timestamp': datetime.now().isoformat()
                    }
        
        except Exception as e:
            print(f"Flipkart scraping error: {e}")
        
        return None

# Test the scraper
if __name__ == '__main__':
    scraper = PriceScraper()
    results = scraper.search_product('laptop')
    print(results)
