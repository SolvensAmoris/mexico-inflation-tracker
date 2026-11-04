# Mexico Inflation Tracker | INPC - Banxico / INEGI

> WE DON'T NEED MORE EXPLANATIONS. WE NEED EVIDENCE.

Reproducible monthly INPC pipeline and Power BI project.

## Data source
- Banxico SIE cuadro CP154: Principales índices mensuales.
- Series SP1: general monthly INPC index.
- Banxico SIE REST API; token passed only in the `Bmx-Token` HTTP header.
- INEGI has held the exclusive legal authority to prepare and publish national price indices since July 2011; Banxico SIE distributes the series.

## Pipeline
1. **Bronze:** `notebooks/01_Bronze_Ingestion.py` downloads SP1 into `data/bronze/inpc.csv`.
2. **Silver:** `notebooks/02_Silver_Transformation.py` validates dates, positive numeric values, and uniqueness.
3. **Gold:** `notebooks/03_Gold_Aggregation.py` creates `Fact_INPC` and contiguous `Dim_Date` CSV outputs.
4. **Power BI:** `powerbi/Mexico-Inflation-Tracker.pbip` contains the semantic model, three KPI cards, a monthly trend chart, and the StarkCore theme.

## Automated validation and refresh
- Offline regression tests run through GitHub Actions on pushes and pull requests. They use synthetic fixtures, never fabricated official data.
- The **Refresh official INPC data** workflow can be run from the GitHub Actions tab or runs monthly. Add the repository secret `BANXICO_TOKEN` once under **Settings > Secrets and variables > Actions**. The workflow uploads Bronze, Silver, and Gold CSVs as a 90-day artifact.
- See [pipeline validation](docs/PIPELINE_VALIDATION.md) for the no-terminal setup.

## Power BI
Open [the PBIP project](powerbi/Mexico-Inflation-Tracker.pbip) in Power BI Desktop. Configure the `BanxicoToken` parameter, refresh, and use **File > Save as > Power BI Desktop (.pbix)**. PBIP is source text; the native PBIX binary can only be produced by Power BI Desktop.

## Evidence and limits
The previous `data/raw/CP154.csv` contained an HTML page, not CSV observations. It was removed rather than treated as data. No INPC values are fabricated. A live refresh is only verified when the live workflow completes successfully. A native PBIX is not included in this repository.
