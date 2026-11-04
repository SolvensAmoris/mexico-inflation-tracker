from pyspark.sql.functions import col, to_date, year, month, trim

# Leer Bronze
df = spark.read.format("delta").load("/mnt/bronze/inpc")

# Limpieza Banxico viene con espacios
df_clean = df.withColumn("Fecha", trim(col("Fecha"))) \
             .withColumn("INPC", trim(col("INPC")))

# Cast correcto
df_cast = df_clean.withColumn("Fecha", to_date(col("Fecha"), "dd/MM/yyyy")) \
                  .withColumn("INPC", col("INPC").cast("double")) \
                  .dropna(subset=["Fecha","INPC"])

df_final = df_cast.withColumn("Year", year(col("Fecha"))) \
                  .withColumn("Month", month(col("Fecha")))

print(f"Silver count: {df_final.count()}")
df_final.display()

# Guardar Silver
df_final.write.format("delta").mode("overwrite").save("/mnt/silver/inpc")
print("Silver OK - STARKCORE verified")
