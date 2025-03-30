from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from database.pool import get_db_connection, return_db_connection
from server_responses import HTTP_BAD_REQUEST, HTTP_OK
from web3_utils import ns
from web3_utils.utils import is_address

def get_follower_with_connected_address(name=None):
    """
    Fetches follower data. If a name is provided, returns that follower's data.
    If no name is provided, returns the full follower JSON.
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT follower_data FROM followers WHERE id = 1")
            result = cur.fetchone()
            if result:
                follower_json = result[0]
                return follower_json.get(name, None) if name else follower_json
            return None
    except Exception as e:
        print(f"Error in get_follower_with_connected_address: {e}")
        return None
    finally:
        if conn:
            return_db_connection(conn)

def get_all_follower():
    """
    Fetches follower data.
    Returns dict: Full name <-> fid mapping of followers
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT follower_data FROM followers WHERE id = 2")
            result = cur.fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"Error fetching follower: {e}")
        return None
    finally:
        if conn:
            return_db_connection(conn)

def set_subscription(email):
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            insert_query = """
                INSERT INTO pm_subscribers (email)
                VALUES (%s)
                ON CONFLICT (email) DO NOTHING
                RETURNING id;
            """
            cur.execute(insert_query, (email,))
            conn.commit()
        return HTTP_OK
    except Exception as e:
        print(f"Error setting subscription: {e}")
        return HTTP_BAD_REQUEST
    finally:
        if conn:
            return_db_connection(conn)

def get_all_creator_links():
    """
    Fetches all creator links.
    Returns list: List of dictionaries containing 'link' and 'created_at'
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT link, created_at FROM creator_links")
            results = cur.fetchall()
            return [{"link": row[0], "created_at": row[1]} for row in results] if results else []
    except Exception as e:
        print(f"Error fetching creator links: {e}")
        return None
    finally:
        if conn:
            return_db_connection(conn)

def add_creator_link(link):
    conn = None
    try:
        parsed = urlparse(link)
        query_params = parse_qs(parsed.query)
        try:
            potential_ens = query_params["address"][0]
            if not is_address(potential_ens):
                query_params["address"] = [ns.address(potential_ens)]
                query_params["submitted-address"] = [potential_ens]
        except Exception as e:
            print(f"ENS resolver error: {e}")
            
        new_query = urlencode(query_params, doseq=True)
        updated_link = urlunparse(parsed._replace(query=new_query))
        
        conn = get_db_connection()
        with conn.cursor() as cur:
            insert_query = """
                INSERT INTO creator_links (link)
                VALUES (%s)
                ON CONFLICT (link) DO NOTHING
                RETURNING id;
            """
            cur.execute(insert_query, (updated_link,))
            conn.commit()
        return HTTP_OK
    except Exception as e:
        print(f"Error adding creator link: {e}")
        return HTTP_BAD_REQUEST
    finally:
        if conn:
            return_db_connection(conn)
