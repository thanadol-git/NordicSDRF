# South Asia countries for a later PXD campaign

Inventory only. These countries are **not** part of NordicSDRF: they are not in
`config.yml`, they do not appear on the README charts, and there are no
`lists/<country>/<city>.txt` manifests yet. Use this file when you start a
sibling campaign (same `build_manifest.py` path: keyword search, then keep only
records that confirm the country).

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

| Order | Country | Slug | Cities that matter | PRIDE hits (country name) | Later manifest |
|---:|---|---|---|---:|---|
| 1 | India | `india` | Bengaluru, Mumbai, Delhi / New Delhi, Hyderabad, Pune, Kolkata, Chennai, (+ others) | 907 | `lists/india/<city>.txt` (several) |
| 2 | Pakistan | `pakistan` | Lahore, Karachi, Islamabad | 15 | `lists/pakistan/lahore.txt` |
| 3 | Nepal | `nepal` | Kathmandu | 12 | `lists/nepal/kathmandu.txt` |
| 4 | Sri Lanka | `sri_lanka` | Colombo | 10 | `lists/sri_lanka/colombo.txt` |
| 5 | Bangladesh | `bangladesh` | Dhaka | 3 | `lists/bangladesh/dhaka.txt` |
| 6 | Bhutan | `bhutan` | Thimphu | 0 | not scoped |
| 7 | Maldives | `maldives` | Malé | 0 | not scoped |
| 8 | Afghanistan | `afghanistan` | Kabul | 0 (`Kabul` 1) | not scoped |

`South Asia` / `Indian subcontinent` as keywords are not useful (5 / 6 hits).
Search city and institution names, then filter on country.

## India — first (by far the largest)

India alone is larger than the whole Nordic campaign's raw country keywords.
Plan several city manifests; do not treat "India" as one list.

| City | Search terms | Key institutions / facilities | PRIDE hits | Notes |
|---|---|---|---:|---|
| Bengaluru | Bangalore, Bengaluru, IISc, NCBS | IISc; NCBS; inStem; IIIT-B | 82 / 13 / 11 / 3 | Prefer `Bangalore` + institute terms; confirm `countries: [India]`. |
| Mumbai | Mumbai, Bombay, "IIT Bombay", ACTREC, TIFR | IIT Bombay; ACTREC / Tata Memorial; TIFR | 37 / 41 / 26 / 6 / 3 | `Bombay` still appears in older affiliations. |
| Delhi / New Delhi | Delhi, "New Delhi", "IIT Delhi", IGIB | AIIMS; IIT Delhi; CSIR-IGIB; JNU | 89 / 76 / 0 / 2 | Bare `Delhi` and `New Delhi` are noisy; institute terms are sparse in PRIDE text. |
| Hyderabad | Hyderabad, CDFD, CCMB | CDFD; CCMB; University of Hyderabad; IIIT-H | 58 / 17 | `Hyderabad` also matches Pakistan / India place ambiguity — country filter required. |
| Pune | Pune, NCCS | NCCS; IISER Pune; NCL | 32 / 4 | |
| Kolkata | Kolkata, Calcutta, "IIT Kharagpur" | IICB; Bose Institute; IIT Kharagpur (nearby) | 26 / 2 / 0 | |
| Chennai | Chennai, Madras, "IIT Madras" | IIT Madras; Cancer Institute (WIA) | 10 / 2 / 0 | |
| Other | Kanpur, Lucknow, Chandigarh, Bhopal, Thiruvananthapuram, Ahmedabad | IITs / medical colleges | 5 / 17 / 9 / 3 / 4 / 1 | Optional add-ons after the metros are filtered. |

Suggested India start order: Bengaluru → Mumbai → Hyderabad → Delhi → Pune.

## Pakistan

| City | Search terms | Key institutions / facilities | PRIDE hits | Notes |
|---|---|---|---:|---|
| Lahore | Pakistan, Lahore | University of the Punjab; LUMS; UVAS | 15 country / 12 Lahore | Country term is the useful seed. |
| Karachi | Karachi, "Aga Khan University" | Aga Khan University; University of Karachi | 2 / 0 | |
| Islamabad | Islamabad, Quaid-i-Azam | Quaid-i-Azam University; NUST | 1 / 0 | |

One short country manifest is enough unless the filter splits cleanly by city.

## Nepal

| City | Search terms | Key institutions / facilities | PRIDE hits | Notes |
|---|---|---|---:|---|
| Kathmandu | Nepal, Kathmandu, Tribhuvan | Tribhuvan University; research hospitals | 12 / 0 / 0 | Country term only so far; city/institute keywords are empty. |

## Sri Lanka

| City | Search terms | Key institutions / facilities | PRIDE hits | Notes |
|---|---|---|---:|---|
| Colombo | "Sri Lanka", Colombo, Peradeniya | University of Colombo; University of Peradeniya | 10 / 34 / 0 | `Colombo` over-counts — always require Sri Lanka in the record. |

## Bangladesh

| City | Search terms | Key institutions / facilities | PRIDE hits | Notes |
|---|---|---|---:|---|
| Dhaka | Bangladesh, Dhaka | University of Dhaka; icddr,b | 3 / 4 / 0 | Tiny; one country-level pass is enough. |

## Bhutan, Maldives, Afghanistan

| Country | Search terms | PRIDE hits | Trap |
|---|---|---:|---|
| Bhutan | Bhutan, Thimphu | 0 / 0 | Skip until India / Pakistan manifests exist. |
| Maldives | Maldives, Malé, "Male Maldives" | 0 / 0 / 0 | Skip. |
| Afghanistan | Afghanistan, Kabul | 0 / 1 | Skip; `Kabul` alone is not evidence. |

## Building later

`scripts/build_manifest.py` currently reads search terms from `config.yml`. When
you start the campaign, add the country/city block there (or copy this file
into a sibling repo) and run:

```bash
python scripts/build_manifest.py india bangalore --dry-run
python scripts/build_manifest.py india mumbai --dry-run
python scripts/build_manifest.py pakistan lahore --dry-run
python scripts/build_manifest.py sri_lanka colombo --dry-run
```

Keep an accession only when the PRIDE record itself confirms the South Asian
country. Do not add these countries to NordicSDRF `config.yml` until you
actually want them on the Nordic status charts.
