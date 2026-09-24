# Southeast Asia countries for a later PXD campaign

Inventory only. These countries are **not** part of NordicSDRF: they are not in
`config.yml`, they do not appear on the README charts, and there are no
`lists/<country>/<city>.txt` manifests yet. Use this file when you start a
sibling campaign (same `build_manifest.py` path: keyword search, then keep only
records that confirm the country).

Scope: the 10 ASEAN members plus Timor-Leste. Suggested order is by likely
curated PXD count, not by geography.

**"PRIDE hits"** is `total_records` from the PRIDE Archive v2 full-text search
(`/pride/ws/archive/v2/search/projects?keyword=<term>`), queried 2026-09-24.
The search matches titles, descriptions and affiliation strings, so it both
over-counts (surnames, acronyms, other places) and under-counts (submitters who
wrote only the institute name). Whole SEA after a country filter is probably
~150–250 PXDs; Singapore alone is about one Swedish-city scale.

> **Known traps.** `Singapore` also matches sea-star studies. `NUS` is an
> acronym, not a place. `Laos` / `Lao` match unrelated papers (Spain/France
> affiliations, *Pongo*, snake venom). `Dili` is almost entirely the DILI
> (drug-induced liver injury) acronym. `Burma` is noise — search `Myanmar`.
> `Indonesia` previously returned a Korea deposit. Same rule as Uppsala: fetch
> `/pride/ws/archive/v2/projects/<PXD>` and require the SEA country in
> `countries` (or a submitter `country` / affiliation string) before screening.

## Country list

| Order | Country | Slug | Cities that matter | PRIDE hits (country name) | Later manifest |
|---:|---|---|---|---:|---|
| 1 | Singapore | `singapore` | Singapore (city-state) | 271 | `lists/singapore/singapore.txt` |
| 2 | Thailand | `thailand` | Bangkok (+ Chiang Mai, small) | 108 | `lists/thailand/bangkok.txt` |
| 3 | Malaysia | `malaysia` | Kuala Lumpur, Penang | 38 | `lists/malaysia/kuala_lumpur.txt`, `lists/malaysia/penang.txt` |
| 4 | Vietnam | `vietnam` | Hanoi, Ho Chi Minh City | 10 (`Viet Nam` 1) | `lists/vietnam/hanoi.txt` |
| 5 | Philippines | `philippines` | Manila / Quezon City | 9 | `lists/philippines/manila.txt` |
| 6 | Indonesia | `indonesia` | Jakarta, Bandung, Yogyakarta, Surabaya | 4 | `lists/indonesia/jakarta.txt` |
| 7 | Myanmar | `myanmar` | Yangon | 1 (`Burma` 18, ignore) | `lists/myanmar/yangon.txt` |
| 8 | Laos | `laos` | Vientiane | 10 (mostly false positives) | `lists/laos/vientiane.txt` |
| 9 | Cambodia | `cambodia` | Phnom Penh | 0 | not scoped |
| 10 | Brunei | `brunei` | Bandar Seri Begawan | 0 | not scoped |
| 11 | Timor-Leste | `timor_leste` | Dili | 0 (`Dili` 22 is DILI) | not scoped |

`Southeast Asia` / `South East Asia` / `ASEAN` as keywords are not useful
(11 / 2 / 0 hits, mixed archaeology and disease papers). Search city and
institution names, then filter on country.

## Singapore — first (city-state)

| City | Search terms | Key institutions / facilities | PRIDE hits | Notes |
|---|---|---|---:|---|
| Singapore | Singapore, "National University of Singapore", "Nanyang Technological University", A*STAR, IMCB, Duke-NUS | NUS; NTU; A*STAR (IMCB, GIS, BII, SIgN); Duke-NUS; NUH / SGH | 271 | Prefer the full university names. Bare `NUS` (143) is noisy. `Nanyang Technological` (72) is NTU Singapore, not Taiwan. `A*STAR` (216) overlaps heavily with `Singapore`. |

One manifest is enough: the country is the city.

## Thailand

