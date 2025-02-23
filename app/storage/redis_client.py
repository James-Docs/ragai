import redis
import json
from typing import Any, Optional
from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB

class RedisClient:
    def __init__(self):
        self.redis = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB
        )
    
    def set_cache(self, key: str, value: Any, expire: int = 3600):
        """Set cache with expiration time."""
        self.redis.setex(
            key,
            expire,
            json.dumps(value)
        )
    
    def get_cache(self, key: str) -> Optional[Any]:
        """Get cached value."""
        value = self.redis.get(key)
        return json.loads(value) if value else None 