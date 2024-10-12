"""
Fetches wallet data (socials and addresses) from the Airstack API.
"""

import os

import requests

from utils.graph_ql.constants import VERIFIED_ADDRESSES_QUERY

AIRSTACK_API_URL = "https://api.airstack.xyz/graphql"
AIRSTACK_API_KEY = os.getenv("API_KEY_AIRSTACK")


def get_farcaster_verified_addresses(fc_name):
    """
    Fetches connected addresses for the given fcname.

    Args:
        identity (str): The wallet identity to query.

    Returns:
        dict: Wallet socials and addresses.
    """
    if not AIRSTACK_API_KEY:
        raise ValueError("AIRSTACK_API_KEY not set")

    headers = {"Authorization": AIRSTACK_API_KEY, "Content-Type": "application/json"}

    response = requests.post(
        AIRSTACK_API_URL,
        json={
            "query": VERIFIED_ADDRESSES_QUERY,
            "operation_name": "GetMostRecentVerifiedAddresses",
            "variables": {"fc_name": fc_name},
        },
        headers=headers,
        timeout=10,
    )

    response.raise_for_status()
    data = response.json()["data"]
    return data
