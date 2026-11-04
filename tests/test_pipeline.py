"""Offline regression tests for the Bronze -> Silver -> Gold pipeline."""
from __future__ import annotations

import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "notebooks" / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


silver = load_script("silver_pipeline", "02_Silver_Transformation.py")
gold = load_script("gold_pipeline", "03_Gold_Aggregation.py")


class PipelineTests(unittest.TestCase):
    def write_csv(self, path: Path, headers: list[str], rows: list[list[object]]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(headers)
            writer.writerows(rows)

    def test_silver_sorts_and_normalizes_observations(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, output = root / "bronze.csv", root / "silver.csv"
            self.write_csv(source, ["Fecha", "INPC"], [
                ["2024-02-01", "133.2"],
                ["2024-01-01", "132.5"],
                ["bad-date", "not-a-number"],
            ])
            with patch.object(silver, "SOURCE", source), patch.object(silver, "OUTPUT", output), patch.object(silver, "ROOT", root):
                silver.main()
            with output.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual([row["Fecha"] for row in rows], ["2024-01-01", "2024-02-01"])
            self.assertEqual(rows[0]["Year"], "2024")
            self.assertEqual(rows[0]["Month"], "1")
            self.assertEqual(rows[0]["INPC"], "132.500000")

    def test_silver_rejects_duplicate_dates_instead_of_overwriting(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, output = root / "bronze.csv", root / "silver.csv"
            self.write_csv(source, ["Fecha", "INPC"], [
                ["2024-01-01", "132.5"],
                ["2024-01-01", "132.7"],
            ])
            with patch.object(silver, "SOURCE", source), patch.object(silver, "OUTPUT", output):
                with self.assertRaisesRegex(SystemExit, "duplicate observation date"):
                    silver.main()
            self.assertFalse(output.exists())

    def test_gold_builds_fact_and_contiguous_calendar(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, output = root / "silver.csv", root / "gold"
            self.write_csv(source, ["Fecha", "INPC", "Year", "Month"], [
                ["2024-01-01", "132.5", "2024", "1"],
                ["2024-03-01", "134.0", "2024", "3"],
            ])
            with patch.object(gold, "SOURCE", source), patch.object(gold, "GOLD", output):
                gold.main()
            with (output / "fact_inpc.csv").open(newline="", encoding="utf-8") as handle:
                facts = list(csv.DictReader(handle))
            with (output / "dim_date.csv").open(newline="", encoding="utf-8") as handle:
                dates = list(csv.DictReader(handle))
            self.assertEqual(len(facts), 2)
            self.assertEqual(len(dates), 61)
            self.assertEqual(dates[0]["MonthName"], "January")
            self.assertEqual(dates[-1]["Quarter"], "Q1")
            self.assertEqual(dates[-1]["Date"], "2024-03-01")

    def test_gold_rejects_duplicate_fact_dates(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, output = root / "silver.csv", root / "gold"
            self.write_csv(source, ["Fecha", "INPC"], [
                ["2024-01-01", "132.5"],
                ["2024-01-01", "132.6"],
            ])
            with patch.object(gold, "SOURCE", source), patch.object(gold, "GOLD", output):
                with self.assertRaisesRegex(SystemExit, "duplicate fact dates"):
                    gold.main()


if __name__ == "__main__":
    unittest.main(verbosity=2)
