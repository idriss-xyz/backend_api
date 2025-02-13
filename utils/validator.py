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
        r"^https:\/\/www\.idriss\.xyz\/creators\/donate\?address="
        r"(0x[\dA-Fa-f]{40}|[\w-]+(\.[a-z]+)+)&token="
        r"[\w,]+&network="
        r"[\w,]+&creatorName=[\w%]+$"
    )
    return bool(pattern.fullmatch(url))
