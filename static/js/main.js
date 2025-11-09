document.addEventListener('DOMContentLoaded', function() {
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchInput');
    const loading = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    
    searchBtn.addEventListener('click', searchProducts);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchProducts();
        }
    });
    
    async function searchProducts() {
        const productName = searchInput.value.trim();
        
        if (!productName) {
            alert('Please enter a product name');
            return;
        }
        
        // Show loading
        loading.style.display = 'block';
        resultsDiv.innerHTML = '';
        
        try {
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ product_name: productName })
            });
            
            const data = await response.json();
            
            if (data.success) {
                displayResults(data.results);
            } else {
                resultsDiv.innerHTML = '<p>No results found. Try a different search term.</p>';
            }
        } catch (error) {
            console.error('Error:', error);
            resultsDiv.innerHTML = '<p>Error fetching prices. Please try again.</p>';
        } finally {
            loading.style.display = 'none';
        }
    }
    
    function displayResults(results) {
        if (results.length === 0) {
            resultsDiv.innerHTML = '<p>No products found. Try a different search.</p>';
            return;
        }
        
        resultsDiv.innerHTML = '';
        
        results.forEach(product => {
            const card = document.createElement('div');
            card.className = 'product-card';
            
            card.innerHTML = `
                <div class="platform-badge">${product.platform}</div>
                <div class="product-name">${product.product_name}</div>
                <div class="price">₹${product.price.toLocaleString()}</div>
                <a href="${product.url}" target="_blank" class="product-link">View Product</a>
            `;
            
            resultsDiv.appendChild(card);
        });
        
        // Find lowest price
        const lowestPrice = Math.min(...results.map(p => p.price));
        const cards = resultsDiv.querySelectorAll('.product-card');
        
        cards.forEach((card, index) => {
            if (results[index].price === lowestPrice) {
                card.style.border = '3px solid #28a745';
                const badge = document.createElement('div');
                badge.style.cssText = 'background: #28a745; color: white; padding: 5px 10px; border-radius: 5px; margin-top: 10px; text-align: center;';
                badge.textContent = '🏆 Best Price';
                card.appendChild(badge);
            }
        });
    }
});
