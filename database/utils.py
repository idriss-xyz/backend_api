from database.connection import get_db_connection
from server_responses import HTTP_BAD_REQUEST, HTTP_OK


def get_follower_with_connected_address(name=None):
    """
    Fetches follower data. If a name is provided, it returns that follower's data.
    If no name is provided, it returns the full follower JSON.

    Args:
        name (str, optional): The name of a specific follower to retrieve.

    Returns:
        dict: The follower's data if found, or the full JSON if no name is provided.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT follower_data FROM followers WHERE id = 1")
            result = cur.fetchone()

            if result:
                follower_json = result[0]

                if name:
                    return follower_json.get(name, None)

                return follower_json
    return None


def get_all_follower():
    """
    Fetches follower data.

    Args:
        None

    Returns:
        dict: Full name <-> fid mapping of followers
    """
    query = "SELECT follower_data FROM followers WHERE id = 2"

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchone()
                return result[0] if result else None
    except Exception as e:
        # Optionally log the error
        print(f"Error fetching follower: {e}")
        return None


def set_subscription(email):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                insert_query = """
                    INSERT INTO pm_subscribers (email)
                    VALUES (%s)
                    ON CONFLICT (email) DO NOTHING
                    RETURNING id;
                """
                cur.execute(insert_query, (email,))
        return HTTP_OK
    except Exception as e:
        print(e)
        return HTTP_BAD_REQUEST
