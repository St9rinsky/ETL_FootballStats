import json

from src.extract.Extraction import run_extraction
from src.transform.transform import run_transformation


def main():
    with open("config.json", "r") as file:
        config = json.load(file)
        league = config.get("data_to_fetch").get("competition_code")
    run_extraction(league)

if __name__ == "__main__":
    main()




