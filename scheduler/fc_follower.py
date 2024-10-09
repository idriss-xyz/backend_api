"""
Periodically sends requests to update @idriss farcaster followers.
"""

import requests

eligible_addresses = requests.get("https://www.api.idriss.xyz/update-fc_follower", timeout=600)

