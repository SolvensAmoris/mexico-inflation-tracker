#!/usr/bin/env python3
"""Download monthly INPC (Banxico SIE series SP1) to the Bronze layer.

Required environment variable: BANXICO_TOKEN
The token is sent only in the Bmx-Token HTTP header and is never written to disk.
"""
from __future__ import annotations

import csv
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "bronze" / "inpc.csv"
SERIES_ID = "SP1"
BASE_URL = "https://www.banxico.org.mx/SieAPIRest/service/v1/series"


def main() -> int:
    token = os.environ.get("BANXICO_TOKEN", "").strip()
    if not token:
        print("ERROR: define BANXICO_TOKEN with your Banxico SIE API token.", file=sys.stderr)
        return 2

    start = "1969-01-01"
    end = date.today().isoformat()
    url = f"{BASE_URL}/{SERIES_ID}/datos/{start}/{end}"
    request = urllib.request.Request(
        url,
        headers={"Bmx-Token": token, "Accept": "application/json", "User-Agent": "MexicoInflationTracker/1.0"},
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"ERROR: Banxico SIE request failed: {exc}", file=sys.stderr)
        return 1

    series = payload.get("bmx", {}).get("series", [])
    if not series or "datos" not in series[0]:
        print("ERROR: unexpected Banxico response; no series/datos payload.", file=sys.stderr)
        return 1

    rows = []
    for item in series[0]["datos"]:
        raw_value = str(item.get("dato", "")).strip()
        raw_date = str(item.get("fecha", "")).strip()
        if not raw_value or raw_value.upper() in {"N/E", "N/D", "NA"}:
            continue
        # SIE API dates are commonly dd/MM/yyyy.
        from datetime import datetime
        try:
            parsed_date = datetime.strptime(raw_date, "%d/%m/%Y").date()
        except ValueError:
            try:
                parsed_date = date.fromisoformat(raw_date)
            except ValueError:
                continue
        try:
            value = float(raw_value.replace(",", ""))
        except ValueError:
            continue
        rows.append((parsed_date.isoformat(), value))

    rows.sort(key=lambda row: row[0])
    if not rows:
        print("ERROR: Banxico returned no numeric observations.", file=sys.stderr)
        return 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Fecha", "INPC"])
        writer.writerows(rows)

    print(f"Bronze OK: {len(rows)} observations -> {OUTPUT.relative_to(ROOT)}")
    print(f"Coverage: {rows[0][0]} to {rows[-1][0]}; source series: {SERIES_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
