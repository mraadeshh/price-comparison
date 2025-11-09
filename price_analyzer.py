import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from database import Database
import statistics

class PriceAnalyzer:
    """Analyze price trends and generate insights"""
    
    def __init__(self):
        self.db = Database()
    
    def get_price_trend(self, product_id, days=30):
        """Analyze price trend over time"""
        history = self.db.get_price_history(product_id, days)
        
        if len(history) < 2:
            return {'trend': 'insufficient_data'}
        
        prices = [h['price'] for h in history]
        
        # Calculate trend
        first_price = prices[-1]
        last_price = prices[0]
        change_percent = ((last_price - first_price) / first_price) * 100
        
        # Determine trend direction
        if change_percent > 5:
            trend = 'increasing'
        elif change_percent < -5:
            trend = 'decreasing'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'change_percent': round(change_percent, 2),
            'lowest_price': min(prices),
            'highest_price': max(prices),
            'average_price': round(statistics.mean(prices), 2),
            'current_price': last_price,
            'volatility': round(statistics.stdev(prices), 2) if len(prices) > 1 else 0
        }
    
    def predict_best_time_to_buy(self, product_id):
        """Predict best time to buy based on historical data"""
        history = self.db.get_price_history(product_id, days=90)
        
        if len(history) < 7:
            return {'recommendation': 'Need more data'}
        
        prices = [h['price'] for h in history]
        current_price = prices[0]
        avg_price = statistics.mean(prices)
        min_price = min(prices)
        
        # Calculate price position
        price_position = (current_price - min_price) / (max(prices) - min_price) * 100
        
        if current_price <= min_price * 1.05:
            recommendation = 'buy_now'
            reason = 'Price is at or near historical low'
        elif current_price <= avg_price * 0.95:
            recommendation = 'good_time'
            reason = 'Price is below average'
        elif current_price >= avg_price * 1.1:
            recommendation = 'wait'
            reason = 'Price is above average, consider waiting'
        else:
            recommendation = 'neutral'
            reason = 'Price is around average'
        
        return {
            'recommendation': recommendation,
            'reason': reason,
            'current_price': current_price,
            'average_price': round(avg_price, 2),
            'lowest_price': min_price,
            'price_position': round(price_position, 2),
            'confidence': 'high' if len(history) > 30 else 'medium'
        }
    
    def compare_platforms(self, product_name):
        """Compare prices across platforms for same product"""
        results = self.db.get_latest_prices_by_product(product_name)
        
        if not results:
            return {'error': 'No data found'}
        
        comparison = []
        for result in results:
            comparison.append({
                'platform': result['platform'],
                'price': result['price'],
                'url': result['url'],
                'last_updated': result['timestamp']
            })
        
        # Find best deal
        best_deal = min(comparison, key=lambda x: x['price'])
        worst_deal = max(comparison, key=lambda x: x['price'])
        
        savings = worst_deal['price'] - best_deal['price']
        savings_percent = (savings / worst_deal['price']) * 100
        
        return {
            'comparison': comparison,
            'best_deal': best_deal,
            'potential_savings': round(savings, 2),
            'savings_percent': round(savings_percent, 2)
        }
    
    def generate_price_chart(self, product_id, days=30):
        """Generate interactive price chart"""
        history = self.db.get_price_history(product_id, days)
        
        if not history:
            return None
        
        # Prepare data
        dates = [h['timestamp'] for h in reversed(history)]
        prices = [h['price'] for h in reversed(history)]
        
        # Create figure
        fig = go.Figure()
        
        # Add price line
        fig.add_trace(go.Scatter(
            x=dates,
            y=prices,
            mode='lines+markers',
            name='Price',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8)
        ))
        
        # Add average line
        avg_price = statistics.mean(prices)
        fig.add_hline(
            y=avg_price,
            line_dash="dash",
            line_color="orange",
            annotation_text=f"Average: ₹{avg_price:.2f}"
        )
        
        # Update layout
        fig.update_layout(
            title='Price History',
            xaxis_title='Date',
            yaxis_title='Price (₹)',
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        
        return fig.to_html(full_html=False)
    
    def get_price_alerts_summary(self, user_email):
        """Get summary of user's price alerts"""
        alerts = self.db.get_user_alerts(user_email)
        
        active_alerts = [a for a in alerts if a['active']]
        triggered_alerts = [a for a in alerts if not a['active']]
        
        return {
            'total_alerts': len(alerts),
            'active_alerts': len(active_alerts),
            'triggered_alerts': len(triggered_alerts),
            'alerts': alerts
        }
    
    def calculate_savings(self, product_id):
        """Calculate potential savings over time"""
        history = self.db.get_price_history(product_id, days=90)
        
        if len(history) < 2:
            return {'savings': 0}
        
        prices = [h['price'] for h in history]
        current_price = prices[0]
        max_price = max(prices)
        
        savings = max_price - current_price
        savings_percent = (savings / max_price) * 100
        
        return {
            'current_price': current_price,
            'highest_price': max_price,
            'savings': round(savings, 2),
            'savings_percent': round(savings_percent, 2)
        }

# Test analyzer
if __name__ == '__main__':
    analyzer = PriceAnalyzer()
    print("Price analyzer loaded successfully!")
