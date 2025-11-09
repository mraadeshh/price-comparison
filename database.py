import sqlite3
from datetime import datetime
import json

class Database:
    """Database handler for price tracking"""
    
    def __init__(self, db_name='prices.db'):
        self.db_name = db_name
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                platform TEXT NOT NULL,
                url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Price history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                price REAL NOT NULL,
                currency TEXT DEFAULT 'INR',
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                target_price REAL NOT NULL,
                active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_price(self, product_data):
        """Save product price to database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Check if product exists
        cursor.execute('''
            SELECT id FROM products 
            WHERE name = ? AND platform = ?
        ''', (product_data['product_name'], product_data['platform']))
        
        result = cursor.fetchone()
        
        if result:
            product_id = result[0]
        else:
            # Insert new product
            cursor.execute('''
                INSERT INTO products (name, platform, url)
                VALUES (?, ?, ?)
            ''', (product_data['product_name'], product_data['platform'], product_data['url']))
            product_id = cursor.lastrowid
        
        # Insert price history
        cursor.execute('''
            INSERT INTO price_history (product_id, price, currency)
            VALUES (?, ?, ?)
        ''', (product_id, product_data['price'], product_data['currency']))
        
        conn.commit()
        conn.close()
        
        return product_id
    
    def get_price_history(self, product_id):
        """Get price history for a product"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT price, timestamp 
            FROM price_history 
            WHERE product_id = ?
            ORDER BY timestamp DESC
            LIMIT 30
        ''', (product_id,))
        
        history = [{'price': row[0], 'timestamp': row[1]} for row in cursor.fetchall()]
        
        conn.close()
        return history
    
    def set_alert(self, product_id, target_price):
        """Set price alert for a product"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alerts (product_id, target_price)
            VALUES (?, ?)
        ''', (product_id, target_price))
        
        conn.commit()
        conn.close()
    
    def check_alerts(self):
        """Check if any alerts should be triggered"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.id, p.name, a.target_price, ph.price
            FROM alerts a
            JOIN products p ON a.product_id = p.id
            JOIN price_history ph ON p.id = ph.product_id
            WHERE a.active = 1
            AND ph.price <= a.target_price
            AND ph.id = (
                SELECT MAX(id) FROM price_history WHERE product_id = p.id
            )
        ''')
        
        triggered_alerts = cursor.fetchall()
        conn.close()
        
        return triggered_alerts

# Test database
if __name__ == '__main__':
    db = Database()
    db.init_db()
    print("Database initialized successfully!")
