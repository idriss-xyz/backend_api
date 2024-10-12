from database.connection import get_db_connection


def get_follower(name=None):
    """
    Fetches follower data. If a name is provided, it returns that follower's data.
    If no name is provided, it returns the full follower JSON.

    Args:
        name (str, optional): The name of a specific follower to retrieve.

    Returns:
        dict: The follower's data if found, or the full JSON if no name is provided.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT follower_data FROM followers WHERE id = 1")
    result = cur.fetchone()

    if result:
        follower_json = result[0]

        if name:
            return follower_json.get(name, None)

        return follower_json
    else:
        return None
