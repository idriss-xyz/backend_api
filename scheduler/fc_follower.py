"""
Periodically sends requests to update @idriss farcaster followers.
"""

import json
import os
import time
from datetime import datetime
from urllib.parse import urlparse

import psycopg2
import requests

AIRSTACK_API_URL = "https://api.airstack.xyz/graphql"
AIRSTACK_API_KEY = os.getenv("API_KEY_AIRSTACK")

DATABASE_URL = os.getenv("DATABASE_URL")
result = urlparse(DATABASE_URL)
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port

FOLLOWER_QUERY = """query MyQuery($cursor: String!) {
  SocialFollowers(
    input: {filter: {dappName: {_eq: farcaster}, identity: {_eq: "fc_fname:idriss"}}, blockchain: ALL, limit: 200, cursor: $cursor}
  ) {
    Follower {
      followerAddress {
        socials(input: {filter: {dappName: {_eq: farcaster}}}) {
          profileName
          userId
          connectedAddresses {
            address
            timestamp
          }
        }
      }
    }
    pageInfo {
      nextCursor
      hasNextPage
    }
  }
}"""


def get_db_connection():
    return psycopg2.connect(
        dbname=database, user=username, password=password, host=hostname, port=port
    )


def get_follower(cursor=""):
    """
    Fetches followers of @idriss farcaster account from Airstack.

    Args:
        cursor (str): Next page cursor.

    Returns:
        dict: Account name to wallet address mapping.
    """
    if not AIRSTACK_API_KEY:
        raise ValueError("AIRSTACK_API_KEY not set")

    headers = {"Authorization": AIRSTACK_API_KEY, "Content-Type": "application/json"}

    response = requests.post(
        AIRSTACK_API_URL,
        json={
            "query": FOLLOWER_QUERY,
            "operation_name": "MyQuery",
            "variables": {"cursor": cursor},
        },
        headers=headers,
        timeout=10,
    )

    response.raise_for_status()
    data = response.json()["data"]
    return data


def get_fc_twitter_account_verifications(cursor=""):
    """
    Fetches Twitter verifications from Warpcast API.

    Args:
        cursor (str): Next page cursor.

    Returns:
        dict: fid to twitter name mapping.
    """
    base_url = "https://api.warpcast.com/fc/account-verifications?limit=1000"
    url = f"{base_url}&cursor={cursor}" if cursor else base_url
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def update_follower():
    """
    Fetches all followers of the @idriss Farcaster account.
    Paginates through all results to ensure all followers are retrieved and returns the latest address mapping.

    Returns:
        dict: A mapping of account names to the latest wallet address (newest by timestamp).
    """
    cursor = ""
    all_followers = {}
    follower_mapping = {}

    while True:
        data = get_follower(cursor)

        followers = data["SocialFollowers"]["Follower"]
        page_info = data["SocialFollowers"]["pageInfo"]
        cursor = page_info["nextCursor"]
        has_next_page = page_info["hasNextPage"]

        for follower in followers:
            socials = follower["followerAddress"]["socials"]
            for social in socials:
                profile_name = social["profileName"]
                profile_fid = social["userId"]
                connected_addresses = social["connectedAddresses"]
                if profile_name and profile_fid:
                    follower_mapping[profile_name] = profile_fid
                if profile_name and connected_addresses:
                    evm_addresses = [
                        addr
                        for addr in connected_addresses
                        if addr["address"].startswith("0x")
                    ]

                    if evm_addresses:
                        latest_evm_address = max(
                            evm_addresses,
                            key=lambda addr: datetime.fromisoformat(
                                addr["timestamp"].replace("Z", "+00:00")
                            ),
                        )
                        all_followers[profile_name] = {
                            "address": latest_evm_address["address"],
                            "fid": profile_fid,
                            "twitter": "",
                        }

        if not has_next_page:
            break
    try:
        verifications = update_twitter_verifications()
        for _, follower_info in all_followers.items():
            fid = follower_info.get("fid", "")

            if fid in verifications:
                follower_info["twitter"] = verifications[fid]
    except:
        print("verifications not updated")
    store_follower(all_followers, follower_mapping)
    return all_followers


def store_follower(all_follower_json, follower_mapping_json):
    """
    Stores the full JSON data of all followers, overwriting the existing entry.

    Args:
        follower_json (dict): The JSON data to store.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO followers (id, follower_data)
        VALUES (1, %s)
        ON CONFLICT (id) DO UPDATE SET follower_data = EXCLUDED.follower_data
    """,
        [json.dumps(all_follower_json)],
    )
    cur.execute(
        """
        INSERT INTO followers (id, follower_data)
        VALUES (2, %s)
        ON CONFLICT (id) DO UPDATE SET follower_data = EXCLUDED.follower_data
    """,
        [json.dumps(follower_mapping_json)],
    )
    conn.commit()
    cur.close()
    conn.close()


def update_twitter_verifications():
    """
    Fetches all verified twitter accounts.
    Paginates through all results to ensure all verifications are retrieved.

    Returns:
        dict: A mapping of twitter account names to fid.
    """
    cursor = ""
    verified_fid_to_twitter = {}

    while True:
        data = get_fc_twitter_account_verifications(cursor)
        verifications = data["result"]["verifications"]

        for verified_account in verifications:
            fid = str(verified_account["fid"])
            twitter_username = verified_account["platformUsername"]
            if fid and twitter_username:
                verified_fid_to_twitter[fid] = twitter_username
        page_info = data.get("next", None)
        if not page_info:
            break
        cursor = page_info.get("cursor", None)

    return verified_fid_to_twitter


def set_interval(func, sec):
    for _ in range(4):
        try:
            func()
        except:
            continue
        time.sleep(sec)


set_interval(update_follower, 120)
