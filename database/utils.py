from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from database.connection import get_db_connection
from server_responses import HTTP_BAD_REQUEST, HTTP_OK
from web3_utils import ns
from web3_utils.utils import is_address


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


def get_all_creator_links():
    """
    Fetches all creator links.

    Returns:
        list: List of dictionaries containing 'link' and 'created_at'
    """
    query = "SELECT link, created_at FROM creator_links"

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                results = cur.fetchall()
                return (
                    [{"link": row[0], "created_at": row[1]} for row in results]
                    if results
                    else []
                )
    except Exception as e:
        print(f"Error fetching creator links: {e}")
        return None


def add_creator_link(link):
    parsed = urlparse(link)
    query_params = parse_qs(parsed.query)
    try:
        potential_ens = query_params["address"][0]
        if not is_address(potential_ens):
            query_params["address"] = [ns.address(potential_ens)]
            query_params["submitted-address"] = [potential_ens]
    except:
        print("ENS resolver error")
    new_query = urlencode(query_params, doseq=True)
    updated_link = urlunparse(parsed._replace(query=new_query))
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                insert_query = """
                    INSERT INTO creator_links (link)
                    VALUES (%s)
                    ON CONFLICT (link) DO NOTHING
                    RETURNING id;
                """
                cur.execute(insert_query, (updated_link,))
        return HTTP_OK
    except Exception as e:
        print(e)
        return HTTP_BAD_REQUEST
