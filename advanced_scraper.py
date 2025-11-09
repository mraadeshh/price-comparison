import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedScraper:
    """Enhanced web scraper supporting multiple platforms"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.timeout = Config.SCRAPE_TIMEOUT
        self.max_retries = Config.MAX_RETRIES
    
    def search_all_platforms(self, product_name):
        """Search product across all supported platforms"""
        results = []
        
        platforms = {
            'Amazon': self.scrape_amazon,
            'Flipkart': self.scrape_flipkart,
            'Myntra': self.scrape_myntra,
            'Snapdeal': self.scrape_snapdeal
        }
        
        for platform_name, scraper_func in platforms.items():
            try:
                logger.info(f"Scraping {platform_name}...")
                result = scraper_func(product_name)
                if result:
                    results.append(result)
                time.sleep(1)  # Rate limiting
            except Exception as e:
                logger.error(f"Error scraping {platform_name}: {e}")
        
        return results
    
    def scrape_amazon(self, product_name):
        """Enhanced Amazon scraper"""
        try:
            search_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
            
            for attempt in range(self.max_retries):
                try:
                    response = requests.get(search_url, headers=self.headers, timeout=self.timeout)
                    response.raise_for_status()
                    break
                except requests.RequestException as e:
                    if attempt == self.max_retries - 1:
                        raise
                    time.sleep(2)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Multiple selectors for better accuracy
            product = soup.find('div', {'data-component-type': 's-search-result'})
            
            if product:
                # Extract title
                title_elem = product.find('h2', {'class': 'a-size-mini'}) or product.find('span', {'class': 'a-text-normal'})
                
                # Extract price
                price_elem = product.find('span', {'class': 'a-price-whole'})
                
                # Extract link
                link_elem = product.find('a', {'class': 'a-link-normal'})
                
                # Extract rating
                rating_elem = product.find('span', {'class': 'a-icon-alt'})
                
                # Extract image
                image_elem = product.find('img', {'class': 's-image'})
                
                if title_elem and price_elem:
                    price_text = price_elem.text.replace(',', '').replace('₹', '').strip()
                    
                    return {
                        'platform': 'Amazon',
                        'product_name': title_elem.text.strip()[:200],
                        'price': float(price_text),
                        'currency': 'INR',
                        'url': f"https://www.amazon.in{link_elem['href']}" if link_elem else search_url,
                        'rating': rating_elem.text.split()[0] if rating_elem else 'N/A',
                        'image': image_elem['src'] if image_elem else '',
                        'timestamp': datetime.now().isoformat()
                    }
        
        except Exception as e:
            logger.error(f"Amazon scraping error: {e}")
        
        return None
    
    def scrape_flipkart(self, product_name):
        """Enhanced Flipkart scraper"""
        try:
            search_url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '%20')}"
            
            response = requests.get(search_url, headers=self.headers, timeout=self.timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try multiple selectors
            product = (soup.find('div', {'class': '_1AtVbE'}) or 
                      soup.find('div', {'class': '_2kHMtA'}) or
                      soup.find('div', {'class': '_13oc-S'}))
            
            if product:
                title_elem = (product.find('div', {'class': '_4rR01T'}) or 
                            product.find('a', {'class': 's1Q9rs'}))
                
                price_elem = (product.find('div', {'class': '_30jeq3'}) or
                            product.find('div', {'class': '_25b18c'}))
                
                link_elem = product.find('a', {'class': '_1fQZEK'}) or product.find('a')
                
                rating_elem = product.find('div', {'class': '_3LWZlK'})
                
                if title_elem and price_elem:
                    price_text = price_elem.text.replace(',', '').replace('₹', '').strip()
                    
                    return {
                        'platform': 'Flipkart',
                        'product_name': title_elem.text.strip()[:200],
                        'price': float(price_text),
                        'currency': 'INR',
                        'url': f"https://www.flipkart.com{link_elem['href']}" if link_elem else search_url,
                        'rating': rating_elem.text if rating_elem else 'N/A',
                        'image': '',
                        'timestamp': datetime.now().isoformat()
                    }
        
        except Exception as e:
            logger.error(f"Flipkart scraping error: {e}")
        
        return None
    
    def scrape_myntra(self, product_name):
        """Myntra scraper for fashion products"""
        try:
            search_url = f"https://www.myntra.com/{product_name.replace(' ', '-')}"
            
            response = requests.get(search_url, headers=self.headers, timeout=self.timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Myntra uses dynamic loading, this is a basic implementation
            product = soup.find('li', {'class': 'product-base'})
            
            if product:
                title_elem = product.find('h4', {'class': 'product-product'})
                price_elem = product.find('span', {'class': 'product-discountedPrice'})
                link_elem = product.find('a')
                
                if title_elem and price_elem:
                    price_text = price_elem.text.replace(',', '').replace('Rs.', '').strip()
                    
                    return {
                        'platform': 'Myntra',
                        'product_name': title_elem.text.strip()[:200],
                        'price': float(price_text),
                        'currency': 'INR',
                        'url': f"https://www.myntra.com{link_elem['href']}" if link_elem else search_url,
                        'rating': 'N/A',
                        'image': '',
                        'timestamp': datetime.now().isoformat()
                    }
        
        except Exception as e:
            logger.error(f"Myntra scraping error: {e}")
        
        return None
    
    def scrape_snapdeal(self, product_name):
        """Snapdeal scraper"""
        try:
            search_url = f"https://www.snapdeal.com/search?keyword={product_name.replace(' ', '%20')}"
            
            response = requests.get(search_url, headers=self.headers, timeout=self.timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            product = soup.find('div', {'class': 'product-tuple-listing'})
            
            if product:
                title_elem = product.find('p', {'class': 'product-title'})
                price_elem = product.find('span', {'class': 'lfloat product-price'})
                link_elem = product.find('a', {'class': 'dp-widget-link'})
                
                if title_elem and price_elem:
                    price_text = price_elem.text.replace(',', '').replace('Rs.', '').strip()
                    
                    return {
                        'platform': 'Snapdeal',
                        'product_name': title_elem.text.strip()[:200],
                        'price': float(price_text),
                        'currency': 'INR',
                        'url': link_elem['href'] if link_elem else search_url,
                        'rating': 'N/A',
                        'image': '',
                        'timestamp': datetime.now().isoformat()
                    }
        
        except Exception as e:
            logger.error(f"Snapdeal scraping error: {e}")
        
        return None

# Test scraper
if __name__ == '__main__':
    scraper = AdvancedScraper()
    results = scraper.search_all_platforms('laptop')
    print(f"Found {len(results)} results")
    for result in results:
        print(f"{result['platform']}: ₹{result['price']}")
