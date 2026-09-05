from pathlib import Path
from pyspark.sql import SparkSession
from delta.tables import DeltaTable
from pyspark.sql.functions import col, to_timestamp, to_date, date_format, when

def transform_matches(spark: SparkSession, matches_data, output_path):

    matches = matches_data.select(
        col("match.id").alias("match_id"),
        col("match.matchday").alias("match_day"),

        date_format(to_timestamp(col("match.utcDate")),"yyyy-MM-dd").alias("match_date"),

        date_format(to_timestamp(col("match.utcDate")),"HH:mm").alias("match_time"),

        when(col("match.status") != "FINISHED","SCHEDULED")
        .otherwise(col("match.status")).alias("status"),

        col("match.homeTeam.id").alias("home_team_id"),
        col("match.awayTeam.id").alias("away_team_id"),
        col("match.score.fullTime.home").alias("home_goals"),
        col("match.score.fullTime.away").alias("away_goals")
    )

    if DeltaTable.isDeltaTable(spark, output_path):

        existing_table = DeltaTable.forPath(spark, output_path)

        existing_table.alias("old")\
        .merge(matches.alias("new"),"old.match_id = new.match_id")\
        .whenMatchedUpdateAll()\
        .whenNotMatchedInsertAll()\
        .execute()

    else:
        matches.write.format("delta").mode("overwrite").save(output_path)