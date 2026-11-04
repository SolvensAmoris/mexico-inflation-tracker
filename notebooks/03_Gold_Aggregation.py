#!/usr/bin/env python3
"""Build Power BI star-schema CSV outputs from Silver INPC data."""
from __future__ import annotations
import csv
from datetime import date
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "silver" / "inpc.csv"
GOLD = ROOT / "data" / "gold"

def main() -> None:
    if not SOURCE.exists():
        raise SystemExit("Missing Silver data. Run notebooks/02_Silver_Transformation.py first.")
    with SOURCE.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit("Gold aggregation failed: Silver dataset is empty.")
    fact_rows, dates = [], set()
    for row in rows:
        day, value = date.fromisoformat(row["Fecha"]), float(row["INPC"])
        fact_rows.append((day, value, day.year, day.month))
        dates.add(day)
    fact_rows.sort(key=lambda item: item[0])
    GOLD.mkdir(parents=True, exist_ok=True)
    with (GOLD / "fact_inpc.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Fecha", "INPC", "Year", "Month"])
        for day, value, year, month in fact_rows:
            writer.writerow([day.isoformat(), f"{value:.6f}", year, month])
    with (GOLD / "dim_date.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Date", "Year", "MonthNumber", "MonthName", "YearMonth", "Quarter"])
        for day in sorted(dates):
            writer.writerow([day.isoformat(), day.year, day.month, day.strftime("%B"),
                             day.strftime("%Y-%m"), f"Q{((day.month - 1) // 3) + 1}"])
    print(f"Gold OK: Fact_INPC={len(fact_rows)}; Dim_Date={len(dates)}")

if __name__ == "__main__":
    main()
