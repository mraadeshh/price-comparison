# 📚 API Documentation

## Base URL
```
http://localhost:5000/api/v1
```

## Rate Limiting
- **Limit:** 100 requests per hour per IP
- **Response:** 429 Too Many Requests when exceeded

---

## Endpoints

### 1. Search Products
Search for products across multiple platforms.

**Endpoint:** `GET /api/v1/search`

**Query Parameters:**
- `q` (required): Product name to search
- `platforms` (optional): Comma-separated platform names (Amazon,Flipkart,Myntra,Snapdeal)

**Example:**
```bash
curl "http://localhost:5000/api/v1/search?q=laptop&platforms=Amazon,Flipkart"
```

**Response:**
```json
{
  "success": true,
  "count": 2,
  "results": [
    {
      "platform": "Amazon",
      "product_name": "Dell Laptop",
      "price": 45990,
      "currency": "INR",
      "url": "https://amazon.in/...",
      "rating": "4.5",
      "timestamp": "2025-11-09T10:00:00"
    }
  ]
}
```

---

### 2. Get Product Details
Get details and history for a specific product.

**Endpoint:** `GET /api/v1/product/{product_id}`

**Example:**
```bash
curl "http://localhost:5000/api/v1/product/123"
```

**Response:**
```json
{
  "success": true,
  "product_id": 123,
  "history": [
    {
      "price": 45990,
      "timestamp": "2025-11-09T10:00:00"
    }
  ]
}
```

---

### 3. Get Price History
Get price history for a product over specified days.

**Endpoint:** `GET /api/v1/product/{product_id}/history`

**Query Parameters:**
- `days` (optional): Number of days (default: 30)

**Example:**
```bash
curl "http://localhost:5000/api/v1/product/123/history?days=60"
```

---

### 4. Create Price Alert
Set up email alert when price drops below target.

**Endpoint:** `POST /api/v1/alert`

**Body:**
```json
{
  "product_id": 123,
  "target_price": 40000,
  "email": "user@example.com"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/v1/alert \
  -H "Content-Type: application/json" \
  -d '{"product_id":123,"target_price":40000,"email":"user@example.com"}'
```

**Response:**
```json
{
  "success": true,
  "alert_id": 456,
  "message": "Alert created successfully"
}
```

---

### 5. Compare Products
Compare multiple products by their IDs.

**Endpoint:** `POST /api/v1/compare`

**Body:**
```json
{
  "product_ids": [123, 456, 789]
}
```

**Response:**
```json
{
  "success": true,
  "comparison": [
    {
      "product_id": 123,
      "current_price": 45990,
      "timestamp": "2025-11-09T10:00:00"
    }
  ]
}
```

---

### 6. Get Platform Statistics
Get statistics about tracked platforms.

**Endpoint:** `GET /api/v1/stats`

**Example:**
```bash
curl "http://localhost:5000/api/v1/stats"
```

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_products": 1500,
    "total_price_points": 45000,
    "platforms": {
      "Amazon": 600,
      "Flipkart": 550,
      "Myntra": 200,
      "Snapdeal": 150
    }
  }
}
```

---

### 7. Get Trending Products
Get most searched/tracked products.

**Endpoint:** `GET /api/v1/trending`

**Query Parameters:**
- `limit` (optional): Number of results (default: 10)

**Example:**
```bash
curl "http://localhost:5000/api/v1/trending?limit=5"
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Product name required"
}
```

### 404 Not Found
```json
{
  "error": "Product not found"
}
```

### 429 Too Many Requests
```json
{
  "error": "Rate limit exceeded",
  "message": "Maximum 100 requests per hour"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Authentication
Currently, the API is open and doesn't require authentication. Rate limiting is applied per IP address.

## Best Practices
1. Cache responses when possible
2. Respect rate limits
3. Use specific platform filters to reduce response size
4. Handle errors gracefully
5. Use pagination for large datasets

## Support
For issues or questions, open an issue on GitHub.
