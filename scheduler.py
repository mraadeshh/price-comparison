import schedule
import time
from database import Database
from advanced_scraper import AdvancedScraper
from email_alerts import EmailAlerts
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PriceScheduler:
    """Background scheduler for automated price checking"""
    
    def __init__(self):
        self.db = Database()
        self.scraper = AdvancedScraper()
        self.email_alerts = EmailAlerts()
    
    def check_price_alerts(self):
        """Check all active alerts and send notifications"""
        logger.info("Checking price alerts...")
        
        try:
            triggered_alerts = self.db.check_alerts()
            
            for alert in triggered_alerts:
                alert_id, product_name, target_price, current_price, email, url = alert
                
                # Send email notification
                self.email_alerts.send_price_alert(
                    recipient_email=email,
                    product_name=product_name,
                    current_price=current_price,
                    target_price=target_price,
                    product_url=url
                )
                
                # Mark alert as triggered
                self.db.deactivate_alert(alert_id)
                
                logger.info(f"Alert triggered for {product_name}: ₹{current_price}")
        
        except Exception as e:
            logger.error(f"Error checking alerts: {e}")
    
    def update_tracked_products(self):
        """Update prices for all tracked products"""
        logger.info("Updating tracked product prices...")
        
        try:
            tracked_products = self.db.get_all_tracked_products()
            
            for product in tracked_products:
                product_id, product_name, platform = product
                
                # Scrape latest price
                if platform == 'Amazon':
                    result = self.scraper.scrape_amazon(product_name)
                elif platform == 'Flipkart':
                    result = self.scraper.scrape_flipkart(product_name)
                elif platform == 'Myntra':
                    result = self.scraper.scrape_myntra(product_name)
                elif platform == 'Snapdeal':
                    result = self.scraper.scrape_snapdeal(product_name)
                else:
                    continue
                
                if result:
                    self.db.save_price(result)
                    logger.info(f"Updated {product_name} on {platform}: ₹{result['price']}")
                
                time.sleep(2)  # Rate limiting
        
        except Exception as e:
            logger.error(f"Error updating products: {e}")
    
    def send_weekly_summaries(self):
        """Send weekly price summaries to users"""
        logger.info("Sending weekly summaries...")
        
        try:
            users = self.db.get_all_users_with_alerts()
            
            for user_email in users:
                tracked_products = self.db.get_user_tracked_products(user_email)
                
                if tracked_products:
                    self.email_alerts.send_weekly_summary(
                        recipient_email=user_email,
                        tracked_products=tracked_products
                    )
                    logger.info(f"Weekly summary sent to {user_email}")
        
        except Exception as e:
            logger.error(f"Error sending summaries: {e}")
    
    def cleanup_old_data(self):
        """Clean up old price history data"""
        logger.info("Cleaning up old data...")
        
        try:
            deleted_count = self.db.cleanup_old_prices(days=90)
            logger.info(f"Deleted {deleted_count} old price records")
        
        except Exception as e:
            logger.error(f"Error cleaning up data: {e}")
    
    def start(self):
        """Start the scheduler"""
        logger.info("Starting price scheduler...")
        
        # Schedule tasks
        schedule.every(1).hours.do(self.check_price_alerts)
        schedule.every(6).hours.do(self.update_tracked_products)
        schedule.every().monday.at("09:00").do(self.send_weekly_summaries)
        schedule.every().sunday.at("02:00").do(self.cleanup_old_data)
        
        logger.info("Scheduler started successfully!")
        
        # Run scheduler
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

if __name__ == '__main__':
    scheduler = PriceScheduler()
    scheduler.start()
