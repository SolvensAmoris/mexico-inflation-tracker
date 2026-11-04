#!/usr/bin/env python3
"""Build Power BI star-schema CSV outputs from Silver INPC data."""
from __future__ import annotations

import csv
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "silver" / "inpc.csv"
GOLD = ROOT / "data" / "gold"
MONTH_NAMES = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit("Missing Silver data. Run notebooks/02_Silver_Transformation.py first.")

    with SOURCE.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit("Gold aggregation failed: Silver dataset is empty.")

    fact_rows = []
    for row in rows:
        try:
            day = date.fromisoformat(row["Fecha"])
            value = float(row["INPC"])
        except (KeyError, ValueError, TypeError) as exc:
            raise SystemExit(f"Gold validation failed: invalid Silver row: {row!r}") from exc
        if value <= 0:
            raise SystemExit(f"Gold validation failed: non-positive INPC on {day.isoformat()}.")
        fact_rows.append((day, value, day.year, day.month))

    fact_rows.sort(key=lambda item: item[0])
    if len({item[0] for item in fact_rows}) != len(fact_rows):
        raise SystemExit("Gold validation failed: duplicate fact dates.")

    GOLD.mkdir(parents=True, exist_ok=True)
    with (GOLD / "fact_inpc.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Fecha", "INPC", "Year", "Month"])
        for day, value, year, month in fact_rows:
            writer.writerow([day.isoformat(), f"{value:.6f}", year, month])

    start, end = fact_rows[0][0], fact_rows[-1][0]
    with (GOLD / "dim_date.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Date", "Year", "MonthNumber", "MonthName", "YearMonth", "Quarter"])
        day = start
        while day <= end:
            writer.writerow([
                day.isoformat(), day.year, day.month, MONTH_NAMES[day.month - 1],
                day.strftime("%Y-%m"), f"Q{((day.month - 1) // 3) + 1}",
            ])
            day += timedelta(days=1)

    calendar_days = (end - start).days + 1
    print(
        f"Gold OK: Fact_INPC={len(fact_rows)} monthly observations; "
        f"Dim_Date={calendar_days} calendar days"
    )


if __name__ == "__main__":
    main()
