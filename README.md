# Mexico Inflation Tracker | INPC - Banxico

> WE DON'T NEED MORE EXPLANATIONS. WE NEED EVIDENCE.
> STARKCORE C4-002 Verified

## Stack
- Bronze: Banxico CP154 -> Delta
- Silver: PySpark cleaning
- Gold: Star Schema for Power BI
- Viz: DAX YoY + 3M Avg

## Estructura
notebooks/
 01_Bronze_Ingestion.py
 02_Silver_Transformation.py
 03_Gold_Aggregation.py
powerbi/
 dax_measures.txt

## Metricas DAX
- INPC_Actual = SUM(Fact_INPC[INPC])
- Inflacion_YoY = DIVIDE(Actual - AñoAnterior, AñoAnterior)
- INPC_Promedio3M = Rolling 3M

## Evidencia
https://github.com/SolvensAmoris/mexico-inflation-tracker
Built in StarkCore - Ensenada 9:30PM
