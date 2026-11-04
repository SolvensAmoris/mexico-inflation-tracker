<div align="center">

# Mexico Inflation Tracker
### Mexico's monthly consumer-price index, made reproducible.

**Banxico SIE · INEGI INPC · Python ETL · Power BI · StarkCore**

[![Pipeline CI](https://github.com/SolvensAmoris/mexico-inflation-tracker/actions/workflows/pipeline-ci.yml/badge.svg?branch=main)](https://github.com/SolvensAmoris/mexico-inflation-tracker/actions/workflows/pipeline-ci.yml)
[![Banxico refresh](https://github.com/SolvensAmoris/mexico-inflation-tracker/actions/workflows/refresh-inpc.yml/badge.svg?branch=main)](https://github.com/SolvensAmoris/mexico-inflation-tracker/actions/workflows/refresh-inpc.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Power BI Project](https://img.shields.io/badge/Power%20BI-PBIP%20%7C%20PBIR-F2C811?logo=powerbi&logoColor=111111)](https://learn.microsoft.com/power-bi/developer/projects/projects-overview)
[![Data source](https://img.shields.io/badge/data-Banxico%20SIE%20SP1-0B6E4F)](https://www.banxico.org.mx/SieAPIRest/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Author](https://img.shields.io/badge/author-Luis%20Alberto%20Burciaga%20Miker-111111)](mailto:Luis.albm77@gmail.com)
[![Organization](https://img.shields.io/badge/organization-StarkCore%20Labs-D4AF37)](https://github.com/SolvensAmoris)

**WE DON'T NEED MORE EXPLANATIONS. WE NEED EVIDENCE.**

</div>

---

A reproducible data pipeline and Power BI project for Mexico's **Índice Nacional de Precios al Consumidor (INPC)**. The repository separates official-source retrieval, deterministic transformation, analytical modeling, and report presentation so each layer can be inspected independently.

## At a glance

| Layer | Implementation | Output |
|---|---|---|
| Bronze | Banxico SIE REST API, series SP1 | Raw monthly observations |
| Silver | Date, numeric, uniqueness and ordering checks | Normalized observations |
| Gold | Fact and continuous calendar generation | Power BI-ready CSV tables |
| Semantic model | TMDL star schema and DAX | Measures and date relationship |
| Report | PBIR project format | KPI cards and monthly trend |

## Data provenance

- Provider: Banco de México, Sistema de Información Económica (SIE).
- Series: SP1, monthly general INPC.
- Reference table: CP154, Principales índices mensuales.
- INEGI is responsible for calculating and publishing the national price index; Banxico SIE provides the series through its API.
- API authentication uses the Bmx-Token HTTP header.

The pipeline preserves source observations and rejects invalid or duplicate dates rather than silently overwriting them. It does not invent missing monthly values.

## Architecture

Banxico SIE SP1 → Bronze ingestion → Silver validation → Gold aggregation → Power BI semantic model (TMDL) → Power BI report (PBIR).

## Power BI model

- Fact_INPC: monthly index observations, one row per observation date.
- Dim_Date: continuous calendar dimension, one row per calendar day.
- Relationship: Dim_Date[Date] (one) → Fact_INPC[Fecha] (many), active.

| Measure | Meaning |
|---|---|
| INPC_Actual | Latest available index within current date filter context |
| INPC_AñoAnterior | Comparable index for the prior year |
| Inflacion_YoY | Year-over-year percentage change |
| INPC_Promedio3M | Mean of the latest three available monthly observations |

The PBIR report defines three KPI cards and a monthly INPC line chart, styled with the StarkCore black-and-gold theme.

## Run the pipeline

Requirements: Python 3.12+ and a Banxico SIE API token.

    export BANXICO_TOKEN="YOUR_TOKEN"
    python notebooks/01_Bronze_Ingestion.py
    python notebooks/02_Silver_Transformation.py
    python notebooks/03_Gold_Aggregation.py
    python -m unittest discover -s tests -v

Never commit the token, .env files, or credential-bearing logs.

## Automated refresh without a local terminal

1. Add a repository secret named BANXICO_TOKEN under Settings → Secrets and variables → Actions.
2. Open [Actions → Refresh official INPC data](https://github.com/SolvensAmoris/mexico-inflation-tracker/actions/workflows/refresh-inpc.yml).
3. Select Run workflow.
4. Download the generated Bronze/Silver/Gold CSV artifact from the completed run.

The workflow also runs monthly. Artifacts are retained for 90 days. A successful GitHub Actions run verifies the Python API pipeline and CSV artifact, not a Power BI Desktop refresh.

## Open the Power BI project

1. Open powerbi/Mexico-Inflation-Tracker.pbip in Power BI Desktop.
2. In Transform data → Manage parameters, set BanxicoToken locally. Do not commit it.
3. Configure Web data source credentials/privacy level if prompted.
4. In Model view, mark Dim_Date[Date] as the date table (Table tools → Mark as date table → Date). The prior-year measure uses classic SAMEPERIODLASTYEAR time intelligence.
5. Refresh and inspect the model/report.
6. Save the project, then use File → Save as → Power BI Desktop (.pbix) to create the native binary deliverable.

**Important:** PBIP is the source-controlled project format. This repository does not claim to contain a generated or Desktop-validated PBIX.

## Quality gates

    python -m compileall -q notebooks tests
    python -m unittest discover -s tests -v

CI checks ETL regression tests and PBIP entrypoint, PBIR JSON syntax, report visuals, TMDL measures, date dimension, relationship and parameterized credential contract.

## Project layout

- .github/workflows/: CI and scheduled/manual refresh
- data/: Bronze, Silver and Gold outputs
- docs/: operational and validation notes
- notebooks/: Python ETL stages
- powerbi/: PBIP, PBIR, TMDL, theme and DAX reference
- tests/: offline regression and project-structure tests

## Documentation

- [Pipeline validation and refresh guide](docs/PIPELINE_VALIDATION.md)
- [Power BI setup](powerbi/README.md)
- [Banxico SIE API](https://www.banxico.org.mx/SieAPIRest/)
- [Power BI Projects (PBIP)](https://learn.microsoft.com/power-bi/developer/projects/projects-overview)
- [Power BI PBIR report format](https://learn.microsoft.com/power-bi/developer/projects/projects-report)
- [Power Query Web.Contents](https://learn.microsoft.com/powerquery-m/web-contents)

## License

No license file is currently published. Until a license is added, reuse, redistribution and modification are not granted by an open-source license.
