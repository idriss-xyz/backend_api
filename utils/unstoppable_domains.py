import os
import requests


def get_unstoppable_domain_owner(domain):
    url = f"https://api.unstoppabledomains.com/resolve/domains/{domain}"
    response = requests.get(url, headers={'accept': 'application/json', 'authorization': f'Bearer {os.getenv("UD_API_KEY")}'})
    response.raise_for_status()
    return response.json()
