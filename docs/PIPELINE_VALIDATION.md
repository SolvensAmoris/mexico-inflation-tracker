# Pipeline validation

The repository includes an offline regression suite. It uses synthetic fixtures only and never claims those fixtures are official INPC observations.

Run locally with:

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs the same checks on pushes, pull requests, and manual dispatch. The checks validate sorting, numeric normalization, duplicate-date rejection, the fact table, and the contiguous date dimension.

A live refresh is a separate operation requiring the owner's Banxico SIE API token. The token must remain outside Git history and be supplied as the `BANXICO_TOKEN` environment variable. No live API run or PBIX binary is claimed by the offline test suite.
