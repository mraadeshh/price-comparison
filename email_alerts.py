import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailAlerts:
    """Handle email notifications for price alerts"""
    
    def __init__(self):
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.email_address = Config.EMAIL_ADDRESS
        self.email_password = Config.EMAIL_PASSWORD
    
    def send_price_alert(self, recipient_email, product_name, current_price, target_price, product_url):
        """Send price drop alert email"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f'🎉 Price Drop Alert: {product_name}'
            msg['From'] = self.email_address
            msg['To'] = recipient_email
            
            # Create HTML content
            html_content = f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        <h1 style="color: #28a745; text-align: center;">🎉 Price Drop Alert!</h1>
                        
                        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                            <h2 style="color: #333; margin-top: 0;">{product_name}</h2>
                            
                            <div style="margin: 15px 0;">
                                <p style="font-size: 16px; color: #666; margin: 5px 0;">
                                    <strong>Current Price:</strong> 
                                    <span style="color: #28a745; font-size: 24px; font-weight: bold;">₹{current_price:,.2f}</span>
                                </p>
                                <p style="font-size: 16px; color: #666; margin: 5px 0;">
                                    <strong>Your Target:</strong> ₹{target_price:,.2f}
                                </p>
                                <p style="font-size: 16px; color: #28a745; margin: 5px 0;">
                                    <strong>You Save:</strong> ₹{(target_price - current_price):,.2f}
                                </p>
                            </div>
                        </div>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{product_url}" 
                               style="background-color: #28a745; color: white; padding: 15px 40px; text-decoration: none; border-radius: 8px; font-size: 18px; display: inline-block;">
                                View Product Now
                            </a>
                        </div>
                        
                        <p style="color: #999; font-size: 12px; text-align: center; margin-top: 30px;">
                            This is an automated alert from Price Comparison Tool
                        </p>
                    </div>
                </body>
            </html>
            """
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
            
            logger.info(f"Price alert email sent to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def send_weekly_summary(self, recipient_email, tracked_products):
        """Send weekly summary of tracked products"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = '📊 Weekly Price Summary'
            msg['From'] = self.email_address
            msg['To'] = recipient_email
            
            # Build product list HTML
            products_html = ""
            for product in tracked_products:
                products_html += f"""
                <div style="background-color: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px;">
                    <h3 style="margin: 0 0 10px 0; color: #333;">{product['name']}</h3>
                    <p style="margin: 5px 0;">Current Price: <strong>₹{product['current_price']:,.2f}</strong></p>
                    <p style="margin: 5px 0;">Lowest This Week: <strong style="color: #28a745;">₹{product['lowest_price']:,.2f}</strong></p>
                    <a href="{product['url']}" style="color: #667eea; text-decoration: none;">View Product →</a>
                </div>
                """
            
            html_content = f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px;">
                        <h1 style="color: #667eea; text-align: center;">📊 Your Weekly Price Summary</h1>
                        <p style="text-align: center; color: #666;">Here's what happened with your tracked products this week</p>
                        
                        {products_html}
                        
                        <p style="color: #999; font-size: 12px; text-align: center; margin-top: 30px;">
                            Price Comparison Tool - Weekly Summary
                        </p>
                    </div>
                </body>
            </html>
            """
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
            
            logger.info(f"Weekly summary sent to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send weekly summary: {e}")
            return False

# Test email alerts
if __name__ == '__main__':
    alerts = EmailAlerts()
    print("Email alerts module loaded successfully!")
