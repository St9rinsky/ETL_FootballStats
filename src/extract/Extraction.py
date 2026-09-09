import os, json, requests
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load my .env variables to my OS
load_dotenv()

API_KEY = os.environ["FOOTBALL_API_KEY"]
BASE_URL = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}
OUTPUT_DIR = "data/Bronze"


def full_load_exists(season, league_code):

    bronze_path = Path(f"data/Bronze")

    return any(bronze_path.glob("*_full_load.json"))


def get_api_data(league_code, filter):

    endpoint = f"competitions/{league_code}/matches"
    url: str = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, headers = HEADERS, params = filter)

    print("Request URL:", response.url)
    print("Status Code:", response.status_code)

    response.raise_for_status()

    return response.json()


def store_data(data, full_load = False):
    file_name = f"{datetime.now().strftime('%Y-%m-%d')}"

    if full_load:
        file_name = file_name + "_full_load"

    file_path = f"{OUTPUT_DIR}/{file_name}.json"
    os.makedirs(OUTPUT_DIR, exist_ok = True)

    with open(file_path, "w", encoding = "utf-8") as file:
        json.dump(data, file, indent=4)


def run_extraction(season, league_code):

    if not full_load_exists(season, league_code):
        print("old essential data missing!!!")
        print("executing full load extraction for essential data....")
        today = datetime.now()
        full_load = {"season" : today.year if today.month >= 7 else today.year - 1}
        past_data = get_api_data(league_code,full_load)
        store_data(past_data, full_load=True)

    else:
        # rolling window filter 7 days forward, 7 days before
        today = datetime.now().date()
        start_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        end_date = (today + timedelta(days=7)).strftime("%Y-%m-%d")

        window = {"dateFrom" : start_date,"dateTo" : end_date,}
    
        data = get_api_data(league_code, window)
        store_data(data)