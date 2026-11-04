from pyspark.sql.functions import col

# Leer Silver
silver = spark.read.format("delta").load("/mnt/silver/inpc")

# Dim_Date - Determinista para Power BI
dim_date = silver.select("Fecha").distinct() \
    .withColumnRenamed("Fecha", "Date") \
    .orderBy("Date")

# Fact_INPC - Hechos
fact_inpc = silver.select("Fecha", "INPC", "Year", "Month")

print(f"Dim_Date: {dim_date.count()} Fact: {fact_inpc.count()}")

# Guardar Gold - Star Schema
dim_date.write.format("delta").mode("overwrite").save("/mnt/gold/dim_date")
fact_inpc.write.format("delta").mode("overwrite").save("/mnt/gold/fact_inpc")

print("Gold OK - Star Schema ready for Power BI")
# Evidencia: SELECT * FROM gold.fact_inpc LIMIT 5
