import os
from urllib.parse import urlparse

import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")
result = urlparse(DATABASE_URL)
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port


def create_table(connection):
    cur = connection.cursor()

    # Create the table for storing followers as JSON
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS followers (
            id SERIAL PRIMARY KEY,
            follower_data jsonb
        )
    """
    )

    connection.commit()
    cur.close()
    connection.close()


def get_db_connection():
    return psycopg2.connect(
        dbname=database, user=username, password=password, host=hostname, port=port
    )


conn = get_db_connection()

create_table(conn)
