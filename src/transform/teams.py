from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from delta.tables import DeltaTable

def transform_teams(spark: SparkSession, matches_data, output_path):
    
    home_teams = matches_data.select(
        col("match.homeTeam.id").alias("team_id"),
        col("match.homeTeam.name").alias("full_name"),
        col("match.homeTeam.shortName").alias("short_name"),
        col("match.homeTeam.tla").alias("abbr_name"),
        col("match.homeTeam.crest").alias("logo")
    )
    
    away_teams = matches_data.select(
        col("match.awayTeam.id").alias("team_id"),
        col("match.awayTeam.name").alias("full_name"),
        col("match.awayTeam.shortName").alias("short_name"),
        col("match.awayTeam.tla").alias("abbr_name"),
        col("match.awayTeam.crest").alias("logo")
    )
    
    new_teams = home_teams.union(away_teams).dropDuplicates(["team_id"])
    
    if DeltaTable.isDeltaTable(spark, output_path):

        existing_table = DeltaTable.forPath(spark, output_path)

        existing_table.alias("old") \
            .merge(new_teams.alias("new"), "old.team_id = new.team_id") \
            .whenNotMatchedInsertAll() \
            .execute()
    else:
        new_teams.write.format("delta").mode("overwrite").save(output_path)
