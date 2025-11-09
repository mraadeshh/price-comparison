from flask import Flask, render_template, request, jsonify
from advanced_scraper import AdvancedScraper
from database import Database
from price_analyzer import PriceAnalyzer
from email_alerts import EmailAlerts
from api import api_bp
from config import Config
import json

app = Flask(__name__)
app.config.from_object(Config)

# Register API blueprint
app.register_blueprint(api_bp)

# Initialize components
db = Database()
scraper = AdvancedScraper()
analyzer = PriceAnalyzer()
email_alerts = EmailAlerts()

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
        
        # Scrape prices from all platforms
        results = scraper.search_all_platforms(product_name)
        
        # Save to database
        for result in results:
            db.save_price(result)
        
        # Add analysis
        if results:
            best_deal = min(results, key=lambda x: x['price'])
            worst_deal = max(results, key=lambda x: x['price'])
            savings = worst_deal['price'] - best_deal['price']
            
            return jsonify({
                'success': True,
                'results': results,
                'analysis': {
                    'best_platform': best_deal['platform'],
                    'best_price': best_deal['price'],
                    'potential_savings': round(savings, 2),
                    'total_platforms': len(results)
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No results found. Try a different search term.'
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history/<int:product_id>')
def get_history(product_id):
    """Get price history for a product"""
    try:
        days = request.args.get('days', 30, type=int)
        history = db.get_price_history(product_id, days)
        
        # Get trend analysis
        trend = analyzer.get_price_trend(product_id, days)
        
        # Get buying recommendation
        recommendation = analyzer.predict_best_time_to_buy(product_id)
        
        return jsonify({
            'success': True,
            'history': history,
            'trend': trend,
            'recommendation': recommendation
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
        email = data.get('email')
        
        if not all([product_id, target_price, email]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        alert_id = db.set_alert(product_id, target_price, email)
        
        return jsonify({
            'success': True,
            'alert_id': alert_id,
            'message': 'Alert set successfully! You will be notified when price drops.'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze/<int:product_id>')
def analyze_product(product_id):
    """Get detailed analysis for a product"""
    try:
        # Get trend analysis
        trend = analyzer.get_price_trend(product_id)
        
        # Get buying recommendation
        recommendation = analyzer.predict_best_time_to_buy(product_id)
        
        # Calculate savings
        savings = analyzer.calculate_savings(product_id)
        
        # Generate chart
        chart_html = analyzer.generate_price_chart(product_id)
        
        return jsonify({
            'success': True,
            'trend': trend,
            'recommendation': recommendation,
            'savings': savings,
            'chart': chart_html
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/compare', methods=['POST'])
def compare_products():
    """Compare prices across platforms"""
    try:
        data = request.get_json()
        product_name = data.get('product_name', '')
        
        comparison = analyzer.compare_platforms(product_name)
        
        return jsonify({
            'success': True,
            'comparison': comparison
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/trending')
def get_trending():
    """Get trending products"""
    try:
        limit = request.args.get('limit', 10, type=int)
        trending = db.get_trending_products(limit)
        
        return jsonify({
            'success': True,
            'trending': trending
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0',
        'features': [
            'multi-platform-search',
            'price-history',
            'email-alerts',
            'price-analysis',
            'api-access'
        ]
    })

if __name__ == '__main__':
    db.init_db()
    print("🚀 Price Comparison Tool v2.0")
    print("📊 Features: Multi-platform search, Price alerts, Analysis, API")
    print("🌐 Server running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
