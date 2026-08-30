from pyspark.sql import SparkSession
from delta.tables import DeltaTable
from pyspark.sql.functions import col


def transform_matches(spark: SparkSession, matches_data, output_path):

    table_path = str(output_path) + "matches"

    matches = matches_data.select(
        col("match.id").alias("match_id"),
        col("match.matchday").alias("match_day"),
        col("match.utcDate").alias("match_date"),
        col("match.status").alias("status"),
        col("match.homeTeam.id").alias("home_team_id"),
        col("match.homeTeam.shortName").alias("home_team"),
        col("match.awayTeam.id").alias("away_team_id"),
        col("match.awayTeam.shortName").alias("away_team"),
        col("match.score.fullTime.home").alias("home_goals"),
        col("match.score.fullTime.away").alias("away_goals")
    )

    if DeltaTable.isDeltaTable(spark, table_path):

        existing_table = DeltaTable.forPath(spark, table_path)

        existing_table.alias("old")\
        .merge(matches.alias("new"),"old.match_id = new.match_id")\
        .whenMatchedUpdateAll()\
        .whenNotMatchedInsertAll()\
        .execute()

    else:
        matches.write.format("delta").mode("overwrite").save(table_path)