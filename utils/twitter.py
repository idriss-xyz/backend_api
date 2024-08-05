import requests


def get_twitter_id(cleaned_identifier):
    url = f"https://www.idriss.xyz/v1/getTwitterIDPlugin?usernames={cleaned_identifier}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
