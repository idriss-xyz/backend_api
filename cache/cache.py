from flask_caching import Cache

# cache = Cache(config={"CACHE_TYPE": "simple"})
twitter_cache = Cache(config={"CACHE_TYPE": "simple", "CACHE_DEFAULT_TIMEOUT": 3600})
twitter_name_cache = Cache(
    config={"CACHE_TYPE": "simple", "CACHE_DEFAULT_TIMEOUT": 3600}
)
kaito_cache = Cache(config={"CACHE_TYPE": "simple", "CACHE_DEFAULT_TIMEOUT": 3600})
