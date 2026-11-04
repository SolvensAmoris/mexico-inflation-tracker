#!/usr/bin/env python3
"""Validate and normalize Bronze INPC observations into the Silver layer."""
from __future__ import annotations
import csv
from datetime import date
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "bronze" / "inpc.csv"
OUTPUT = ROOT / "data" / "silver" / "inpc.csv"

def main() -> None:
    if not SOURCE.exists():
        raise SystemExit("Missing Bronze data. Run notebooks/01_Bronze_Ingestion.py first.")
    rows: dict[date, float] = {}
    with SOURCE.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            try:
                day = date.fromisoformat(row["Fecha"].strip())
                value = float(row["INPC"])
            except (KeyError, ValueError, AttributeError):
                continue
            if value > 0:
                rows[day] = value
    if not rows:
        raise SystemExit("Silver validation failed: no valid Fecha/INPC rows.")
    ordered = sorted(rows.items())
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Fecha", "INPC", "Year", "Month"])
        for day, value in ordered:
            writer.writerow([day.isoformat(), f"{value:.6f}", day.year, day.month])
    print(f"Silver OK: {len(ordered)} unique monthly observations -> {OUTPUT.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
