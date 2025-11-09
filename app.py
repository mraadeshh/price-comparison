from flask import Flask, render_template, request, jsonify
from scraper import PriceScraper
from database import Database
import json

app = Flask(__name__)
db = Database()
scraper = PriceScraper()

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Search for product prices across platforms"""
    try:
        data = request.get_json()
        product_name = data.get('product_name', '')
        
        if not product_name:
            return jsonify({'error': 'Product name is required'}), 400
        
        # Scrape prices from different platforms
        results = scraper.search_product(product_name)
        
        # Save to database
        for result in results:
            db.save_price(result)
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history/<product_id>')
def get_history(product_id):
    """Get price history for a product"""
    try:
        history = db.get_price_history(product_id)
        return jsonify({
            'success': True,
            'history': history
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/alert', methods=['POST'])
def set_alert():
    """Set price alert for a product"""
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        target_price = data.get('target_price')
        
        db.set_alert(product_id, target_price)
        
        return jsonify({
            'success': True,
            'message': 'Alert set successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    db.init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
