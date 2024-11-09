from database import get_db_connection


def get_twitter_ids_from_db(usernames):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                user_names = [
                    username.replace("@", "").lower() for username in usernames
                ]
                sql_query = (
                    "SELECT user_name, user_id FROM twitter_cache WHERE user_name IN %s"
                )
                cur.execute(sql_query, (tuple(user_names),))
                results = cur.fetchall()
                id_dict = {}
                for result in results:
                    id_dict[result[0]] = str(result[1])
                return id_dict
    except Exception:
        return {}


def get_twitter_names_from_db(user_ids):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                sql_query = (
                    "SELECT user_id, user_name FROM twitter_cache WHERE user_id IN %s"
                )

                cur.execute(sql_query, (tuple(user_ids),))
                results = cur.fetchall()
                id_dict = {}
                for result in results:
                    id_dict[str(result[0])] = result[1]
                return id_dict
    except Exception:
        return {}
