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
    invalid_rows = 0
    with SOURCE.open(newline="", encoding="utf-8-sig") as handle:
        for line_number, row in enumerate(csv.DictReader(handle), start=2):
            try:
                day = date.fromisoformat(row["Fecha"].strip())
                value = float(row["INPC"])
                if value <= 0:
                    raise ValueError("INPC must be positive")
            except (KeyError, ValueError, AttributeError):
                invalid_rows += 1
                continue

            if day in rows:
                raise SystemExit(
                    f"Silver validation failed: duplicate observation date "
                    f"{day.isoformat()} (source line {line_number})."
                )
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

    print(
        f"Silver OK: {len(ordered)} unique observations; "
        f"invalid rows skipped={invalid_rows} -> {OUTPUT.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
