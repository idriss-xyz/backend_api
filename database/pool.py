import os
from urllib.parse import urlparse

from psycopg2.pool import SimpleConnectionPool

connection_pool = None


def initialize_pool():
    """Initialize the connection pool with database credentials from environment"""
    global connection_pool
    try:
        DATABASE_URL = os.getenv("DATABASE_URL")
        result = urlparse(DATABASE_URL)

        connection_pool = SimpleConnectionPool(
            1,  # minconn
            20,  # maxconn
            dbname=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port,
        )
    except Exception as e:
        print(f"Error initializing connection pool: {e}")
        raise


def get_db_connection():
    """Get a connection from the pool"""
    if connection_pool:
        return connection_pool.getconn()
    else:
        raise Exception("Connection pool not initialized")


def return_db_connection(conn):
    """Return a connection to the pool"""
    if connection_pool:
        connection_pool.putconn(conn)
