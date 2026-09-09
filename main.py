import json

from src.extract.Extraction import run_extraction
from src.transform.transform import run_transformation


def main():
    with open("src/resources/config.json", "r") as file:
        config = json.load(file)
        league = config.get("data_to_fetch").get("competition_code")
        season = config.get("data_to_fetch").get("season")
    run_extraction(season, league)

    run_transformation(season, league)

if __name__ == "__main__":
    main()




