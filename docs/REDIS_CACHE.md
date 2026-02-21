# Redis Cache Layer (OPTIONAL)

## When to Add Redis?
- API response time > 1 second
- Supabase rate limit issues
- High traffic (1000+ req/min)

## Setup (Upstash Redis - Free)

### 1. Create Upstash Account
1. Go to https://upstash.com
2. Sign up (free)
3. Create Redis database
4. Copy: `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN`

### 2. Add to .env
```env
REDIS_URL=https://xxxxx.upstash.io
REDIS_TOKEN=your_token_here
```

### 3. Install Package
```bash
pip install redis
```

### 4. Use Cache
```python
from core.redis_cache import RedisCache

cache = RedisCache()

# Cache ticker analysis (5 min TTL)
result = cache.get(f"ticker:{ticker}")
if not result:
    result = analyze_ticker(ticker)
    cache.set(f"ticker:{ticker}", result, ttl=300)
```

## Current Performance (WITHOUT Redis)
- Supabase query: ~50-100ms ✅
- API response: ~200-500ms ✅
- Real-time Telegram: <2 min ✅

## Conclusion
**You DON'T need Redis now.** Your setup is already fast.

Add Redis later if you see performance issues.
