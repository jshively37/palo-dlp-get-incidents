from datetime import date, timedelta, timezone
from dotenv import load_dotenv

import csv
import os
import requests

BASE_AUTH_URL = "https://auth.apps.paloaltonetworks.com/auth/v1/oauth2/access_token"
BASE_URL = "https://api.dlp.paloaltonetworks.com/v2/api/"

HEADERS = {
    "Accept": "application/json",
}

AUTH_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
}

load_dotenv()
TSG_ID = os.environ.get("TSG_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
SECRET_ID = os.environ.get("SECRET_ID")

FIELDNAMES = [
    "action",
    "app_id",
    "app_name",
    "channel",
    "data_profile_id",
    "data_profile_name",
    "file_name",
    "file_sha",
    "file_type",
    "incident_creation_time",
    "incident_id",
    "report_id",
    "source",
    "tenant_id",
    "user",
]


def create_token():
    auth_url = f"{BASE_AUTH_URL}?grant_type=client_credentials&scope:tsg_id:{TSG_ID}"

    token = requests.request(
        method="POST",
        url=auth_url,
        headers=AUTH_HEADERS,
        auth=(CLIENT_ID, SECRET_ID),
    ).json()
    HEADERS.update({"Authorization": f'Bearer {token["access_token"]}'})


def get_dlp_incidents(page_size: int = 2000):
    url = BASE_URL + f"incidents?page_size={page_size}"
    return requests.request(method="GET", url=url, headers=HEADERS).json()


if __name__ == "__main__":
    create_token()
    incidents = get_dlp_incidents()
    csv_file = "output/output.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(incidents["resources"])
