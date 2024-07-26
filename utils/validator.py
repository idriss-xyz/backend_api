URL_SCHEMA = {
    "type": "object",
    "properties": {
        "url": {
            "type": "string",
            "anyOf": [
                {"pattern": r"^https://across\.to/api/suggested-fees\?.*"},
            ]
        }
    },
    "required": ["url"]
}