# Middle East countries for a later PXD campaign

Inventory only. These countries are **not** part of NordicSDRF: they are not in
`config.yml`, they do not appear on the README charts, and there are no
`lists/<country>/<city>.txt` manifests yet. Use this file when you start a
sibling campaign (same `build_manifest.py` path: keyword search, then keep only
records that confirm the country).

Scope: Levant, Gulf, Iran, Egypt, Turkey, and Cyprus (common “Middle East /
West Asia” MS-proteomics depositors). North Africa beyond Egypt is out of
scope here. Suggested order is by likely curated PXD count, not by geography.

**"PRIDE hits"** is `total_records` from the PRIDE Archive v2 full-text search
(`/pride/ws/archive/v2/search/projects?keyword=<term>`), queried 2026-11-19.
The search matches titles, descriptions and affiliation strings, so it both
over-counts (surnames, other places, diaspora affiliations) and under-counts
(submitters who wrote only the institute name). After a country filter, Israel
is the clear first campaign; Saudi Arabia / Turkey / Egypt / UAE / Iran are the
next tier; most of the Gulf and Levant are small.

> **Known traps.** `Jordan` is a common surname (66 raw hits — treat as noisy).
> `AUB` (188) is useless as a bare acronym. `Syria` / `Giza` / `Cyprus` need a
> hard country check. Prefer institute strings (`Weizmann`, `Technion`,
> `KAUST`, `Hebrew University`) plus `countries` confirmation. Same rule as
> Uppsala: fetch `/pride/ws/archive/v2/projects/<PXD>` and require the Middle
> Eastern country in `countries` (or a submitter `country` / affiliation
> string) before screening.

## Country list

| Order | Country | Slug | Cities that matter | PRIDE hits (country name) | Later manifest |
|---:|---|---|---|---:|---|
| 1 | Israel | `israel` | Rehovot, Haifa, Tel Aviv, Jerusalem | 522 | `lists/israel/<city>.txt` (several) |
| 2 | Turkey | `turkey` | Istanbul, Ankara, Izmir | 65 (`Türkiye` 3) | `lists/turkey/istanbul.txt` |
| 3 | Saudi Arabia | `saudi_arabia` | Thuwal (KAUST), Riyadh, Jeddah | 50 | `lists/saudi_arabia/kaust.txt` |
| 4 | Egypt | `egypt` | Cairo, Alexandria, Giza | 49 | `lists/egypt/cairo.txt` |
| 5 | Iran | `iran` | Tehran, Tabriz | 30 | `lists/iran/tehran.txt` |
| 6 | United Arab Emirates | `uae` | Sharjah, Dubai, Abu Dhabi | 21 (`UAE` 6) | `lists/uae/sharjah.txt` |
| 7 | Qatar | `qatar` | Doha | 17 | `lists/qatar/doha.txt` |
| 8 | Lebanon | `lebanon` | Beirut | 10 | `lists/lebanon/beirut.txt` |
| 9 | Cyprus | `cyprus` | Nicosia | 9 | `lists/cyprus/nicosia.txt` |
| 10 | Kuwait | `kuwait` | Kuwait City | 8 | `lists/kuwait/kuwait_city.txt` |
| 11 | Jordan | `jordan` | Amman | 66 (noisy surname) | only after country filter |
| 12 | Syria | `syria` | Damascus | 18 (likely noisy) | only after country filter |
| 13 | Iraq | `iraq` | Baghdad | 3 | not scoped |
| 14 | Oman | `oman` | Muscat | 1 | not scoped |
| 15 | Yemen | `yemen` | Sana'a | 1 | not scoped |
| 16 | Bahrain | `bahrain` | Manama | 0 | not scoped |
| 17 | Palestine | `palestine` | — | 0 | not scoped |

`Middle East` as a keyword is not useful (14 mixed hits). Search city and
institution names, then filter on country. Search both `Turkey` and `Türkiye`;
PRIDE `countries` may use either.

## Israel — first (largest by a wide margin)

Israel is roughly Singapore-scale or larger in raw hits, with dense Weizmann /
Technion / university output. Plan multiple city (or institute) manifests.

| City | Search terms | Key institutions / facilities | PRIDE hits | Notes |
|---|---|---|---:|---|
| Rehovot | Rehovot, Weizmann | Weizmann Institute of Science | 80 / 160 | `Weizmann` is the strongest Israel seed; still confirm country. |
| Haifa | Haifa, Technion | Technion – Israel Institute of Technology | 74 / 101 | |
| Tel Aviv | "Tel Aviv", "Bar-Ilan", "Sheba Medical" | Tel Aviv University; Bar-Ilan; Sheba Medical Center | 73 / 13 / 6 | |
| Jerusalem | Jerusalem, "Hebrew University" | Hebrew University of Jerusalem; Hadassah | 72 / 75 | |
| Beer Sheva | Ben-Gurion | Ben-Gurion University of the Negev | 12 | Optional after the four metros. |

