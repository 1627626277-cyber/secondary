# Reference DOI/URL Live-Link Audit

Date: 2026-05-01

Scope:

- Checked DOI and URL targets in the current Vancouver reference list.
- `access_limited` means the target responded but blocked automated access, usually with 403, 405, 429, or authentication behavior.
- `browser_verified` means the automated Python check failed locally, but the same URL opened successfully through browser verification on 2026-05-01.

## Summary

- ok: 10
- browser_verified: 6
- access_limited: 9
- failed: 0
- not_applicable: 1

## Results

| Ref | Type | Status | HTTP | Target | Note |
|---:|---|---|---|---|---|
| 1 | doi | ok | 200 | https://doi.org/10.1038/s41588-024-01853-0 |  |
| 2 | doi | ok | 200 | https://doi.org/10.1038/s41467-019-11680-1 |  |
| 3 | doi | access_limited | 403 | https://doi.org/10.1200/JCO.2015.61.2267 | HTTPError |
| 4 | doi | ok | 200 | https://doi.org/10.1016/S1470-2045(14)70442-5 |  |
| 5 | doi | ok | 200 | https://doi.org/10.1038/nature09837 |  |
| 6 | doi | access_limited | 403 | https://doi.org/10.1002/ajh.26590 | HTTPError |
| 7 | doi | access_limited | 403 | https://doi.org/10.1200/JCO.2005.04.242 | HTTPError |
| 8 | doi | access_limited | 403 | https://doi.org/10.1182/blood-2005-11-013458 | HTTPError |
| 9 | doi | access_limited | 403 | https://doi.org/10.1182/blood-2006-03-009910 | HTTPError |
| 10 | doi | access_limited | 403 | https://doi.org/10.1182/blood.2025028896 | HTTPError |
| 11 | doi | ok | 200 | https://doi.org/10.1186/s12967-025-07098-7 |  |
| 12 | doi | access_limited | 403 | https://doi.org/10.1093/jnci/dji237 | HTTPError |
| 13 | doi | access_limited | 403 | https://doi.org/10.1093/nar/gks1193 | HTTPError |
| 14 | doi | ok | 200 | https://doi.org/10.1038/s41467-021-21254-9 |  |
| 15 | url | browser_verified |  | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE269875 | Python urllib reported TLS EOF, but the page opened successfully in browser verification on 2026-05-01. |
| 16 | url | browser_verified |  | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299193 | Python urllib reported TLS EOF, but the page opened successfully in browser verification on 2026-05-01. |
| 17 | url | browser_verified |  | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE271107 | Python urllib reported TLS EOF, but the page opened successfully in browser verification on 2026-05-01. |
| 18 | url | browser_verified |  | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE24080 | Python urllib reported TLS EOF, but the page opened successfully in browser verification on 2026-05-01. |
| 19 | url | browser_verified |  | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE2658 | Python urllib reported TLS EOF, but the page opened successfully in browser verification on 2026-05-01. |
| 20 | url | browser_verified |  | https://gdc.cancer.gov/about-gdc/contributed-genomic-data-cancer-research/foundation-medicine/multiple-myeloma-research-foundation-mmrf | Python urllib reported TLS EOF, but the page opened successfully in browser verification on 2026-05-01. |
| 21 | doi | ok | 200 | https://doi.org/10.1186/s13059-017-1382-0 |  |
| 22 | url | ok | 200 | https://www.statsmodels.org/ |  |
| 23 | doi | ok | 200 | https://doi.org/10.1038/nbt.1665 |  |
| 24 | doi | ok | 200 | https://doi.org/10.1371/journal.pone.0008250 |  |
| 25 | none | not_applicable |  |  | No DOI or URL present in reference entry. |
| 26 | doi | access_limited | 403 | https://doi.org/10.1111/j.2517-6161.1995.tb02031.x | HTTPError |
