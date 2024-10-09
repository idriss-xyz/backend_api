from datetime import datetime

import requests

from utils.graph_ql.fc_connected_addresses import get_follower


def get_farcaster_verified_addresses(fid):
    url = f"https://api.warpcast.com/v2/verifications?fid={fid}"
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
                connected_addresses = social["connectedAddresses"]

                if profile_name and connected_addresses:
                    evm_addresses = [
                        addr for addr in connected_addresses if addr["address"].startswith("0x")
                    ]

                    if evm_addresses:
                        latest_evm_address = max(
                            evm_addresses,
                            key=lambda addr: datetime.fromisoformat(addr["timestamp"].replace("Z", "+00:00"))
                        )
                        all_followers[profile_name] = latest_evm_address["address"]

        if not has_next_page:
            break

    return all_followers
