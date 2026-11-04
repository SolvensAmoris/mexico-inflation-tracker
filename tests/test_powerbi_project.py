"""Structural guardrails for the Power BI Project (PBIP/PBIR/TMDL)."""
from __future__ import annotations
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POWERBI = ROOT / "powerbi"
REPORT = POWERBI / "Mexico-Inflation-Tracker.Report"
MODEL = POWERBI / "Mexico-Inflation-Tracker.SemanticModel"

class PowerBIProjectTests(unittest.TestCase):
    def test_pbip_entrypoint_and_relative_model_reference(self):
        pbip = json.loads((POWERBI / "Mexico-Inflation-Tracker.pbip").read_text(encoding="utf-8"))
        self.assertEqual(pbip["version"], "1.0")
        report_path = POWERBI / pbip["artifacts"][0]["report"]["path"]
        self.assertTrue((report_path / "definition.pbir").is_file())
        definition = json.loads((report_path / "definition.pbir").read_text(encoding="utf-8"))
        model_path = (report_path / definition["datasetReference"]["byPath"]["path"]).resolve()
        self.assertEqual(model_path, MODEL.resolve())
        self.assertTrue((MODEL / "definition.pbism").is_file())

    def test_pbir_json_files_are_valid(self):
        json_files = list(REPORT.rglob("*.json")) + [REPORT / "definition.pbir"]
        self.assertGreaterEqual(len(json_files), 7)
        for path in json_files:
            with self.subTest(path=path.relative_to(ROOT)):
                json.loads(path.read_text(encoding="utf-8"))

    def test_report_has_three_kpis_and_monthly_trend(self):
        page = REPORT / "definition/pages/a9f4b3c7d2e1468f9a01"
        visuals = sorted((page / "visuals").glob("*/visual.json"))
        parsed = [json.loads(path.read_text(encoding="utf-8")) for path in visuals]
        types = [item["visual"]["visualType"] for item in parsed]
        self.assertEqual(types.count("cardVisual"), 3)
        self.assertIn("lineChart", types)
        self.assertEqual(len(types), 4)

    def test_semantic_model_contract(self):
        fact = (MODEL / "definition/tables/Fact_INPC.tmdl").read_text(encoding="utf-8")
        dim = (MODEL / "definition/tables/Dim_Date.tmdl").read_text(encoding="utf-8")
        relationships = (MODEL / "definition/relationships.tmdl").read_text(encoding="utf-8")
        for measure in ("INPC_Actual", "INPC_AñoAnterior", "Inflacion_YoY", "INPC_Promedio3M"):
            self.assertIn(f"measure {measure}", fact)
        self.assertIn("column Date", dim)
        self.assertIn("column YearMonth", dim)
        self.assertIn("sortByColumn: MonthNumber", dim)
        self.assertIn("fromColumn: Fact_INPC.Fecha", relationships)
        self.assertIn("toColumn: Dim_Date.Date", relationships)

    def test_token_is_parameterized_not_committed(self):
        expressions = (MODEL / "definition/expressions.tmdl").read_text(encoding="utf-8")
        fact = (MODEL / "definition/tables/Fact_INPC.tmdl").read_text(encoding="utf-8")
        self.assertIn("BanxicoToken", expressions)
        self.assertIn("IsParameterQuery=true", expressions)
        self.assertIn('Headers = [#"Bmx-Token" = BanxicoToken', fact)
        self.assertNotRegex(expressions, r"(?i)(bearer\\s+|[a-f0-9]{32,})")

    def test_data_refresh_contract_is_documented(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("BANXICO_TOKEN", readme)
        self.assertIn("Power BI Desktop", readme)
        self.assertIn("PBIX", readme)

if __name__ == "__main__":
    unittest.main(verbosity=2)
