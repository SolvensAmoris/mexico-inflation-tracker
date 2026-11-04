# Gold - Star Schema
df_silver = spark.read.format("delta").load("/mnt/silver/inpc")
dim_date = df_silver.select("Fecha").distinct().withColumnRenamed("Fecha","Date")
fact = df_silver
dim_date.write.format("delta").mode("overwrite").save("/mnt/gold/dim_date")
fact.write.format("delta").mode("overwrite").save("/mnt/gold/fact_inpc")
