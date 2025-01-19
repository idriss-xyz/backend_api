import json
import os

from utils.constants import INELIGIBLE


def fetch_custom_badges():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(root_dir, "data", "customBadges.json")

    with open(file_path, "r", encoding="utf-8") as badges:
        data = json.load(badges)
    return data


def fetch_gitcoin_rounds_by_chain():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(root_dir, "data", "gitcoinRounds.json")

    with open(file_path, "r", encoding="utf-8") as badges:
        data = json.load(badges)
    return data


def fetch_handles():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(root_dir, "data", "daoHandles.json")

    with open(file_path, "r", encoding="utf-8") as badges:
        data = json.load(badges)
    return data


def get_status():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(root_dir, "data", "serviceStatus.json")
    with open(file_path, "r", encoding="utf-8") as service_status:
        status = json.load(service_status)
    return status


def get_eligibility(address):
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(root_dir, "data", "eligibility.json")
    with open(file_path, "r", encoding="utf-8") as eligibility:
        status = json.load(eligibility)
    eligibility_status_for_address = status.get(address, INELIGIBLE)
    return eligibility_status_for_address
