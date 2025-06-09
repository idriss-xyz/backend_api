import re

ALLOWED_ORIGINS = [
    "https://idriss.xyz",
    "https://www.idriss.xyz",
]


URL_SCHEMA = {
    "type": "object",
    "properties": {
        "url": {
            "type": "string",
            "anyOf": [
                {"pattern": r"^https://across\.to/api/suggested-fees\?.*"},
            ],
        }
    },
    "required": ["url"],
}


def is_valid_donation_url(url: str) -> bool:
    pattern = re.compile(
        r"^https://www\.idriss\.xyz/creators/"
        r"(?:(?:donate\?address="
        r"(0x[\da-fA-F]{40}|[\w-]+(?:\.[a-z]+)+)"
        r"&token=[\w,]+&network=[\w,]+&creatorName=[\w%]+)"
        r"|[A-Za-z0-9_-]+)"
        r"/?$"
    )
    return bool(pattern.fullmatch(url))
