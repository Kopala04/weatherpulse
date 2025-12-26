import time
from typing import Any

_cache: dict[str, tuple[float, Any]] = {}

def cache_get(key: str) -> Any | None:
    entry = _cache.get(key)
    if not entry:
        return None

    expires_at, value = entry
    if time.time() > expires_at:
        del _cache[key]
        return None
    return value

def cache_set(key: str, value: Any, ttl_seconds: int = 600) -> None:
    _cache[key] = (time.time() + ttl_seconds, value)
