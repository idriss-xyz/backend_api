import os

import requests


def get_farcaster_verified_addresses(fid):
    url = f"https://api.warpcast.com/v2/verifications?fid={fid}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_farcaster_link(fid):
    server = "https://hubs.airstack.xyz"
    endpoint = f"{server}/v1/linkById?fid={fid}&target_fid=189333&link_type=follow"
    
    headers = {
        "Content-Type": "application/json",
        "x-airstack-hubs": os.getenv("API_KEY_AIRSTACK"),
    }
    
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    json_data = response.json()
    return json_data
