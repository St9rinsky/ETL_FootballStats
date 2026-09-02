import glob
import os
import sys
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode

from src.transform.teams import transform_teams
from src.transform.matches import transform_matches

os.environ["HADOOP_HOME"] = r"C:\hadoop"
sys.path.append(r"C:\hadoop\bin")
BRONZE_PATH = Path("data/Bronze")
SILVER_TEAMS_PATH = Path("data/Silver/season_league_code/teams")
SILVER_MATCHES_PATH = Path("data/Silver/matches")
os.environ["PYSPARK_SUBMIT_ARGS"] = "--conf spark.driver.extraJavaOptions=-Divy.log=error --packages io.delta:delta-spark_2.13:4.4.0 pyspark-shell"


def get_recent_data(path: Path):
    """
    Takes the most recent added file, uses alphabetical ordering\n
    PARAMETERS:\n
    \tpath: Path\n
    RETURN -> most recent file in path

    RAISES:\n
    \tFileNotFoundError : when no files exist

    """
    files = glob.glob(f"{path}/*.json")

    if not files:
        raise FileNotFoundError (f"No json files exist in {path}")
    return max(files)


def is_matchday_one(match_data) -> bool:
    """
    check if match data contains matchday one games
    """
    return (
        match_data
        .filter(col("match.matchday") == 1)
        .limit(1)
        .count() > 0)


def process_file(spark, bronze_file) -> None:
    """
    Processes a file, using spark to extract match data,
    transforms the matches from the match data and if
    the matches contain matches for matchday one, new teams get
    data gets processed

    PARAMETERS:\n
    \tspark : SparkSession
    \tbronze_file : str
    """

    print(f"Processing: {bronze_file}")

    raw_data = spark.read.option("multiLine", True).json(str(bronze_file))
    matches = raw_data.select(explode(col("matches")).alias("match"))

    transform_matches(spark, matches, SILVER_MATCHES_PATH)

    if is_matchday_one(matches):
            print("Matchday 1 detected")
            print("Adding new teams...")

            transform_teams(spark, matches, SILVER_TEAMS_PATH)


def main():
    spark = SparkSession.builder \
        .appName("Transformations") \
        .master("local[*]") \
        .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.4.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

    file = get_recent_data(BRONZE_PATH)
    process_file(spark, file)

    spark.stop()

main()