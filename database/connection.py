from contextlib import contextmanager

from .pool import get_db_connection, return_db_connection

@contextmanager
def get_db_cursor():
    """Context manager for database cursor"""
    conn = get_db_connection()
    try:
        yield conn.cursor()
        conn.commit()
    finally:
        conn.close()
        return_db_connection(conn)

def create_table():
    """Create required database tables"""
    conn = get_db_connection()
    try:
        cur = conn.cursor()

        # Create the table for storing followers as JSON
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS followers (
                id SERIAL PRIMARY KEY,
                follower_data jsonb
            )
        """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS pm_subscribers (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS twitter_cache (
                user_name VARCHAR(20) NOT NULL,
                user_id VARCHAR(25) NOT NULL,
                topicality TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_name),
                UNIQUE (user_id)
            );
        """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS creator_links (
                id SERIAL PRIMARY KEY,
                link TEXT NOT NULL UNIQUE,
                created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """
        )

        conn.commit()
        cur.close()
    finally:
        conn.close()
        return_db_connection(conn)
