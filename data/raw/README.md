# Raw source status

The former `CP154.csv` was not a CSV export. It contained the HTML page for the Banxico SIE cuadro CP154 and has been removed rather than preserved under a misleading extension.

The reproducible Bronze ingestion requests the monthly INPC series from the Banxico SIE REST API:
- SIE cuadro: CP154 (Principales índices mensuales)
- Series identifier: SP1 (general monthly INPC index)
- API route: `/service/v1/series/SP1/datos/{start}/{end}`
- Authentication: API token in the `Bmx-Token` header

Set `BANXICO_TOKEN` locally and run `python notebooks/01_Bronze_Ingestion.py`. Never commit the token.
