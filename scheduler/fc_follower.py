"""
Periodically sends requests to update @idriss farcaster followers.
"""

import time

import requests

url = "https://www.api.idriss.xyz/update-fc-follower"

for _ in range(4):
    try:
        eligible_addresses = requests.get(url, timeout=100)
        print("Request sent. Status code:", eligible_addresses.status_code)

    except requests.RequestException as e:
        print("Error sending request:", str(e))

    time.sleep(120)


