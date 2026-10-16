from pyspark.sql.functions import col, when, lit, sum, row_number
from pyspark.sql.window import Window

from src.spark.session import spark


def get_teams(path):
    return spark.read.format("delta").load(
        f"data/Silver/{path}/teams"
    )


def get_finished_matches(path):
    matches = spark.read.format("delta").load(
        f"data/Silver/{path}/matches"
    )

    return matches.filter(col("status") == "FINISHED")


def transform_matches(side, matches):
    other = "away" if side == "home" else "home"

    return matches.select(
    col(f"{side}_team_id").alias("team_id"),

    lit(1).alias("played"),

    when(col(f"{side}_score") > col(f"{other}_score"), 1).otherwise(0).alias("wins"),

    when(col(f"{side}_score") == col(f"{other}_score"), 1).otherwise(0).alias("draws"),

    when(col(f"{side}_score") < col(f"{other}_score"), 1).otherwise(0).alias("losses"),

    col(f"{side}_score").alias("goals_for"),

    col(f"{other}_score").alias("goals_against"),

    when(
    col(f"{side}_score") > col(f"{other}_score"), 3
    ).when(
    col(f"{side}_score") == col(f"{other}_score"), 1
    ).otherwise(0).alias("points"))


def aggregate_stats(home, away):
    return home.unionByName(away) \
    .groupBy("team_id") \
    .agg(
        sum("played").alias("played"),
        sum("wins").alias("wins"),
        sum("draws").alias("draws"),
        sum("losses").alias("losses"),
        sum("goals_for").alias("goals_for"),
        sum("goals_against").alias("goals_against"),
        sum("points").alias("points")
    )

def build_table(stats, teams):
    table = teams.join(stats, on="team_id",how="left") \
    .fillna({
        "played": 0,
        "wins": 0,
        "draws": 0,
        "losses": 0,
        "goals_for": 0,
        "goals_against": 0,
        "points": 0}) \
    .withColumn(
        "goal_difference",
        col("goals_for") - col("goals_against"))

    window = Window.orderBy(
        col("points").desc(),
        col("goal_difference").desc(),
        col("goals_for").desc())

    return table.withColumn(
        "position",
        row_number().over(window)
        ).select(
            "position",
            "team_id",
            "team_name",
            "played",
            "wins",
            "draws",
            "losses",
            "goals_for",
            "goals_against",
            "goal_difference",
            "points"
        )

def save(table, path):
    table.write \
    .format("delta") \
    .mode("overwrite") \
    .save(path)


def run_transformations(path, gold_path):
    teams = get_teams(path)
    matches = get_finished_matches(path)

    home = transform_matches("home", matches)
    away = transform_matches("away", matches)

    team_stats = aggregate_stats(home, away)

    table = build_table(team_stats, teams)

    save(table, gold_path)