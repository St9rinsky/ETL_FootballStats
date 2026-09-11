import sys, os, glob
from pathlib import Path
from pyspark.sql.functions import col, explode

from src.spark.session import spark
from transform.silver.teams import transform_teams
from transform.silver.matches import transform_matches

if os.name == "nt":
    os.environ["HADOOP_HOME"] = r"C:\hadoop"
    sys.path.append(r"C:\hadoop\bin")

BRONZE_PATH = "data/Bronze"


def get_recent_data(path):
    files = [Path(file) for file in glob.glob(f"{path}/*.json")]

    if not files:
        raise FileNotFoundError(f"No json files exist in {path}")

    return max(files, key=lambda file: file.stat().st_mtime)


def is_matchday_one(match_data):
    return (
        match_data
        .filter(col("match.matchday") == 1)
        .limit(1)
        .count() > 0)


def process_file(spark, bronze_file, season, league_code):
    print(f"Processing: {bronze_file}")

    raw_data = spark.read.option("multiLine", True).json(str(bronze_file))
    matches = raw_data.select(explode(col("matches")).alias("match"))

    transform_matches(spark, matches, season, league_code)

    if is_matchday_one(matches):
            print("Matchday 1 detected")
            print("Adding new teams...")

            transform_teams(spark, matches, season, league_code)


def run_transformation(season, code):
    recent_raw = get_recent_data(BRONZE_PATH)
    process_file(spark, recent_raw, season, code)

    spark.stop()