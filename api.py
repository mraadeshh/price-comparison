from flask import Blueprint, request, jsonify
from functools import wraps
import time
from collections import defaultdict
from database import Database
from advanced_scraper import AdvancedScraper

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Rate limiting
request_counts = defaultdict(list)
RATE_LIMIT = 100  # requests per hour

def rate_limit(f):
    """Rate limiting decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr
        current_time = time.time()
        
        # Clean old requests
        request_counts[client_ip] = [
            req_time for req_time in request_counts[client_ip]
            if current_time - req_time < 3600
        ]
        
        # Check rate limit
        if len(request_counts[client_ip]) >= RATE_LIMIT:
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': f'Maximum {RATE_LIMIT} requests per hour'
            }), 429
        
        request_counts[client_ip].append(current_time)
        return f(*args, **kwargs)
    
    return decorated_function

db = Database()
scraper = AdvancedScraper()

@api_bp.route('/search', methods=['GET'])
@rate_limit
def api_search():
    """
    Search for products across platforms
    Query params: q (product name), platforms (comma-separated)
    """
    product_name = request.args.get('q', '')
    platforms = request.args.get('platforms', '').split(',')
    
    if not product_name:
        return jsonify({'error': 'Product name required'}), 400
    
    results = scraper.search_all_platforms(product_name)
    
    # Filter by platforms if specified
    if platforms and platforms[0]:
        results = [r for r in results if r['platform'] in platforms]
    
    return jsonify({
        'success': True,
        'count': len(results),
        'results': results
    })

@api_bp.route('/product/<int:product_id>', methods=['GET'])
@rate_limit
def api_get_product(product_id):
    """Get product details by ID"""
    history = db.get_price_history(product_id)
    
    if not history:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify({
        'success': True,
        'product_id': product_id,
        'history': history
    })

@api_bp.route('/product/<int:product_id>/history', methods=['GET'])
@rate_limit
def api_get_history(product_id):
    """Get price history for a product"""
    days = request.args.get('days', 30, type=int)
    
    history = db.get_price_history(product_id, days)
    
    return jsonify({
        'success': True,
        'product_id': product_id,
        'days': days,
        'history': history
    })

@api_bp.route('/alert', methods=['POST'])
@rate_limit
def api_create_alert():
    """
    Create price alert
    Body: {product_id, target_price, email}
    """
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
        'message': 'Alert created successfully'
    })

@api_bp.route('/compare', methods=['POST'])
@rate_limit
def api_compare():
    """
    Compare multiple products
    Body: {product_ids: [1, 2, 3]}
    """
    data = request.get_json()
    product_ids = data.get('product_ids', [])
    
    if not product_ids:
        return jsonify({'error': 'Product IDs required'}), 400
    
    comparison = []
    for product_id in product_ids:
        history = db.get_price_history(product_id, days=1)
        if history:
            comparison.append({
                'product_id': product_id,
                'current_price': history[0]['price'],
                'timestamp': history[0]['timestamp']
            })
    
    return jsonify({
        'success': True,
        'comparison': comparison
    })

@api_bp.route('/stats', methods=['GET'])
@rate_limit
def api_stats():
    """Get platform statistics"""
    stats = db.get_platform_stats()
    
    return jsonify({
        'success': True,
        'stats': stats
    })

@api_bp.route('/trending', methods=['GET'])
@rate_limit
def api_trending():
    """Get trending products (most searched)"""
    limit = request.args.get('limit', 10, type=int)
    
    trending = db.get_trending_products(limit)
    
    return jsonify({
        'success': True,
        'trending': trending
    })

# Error handlers
@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@api_bp.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500
