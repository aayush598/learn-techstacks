# API Security for Recommendation Systems

## 1. Rate Limiting

### 1.1 Rate Limiting Algorithms
- **Token Bucket**: Allow bursts up to bucket capacity; refill at fixed rate
- **Sliding Window**: Count requests in rolling time window
- **Fixed Window**: Count requests in fixed time window
- **Leaky Bucket**: Process requests at fixed rate; reject when queue full

### 1.2 Rate Limit Dimensions
- **Per User**: 100 requests/minute per user
- **Per API Key**: 1000 requests/minute per API key
- **Per Endpoint**: Different limits per endpoint
- **Global**: Total system throughput limit

### 1.3 Implementation
- Rate limiting at API gateway (Kong, Traefik)
- Distributed rate limiting with Redis (sliding window counter)
- Rate limit headers in responses (X-RateLimit-Limit, X-RateLimit-Remaining)

---

## 2. Input Validation

### 2.1 Request Validation
- **Schema Validation**: Validate request body against JSON schema
- **Type Checking**: Ensure correct data types
- **Range Validation**: Ensure values within expected ranges
- **Length Limits**: Limit string and array lengths
- **Enum Validation**: Restrict to allowed values

### 2.2 Sanitization
- **SQL Injection Prevention**: Use parameterized queries
- **XSS Prevention**: Escape output, Content-Security-Policy headers
- **Command Injection Prevention**: Never pass user input to shell commands
- **Path Traversal Prevention**: Validate file paths

### 2.3 Recommendation-Specific Validation
- **User ID Format**: Validate UUID/string format
- **Item ID Format**: Validate against catalog
- **Context Parameters**: Validate device, platform, location
- **Filter Parameters**: Validate filter values against allowed lists

---

## 3. CORS Configuration

### 3.1 CORS for Recommendation APIs
```yaml
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Authorization, Content-Type, X-API-Key
Access-Control-Max-Age: 86400
Access-Control-Allow-Credentials: true
```

### 3.2 CORS Best Practices
- Never use `Access-Control-Allow-Origin: *` with credentials
- Whitelist specific origins
- Limit allowed methods to what's needed
- Use preflight caching (Access-Control-Max-Age)

---

## 4. Additional Security Measures

### 4.1 Content Security Policy
- Restrict resource loading to trusted sources
- Prevent XSS attacks
- Block inline scripts

### 4.2 Request Size Limits
- Limit request body size (e.g., 1MB)
- Limit URL length (e.g., 2048 characters)
- Limit number of parameters
- Prevent resource exhaustion attacks

### 4.3 Timeout Configuration
- Request processing timeout (e.g., 30 seconds)
- Connection timeout (e.g., 5 seconds)
- Idle connection timeout (e.g., 60 seconds)
- Prevent slow loris attacks

### 4.4 Logging and Monitoring
- Log all authentication failures
- Log rate limit hits
- Log suspicious input patterns
- Alert on unusual traffic patterns
- Monitor for credential stuffing attacks
