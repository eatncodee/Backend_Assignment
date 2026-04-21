from fastapi import Request, HTTPException
import redis.asyncio as redis

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
async def login_rate_limiter(request: Request):
    client_ip = request.client.host
    redis_key = f"rate_limit:login:{client_ip}"
    
    attempts = await redis_client.incr(redis_key)
    if attempts == 1:
        await redis_client.expire(redis_key, 60) 
        
    if attempts > 5: 
        time_left = await redis_client.ttl(redis_key)
        raise HTTPException(status_code=429, detail=f"Too many login attempts. Try again in {time_left} seconds.")