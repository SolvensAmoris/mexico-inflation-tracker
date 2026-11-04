from pyspark.sql.functions import to_date, col, year, month

df_bronze = spark.read.format("delta").load("/mnt/bronze/inpc")

df_silver = df_bronze.withColumn("Fecha", to_date(col("Fecha"), "dd/MM/yyyy")) \
  .withColumn("INPC", col("INPC").cast("double")) \
  .dropna(subset=["Fecha","INPC"]) \
  .withColumn("Year", year("Fecha")) \
  .withColumn("Month", month("Fecha"))

df_silver.write.format("delta").mode("overwrite").save("/mnt/silver/inpc")
