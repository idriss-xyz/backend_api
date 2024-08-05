import requests


def get_farcaster_verified_addresses(fid):
    url = f"https://api.warpcast.com/v2/verifications?fid={fid}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
