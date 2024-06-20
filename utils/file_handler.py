import json
import os


def fetch_custom_badges():
    root_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    file_path = os.path.join(root_dir, "data", "customBadges.json")

    with open(file_path, "r", encoding="utf-8") as badges:
        data = json.load(badges)
    return data

def fetch_handles():
    root_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    file_path = os.path.join(root_dir, "data", "daoHandles.json")

    with open(file_path, "r", encoding="utf-8") as badges:
        data = json.load(badges)
    return data


def fetch_agora_mock():
    root_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    file_path = os.path.join(root_dir, "data", "agoraMock.json")

    with open(file_path, "r", encoding="utf-8") as badges:
        data = json.load(badges)
    return data