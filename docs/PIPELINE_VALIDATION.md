# Pipeline validation and live refresh

## Offline regression tests

Run:

    python -m unittest discover -s tests -v

The suite uses synthetic fixtures only. It checks ETL normalization, date ordering, duplicate rejection, non-finite values, and structural Power BI project contracts. Synthetic tests are not evidence of a live Banxico retrieval.

## Live Banxico refresh without a local terminal

The Refresh official INPC data workflow can be started from GitHub Actions and also runs monthly. One-time setup:

1. Open repository Settings.
2. Select Secrets and variables > Actions.
3. Create repository secret BANXICO_TOKEN.
4. Paste the Banxico SIE token and save.

Then open Actions > Refresh official INPC data > Run workflow. The token is injected as an environment secret and is not printed, committed, or included in artifacts. Successful runs upload Bronze, Silver, and Gold CSV outputs as a 90-day artifact.

A successful workflow verifies the Python API pipeline and CSV artifact. It does not refresh or validate the Power BI Desktop semantic model.

## Power BI Desktop handoff

1. Open powerbi/Mexico-Inflation-Tracker.pbip in Power BI Desktop.
2. Set the local BanxicoToken parameter in Power Query.
3. Configure Web source credentials/privacy level if prompted.
4. Refresh and inspect the semantic model and report.
5. Save as .pbix if a native binary is required.

PBIP/PBIR/TMDL are source-controlled project formats. The native PBIX binary must be serialized by Power BI Desktop.

## Security

Never commit the Banxico token, .env files, or credential-bearing logs. If a token is exposed, revoke it at the provider and create a replacement.
