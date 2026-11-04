# Mexico Inflation Tracker

End-to-end pipeline analyzing Mexican INPC from Banxico CP154.
Bronze/Silver/Gold with Databricks + Power BI.

## Stack
Databricks, PySpark, DLT, Unity Catalog, Power BI, DAX

## Architecture
- Bronze: Auto Loader CP154 CSV
- Silver: PySpark cleaning
- Gold: Star Schema

StarkCore userland - Built for Canada market.