Suggested Israel start: Weizmann / Rehovot → Technion / Haifa → Hebrew University / Jerusalem → Tel Aviv.

## Turkey

| City | Search terms | Key institutions / facilities | PRIDE hits | Notes |
|---|---|---|---:|---|
| Istanbul | Turkey, Türkiye, Istanbul, Bogazici, Boğaziçi | Boğaziçi / Bogazici; Istanbul University; Koç; Sabancı | 65 / 3 / 12 / 0 / 1 | Prefer `Turkey` + city; `Türkiye` alone is sparse. |
| Ankara | Ankara, Hacettepe, METU, Bilkent | Hacettepe; METU; Bilkent | 6 / 2 / 7 / 0 | |
| Izmir | Izmir, İzmir | Ege University; Dokuz Eylül | 4 / 4 | |

## Saudi Arabia

| City | Search terms | Key institutions / facilities | PRIDE hits | Notes |
|---|---|---|---:|---|
| Thuwal / KAUST | "Saudi Arabia", KAUST | King Abdullah University of Science and Technology | 50 / 22 | KAUST dominates the Saudi signal. |
| Riyadh | Riyadh, "King Saud University" | King Saud University; KFSHRC | 5 / 0 | |
| Jeddah | Jeddah, "King Abdulaziz" | King Abdulaziz University | 1 / 1 | |

One KAUST-centred manifest plus a residual `Saudi Arabia` pass is enough at first.

## Egypt

| City | Search terms | Key institutions / facilities | PRIDE hits | Notes |
|---|---|---|---:|---|
| Cairo | Egypt, Cairo, "Ain Shams" | Cairo University; Ain Shams; NRC | 49 / 21 / 0 | Country term is the useful seed. |
| Alexandria | Alexandria | Alexandria University | 10 | Confirm Egypt — place-name collisions exist. |
| Giza | Giza | Cairo University / Giza campus | 13 | Noisy; do not use without country filter. |

## Iran

| City | Search terms | Key institutions / facilities | PRIDE hits | Notes |
|---|---|---|---:|---|
| Tehran | Iran, Tehran, "University of Tehran", "Sharif University" | University of Tehran; Sharif; Pasteur Institute | 30 / 18 / 1 / 0 | |
| Tabriz | Tabriz | University of Tabriz | 4 | |
| Isfahan / Shiraz | Isfahan, Shiraz | local universities | 1 / 1 | Optional. |

## United Arab Emirates, Qatar, Kuwait, Bahrain, Oman

| Country | Search terms | PRIDE hits | Notes |
|---|---|---:|---|
| UAE | "United Arab Emirates", UAE, Sharjah, Dubai, "Abu Dhabi" | 21 / 6 / 14 / 5 / 3 | Prefer the full country name; `Sharjah` is the strongest city term. |
| Qatar | Qatar, Doha, "Qatar University" | 17 / 8 / 2 | |
| Kuwait | Kuwait, "Kuwait University", "Kuwait City" | 8 / 6 / 1 | |
| Bahrain | Bahrain, Manama | 0 / 0 | Skip. |
| Oman | Oman, Muscat, "Sultan Qaboos" | 1 / 3 / 0 | Skip or tiny residual. |

## Lebanon, Jordan, Syria, Cyprus, Iraq, Yemen, Palestine

| Country | Search terms | PRIDE hits | Trap |
|---|---|---:|---|
| Lebanon | Lebanon, Beirut, "American University of Beirut" | 10 / 1 / 0 | Never search bare `AUB` (188 unrelated). |
| Jordan | Jordan, Amman | 66 / 16 | `Jordan` surname noise — require `countries` / affiliation. |
| Syria | Syria, Damascus | 18 / 0 | Likely noisy; country filter before any list. |
| Cyprus | Cyprus, Nicosia | 9 / 11 | Confirm country; Nicosia can collide. |
| Iraq | Iraq, Baghdad | 3 / 1 | Tiny. |
| Yemen | Yemen, Sanaa, "Sana'a" | 1 / 0 / 0 | Skip. |
| Palestine | Palestine, Palestinian | 0 / 0 | Skip until other manifests exist. |

## Building later

`scripts/build_manifest.py` currently reads search terms from `config.yml`. When
you start the campaign, add the country/city block there (or copy this file
into a sibling repo) and run:

```bash
python scripts/build_manifest.py israel rehovot --dry-run
python scripts/build_manifest.py israel haifa --dry-run
python scripts/build_manifest.py saudi_arabia kaust --dry-run
python scripts/build_manifest.py turkey istanbul --dry-run
python scripts/build_manifest.py egypt cairo --dry-run
```

Keep an accession only when the PRIDE record itself confirms the Middle Eastern
country. Do not add these countries to NordicSDRF `config.yml` until you
actually want them on the Nordic status charts.
