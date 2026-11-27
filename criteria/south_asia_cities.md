# South Asia countries for the PXD campaign

Narrative reference for South Asia cities tracked in `config.yml` with
`region: south_asia`. The region overview is `status/plots/south_asia.svg`
(one horizontal bar per country, same style as Nordic / SEA). Per-country city
charts are `status/plots/<country>.svg` with pages under `status/markdowns/`.
Manifests appear under `lists/<country>/<city>.txt` when scoped; use the same
`build_manifest.py` path (keyword search, then keep only records that confirm
the country).

Scope: the eight SAARC members (India, Pakistan, Bangladesh, Sri Lanka, Nepal,
Bhutan, Maldives, Afghanistan). Suggested order is by likely curated PXD count,
not by geography.

**"PRIDE hits"** is `total_records` from the PRIDE Archive v2 full-text search
(`/pride/ws/archive/v2/search/projects?keyword=<term>`), queried 2026-11-19.
The search matches titles, descriptions and affiliation strings, so it both
over-counts (surnames, other places, diaspora affiliations) and under-counts
(submitters who wrote only the institute name). After a country filter, expect
India to dominate by a large margin; the rest of SAARC together is closer to a
small Nordic country.

> **Known traps.** `India` and city names (`Delhi`, `Bangalore`, `Hyderabad`,
> `Bombay`) over-count heavily — Indian researchers abroad, common place-name
> collisions, and title keywords. `Colombo` is not only Sri Lanka. Prefer
> institute strings (`IISc`, `IIT Bombay`, `NCBS`, `CDFD`) plus a hard
> `countries: [India]` (or equivalent) check. Same rule as Uppsala: fetch
> `/pride/ws/archive/v2/projects/<PXD>` and require the South Asian country in
> `countries` (or a submitter `country` / affiliation string) before screening.

## Country list

| Order | Country | Slug | Cities that matter | PRIDE hits (country name) | Manifest |
|---:|---|---|---|---:|---|
| 1 | India | `india` | Bengaluru, Mumbai, Delhi, Hyderabad, Pune, Kolkata, Chennai | 907 | `lists/india/<city>.txt` |
| 2 | Pakistan | `pakistan` | Lahore, Karachi, Islamabad | 15 | `lists/pakistan/<city>.txt` |
| 3 | Nepal | `nepal` | Kathmandu | 12 | `lists/nepal/kathmandu.txt` |
| 4 | Sri Lanka | `sri_lanka` | Colombo | 10 | `lists/sri_lanka/colombo.txt` |
| 5 | Bangladesh | `bangladesh` | Dhaka | 3 | `lists/bangladesh/dhaka.txt` |
| 6 | Bhutan | `bhutan` | Thimphu | 0 | `lists/bhutan/thimphu.txt` (empty) |
| 7 | Maldives | `maldives` | Malé | 0 | `lists/maldives/male.txt` (empty) |
| 8 | Afghanistan | `afghanistan` | Kabul | 0 | `lists/afghanistan/kabul.txt` (empty) |

`South Asia` / `Indian subcontinent` as keywords are not useful (5 / 6 hits).
Search city and institution names, then filter on country.

## India — first (by far the largest)

| City | Search terms | Key institutions / facilities | PRIDE hits | Notes |
|---|---|---|---:|---|
| Bengaluru | Bangalore, Bengaluru, IISc, NCBS | IISc; NCBS; inStem; IIIT-B | 82 / 13 / 11 / 3 | Prefer `Bangalore` + institute terms; confirm `countries: [India]`. |
| Mumbai | Mumbai, Bombay, "IIT Bombay", ACTREC, TIFR | IIT Bombay; ACTREC / Tata Memorial; TIFR | 37 / 41 / 26 / 6 / 3 | `Bombay` still appears in older affiliations. |
| Delhi | Delhi, "New Delhi", "IIT Delhi", IGIB | AIIMS; IIT Delhi; CSIR-IGIB; JNU | 89 / 76 / 0 / 2 | Bare `Delhi` is noisy. |
| Hyderabad | Hyderabad, CDFD, CCMB | CDFD; CCMB; University of Hyderabad | 58 / 17 | Country filter required. |
| Pune | Pune, NCCS | NCCS; IISER Pune; NCL | 32 / 4 | |
| Kolkata | Kolkata, Calcutta, "IIT Kharagpur" | IICB; Bose Institute; IIT Kharagpur | 26 / 2 / 0 | |
| Chennai | Chennai, Madras, "IIT Madras" | IIT Madras; Cancer Institute (WIA) | 10 / 2 / 0 | |

Suggested India start order: Bengaluru → Mumbai → Hyderabad → Delhi → Pune.

## Building manifests

```bash
python scripts/build_manifest.py india bengaluru
python scripts/build_manifest.py pakistan lahore
python scripts/build_manifest.py sri_lanka colombo
python scripts/update_status.py --no-pride
```

Keep an accession only when the PRIDE record itself confirms the South Asian
country. Refresh `status/plots/south_asia.svg` with `python scripts/update_status.py --no-pride`.
