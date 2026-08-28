import os
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load my .env variables to my OS
load_dotenv()

API_KEY = os.environ["FOOTBALL_API_KEY"]
BASE_URL = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY, "X-Unfold-Goals": "true"}
OUTPUT_DIR = os.path("data/Bronze")

def get_api_data(league_code: str, filter: dict = None) -> json:
    """
    Fetches data from the football api\n
    Takes a url endpoint and a parameter\n\n

    PARAMETERS:\n
    \tendpoint : str\n
    \tparams : dict\n

    RETURNS: a JSON data object\n
    RAISES: http error if occurs
    """
    endpoint = f"competitions/{league_code}/matches"
    url: str = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, headers = HEADERS, params = filter)

    print("Request URL:", response.url)
    print("Status Code:", response.status_code)

    response.raise_for_status()
    return response.json()

def store_data(data: json) -> None:
    """
    Saves Json data to a dedicated folder\n
    PARAMETERS:\n
    \tdata: json
    """
    file_name = f"{datetime.now().strftime("%Y-%m-%d")}.json"
    file_path = f"{OUTPUT_DIR}/{file_name}"
    os.makedirs(OUTPUT_DIR, exist_ok = True)

    with open(file_path, "w", encoding = "utf-8") as file:
        json.dump(data, file, indent=4)
