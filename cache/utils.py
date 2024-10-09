import json

from cache.redis_fc import redis_fc


def cache_get_follower(account):
    """
    Fetch and cache follower data for a given FID (if not already cached).
    """
    cached_followers = redis_fc.get("followers")
    if not cached_followers: return ""
    json_cache = json.loads(cached_followers)

    if json_cache.get(account, ""):
        return json_cache.get(account)

    return ""

def cache_get_all_followers():
    """
    Fetch and cache follower data for a given FID (if not already cached).
    """
    cached_followers = redis_fc.get("followers")
    if not cached_followers: return ""
    json_cache = json.loads(cached_followers)
    
    if json_cache:
        return json.loads(cached_followers)

    return ""