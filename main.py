import json

from src.extract.Extraction import run_extraction
from src.transform.silver.transform import run_transformation
from src.transform.gold.transform_league import run_transformations as gold_transform


def main():
    with open("src/resources/config.json", "r") as file:
        config = json.load(file)
        league = config.get("data_to_fetch").get("competition_code")
        season = config.get("data_to_fetch").get("season")
    run_extraction(season, league)

    run_transformation(season, league)

    gold_transform()

if __name__ == "__main__":
    main()




