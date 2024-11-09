from cache import twitter_cache, twitter_name_cache
from twitter.utils.database_requests import (
    get_twitter_ids_from_db,
    get_twitter_names_from_db,
)


def get_batch_twitter_ids(user_names):
    try:
        cache_ids = {}
        db_ids = {}

        for user_name in user_names:
            temp_twitter_id = twitter_cache.get(user_name.lower())
            if temp_twitter_id is not None:
                cache_ids[user_name] = temp_twitter_id
                continue

        remaining_names = ""
        for id_ in user_names:
            if id_ not in list(cache_ids):
                remaining_names += "," + id_
        if remaining_names:
            temp_twitter_ids_db = get_twitter_ids_from_db(
                remaining_names[1:].split(",")
            )
            if temp_twitter_ids_db:
                for key, value in temp_twitter_ids_db.items():
                    twitter_cache.set(key.lower(), value)
                db_ids = temp_twitter_ids_db
        return {"data_db": db_ids, "data_cache": cache_ids}
    except Exception as e:
        print("Exception", e)
        return {"data_db": {}, "data_cache": {}}


def get_batch_twitter_usernames(user_ids):
    try:
        print("getting names", user_ids)
        cache_names = {}
        db_names = {}

        for twitter_id in user_ids:
            temp_twitter_username = twitter_name_cache.get(twitter_id)
            if temp_twitter_username is not None:
                cache_names[twitter_id] = temp_twitter_username
                continue

        remaining_ids = ""
        for id_ in user_ids:
            if id_ not in list(cache_names):
                remaining_ids += "," + id_
        print("remaining ids", remaining_ids)
        if remaining_ids:
            temp_twitter_names_db = get_twitter_names_from_db(
                remaining_ids[1:].split(",")
            )
            if temp_twitter_names_db:
                for key, value in temp_twitter_names_db.items():
                    twitter_name_cache.set(value.lower(), key)
                cache_names = {**temp_twitter_names_db, **cache_names}
        return {"data_db": db_names, "data_cache": cache_names}
    except Exception:
        return {"data_db": {}, "data_cache": {}}


def fetch_twitter_ids(usernames):
    result_ids_full_plugin = get_batch_twitter_ids(usernames)
    print(result_ids_full_plugin)
    result_ids_plugin = {
        **result_ids_full_plugin["data_db"],
        **result_ids_full_plugin["data_cache"],
    }
    return result_ids_plugin


def fetch_twitter_usernames(user_ids):
    result_names_full_plugin = get_batch_twitter_usernames(user_ids)
    result_names_plugin = {
        **result_names_full_plugin["data_db"],
        **result_names_full_plugin["data_cache"],
    }
    return result_names_plugin