| City | Search terms | Key institutions / facilities | PRIDE hits | Notes |
|---|---|---|---:|---|
| Bangkok | Bangkok, Mahidol, Chulalongkorn, Siriraj, Thailand | Mahidol University (Siriraj, Ramathibodi); Chulalongkorn University; BIOTEC / NSTDA | 108 country / 52 Bangkok / 34 Mahidol / 30 Chulalongkorn / 13 Siriraj | Real deposits (Mahidol clinical and kidney-stone series showed up in the sample). |
| Chiang Mai | "Chiang Mai" | Chiang Mai University | 1 | Optional extra term on the Bangkok run, not its own list unless the country filter keeps it. |

## Malaysia

| City | Search terms | Key institutions / facilities | PRIDE hits | Notes |
|---|---|---|---:|---|
| Kuala Lumpur | Malaysia, "Kuala Lumpur", "University of Malaya" | Universiti Malaya (UM); UKM; UPM | 38 country / 12 University of Malaya / 3 Kuala Lumpur | Bare `Malaya` (19) is broader than UM. |
| Penang | "Universiti Sains Malaysia", Penang | Universiti Sains Malaysia (USM) | 1 USM / 2 Penang | Do **not** search bare `USM` (Southern Mississippi and other expansions). Sample hit `PXD010171` is a real USM deposit. |

## Vietnam

| City | Search terms | Key institutions / facilities | PRIDE hits | Notes |
|---|---|---|---:|---|
| Hanoi | Vietnam, "Viet Nam", Hanoi | University of Science / VNU Hanoi; Oxford University Clinical Research Unit (OUCRU) also appears in Viet Nam records | 10 / 1 / 2 | Search both `Vietnam` and `Viet Nam`; PRIDE `countries` may use either. |
| Ho Chi Minh City | "Ho Chi Minh", Saigon | University of Medicine and Pharmacy HCMC; OUCRU HCMC | 0 for "Ho Chi Minh" / "Ho Chi Minh City" | Likely captured by the Vietnam country term; do not expect a second list. |

## Philippines

| City | Search terms | Key institutions / facilities | PRIDE hits | Notes |
|---|---|---|---:|---|
| Manila | Philippines, Manila, "University of the Philippines" | University of the Philippines (Manila / Diliman); St. Luke's | 9 / 3 / 2 | Sample hits include Filipino NSCLC proteomes (`PXD050598`, `PXD027710`). `Quezon` alone is 0. |

## Indonesia

| City | Search terms | Key institutions / facilities | PRIDE hits | Notes |
|---|---|---|---:|---|
| Jakarta | Indonesia, Jakarta | University of Indonesia; Eijkman / BRIN | 4 / 0 | Country term only; city names currently return nothing. Confirm `countries` — at least one earlier Indonesia keyword hit was Korea. |
| Bandung | Bandung | Institut Teknologi Bandung (ITB) | 0 | |
| Yogyakarta | Yogyakarta | Universitas Gadjah Mada (UGM) | 0 | |
| Surabaya | Surabaya | Universitas Airlangga | 0 | |

Treat as one short country manifest unless the filter actually splits by city.

## Myanmar, Laos, Cambodia, Brunei, Timor-Leste

| Country | Search terms | PRIDE hits | Trap |
|---|---|---:|---|
| Myanmar | Myanmar | 1 | Do not search `Burma` (18 unrelated hits). `Yangon` is 0. |
| Laos | Laos | 10 | Almost all false positives; `Lao` (43) is worse. `Vientiane` is 0. |
| Cambodia | Cambodia | 0 | `Phnom Penh` is 0. |
| Brunei | Brunei | 0 | `Brunei Darussalam` and `Bandar Seri Begawan` are 0. |
| Timor-Leste | Timor-Leste, "East Timor" | 0 / 0 | Never search `Dili` (22 hits, DILI). |

Worth a country-filter pass on Myanmar and Laos only after Singapore / Thailand / Malaysia. The last three can wait until those manifests exist.

## Building later

`scripts/build_manifest.py` currently reads search terms from `config.yml`. When
you start the campaign, add the country/city block there (or copy this file
into a sibling repo) and run:

```bash
python scripts/build_manifest.py singapore singapore --dry-run
python scripts/build_manifest.py thailand bangkok --dry-run
python scripts/build_manifest.py malaysia kuala_lumpur --dry-run
```

Keep an accession only when the PRIDE record itself confirms the SEA country.
Do not add these countries to NordicSDRF `config.yml` until you actually want
them on the Nordic status charts.
