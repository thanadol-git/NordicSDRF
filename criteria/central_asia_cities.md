# Central Asia countries for the PXD campaign

Narrative reference for Central Asia cities tracked in `config.yml` with
`region: central_asia`. The region overview is `status/plots/central_asia.svg`
(one horizontal bar per country, same style as Nordic / SEA / South Asia /
Middle East). Per-country city charts are `status/plots/<country>.svg` with
pages under `status/markdowns/`. Manifests appear under
`lists/<country>/<city>.txt` when scoped; use the same `build_manifest.py`
path (keyword search, then keep only records that confirm the country).

Scope: the five Central Asian republics (Kazakhstan, Uzbekistan, Kyrgyzstan,
Tajikistan, Turkmenistan). Mongolia is **out of scope** here — the bare
`Mongolia` / `Mongolian` keywords are dominated by Inner Mongolia (China) and
archaeology papers deposited elsewhere; none of a spot-check confirmed
`countries: [Mongolia]`. Afghanistan is already under South Asia.

**"PRIDE hits"** is `total_records` from the PRIDE Archive v2 full-text search
(`/pride/ws/archive/v2/search/projects?keyword=<term>`), queried 2026-11-27.
The search matches titles, descriptions and affiliation strings, so it both
over-counts (demonyms, sample geography, diaspora) and under-counts
(submitters who wrote only the institute name). After a country filter this
region is **very small**: Kazakhstan is the only country with confirmed
deposits so far; the other four are empty stubs kept for the overview.

> **Known traps.** `Uzbek` (8) is almost all France/Germany bovine / EV papers
> (author surnames), not Uzbekistan. `Tajik` / `Tajikistan` hits are sample
> geography in European archaeology labs. `Kazakh` overlaps the same four
> records as `Kazakhstan`. Prefer institute strings (`Nazarbayev University`,
> `National Center for Biotechnology`) plus a hard `countries` check. City
> names (`Almaty`, `Astana`, `Tashkent`, `Bishkek`, …) currently return 0
> raw hits on their own.

## Country list

| Order | Country | Slug | Cities that matter | PRIDE hits (country name) | Manifest |
|---:|---|---|---|---:|---|
| 1 | Kazakhstan | `kazakhstan` | Astana, Almaty | 4 | `lists/kazakhstan/<city>.txt` |
| 2 | Uzbekistan | `uzbekistan` | Tashkent | 1 | `lists/uzbekistan/tashkent.txt` |
| 3 | Tajikistan | `tajikistan` | Dushanbe | 1 | `lists/tajikistan/dushanbe.txt` |
| 4 | Kyrgyzstan | `kyrgyzstan` | Bishkek | 0 | `lists/kyrgyzstan/bishkek.txt` (empty) |
| 5 | Turkmenistan | `turkmenistan` | Ashgabat | 0 | `lists/turkmenistan/ashgabat.txt` (empty) |

`Central Asia` as a keyword is not useful (4 mixed hits). Search country /
institute names, then filter on country.

## Kazakhstan — only confirmed deposits so far

| City | Search terms | Key institutions / facilities | PRIDE hits | Notes |
|---|---|---|---:|---|
| Astana | Kazakhstan, Astana, Nur-Sultan, Nazarbayev | Nazarbayev University; National Center for Biotechnology | 4 / 0 / 0 / 0 | Both confirmed Kazakhstan PXDs (spot-check) are Astana-linked. |
| Almaty | Almaty, KazNU, "Al-Farabi" | Al-Farabi Kazakh National University | 0 / 0 / 0 | Keep stub; city terms currently empty. |

## Uzbekistan, Kyrgyzstan, Tajikistan, Turkmenistan

| Country | Search terms | PRIDE hits | Notes |
|---|---|---:|---|
| Uzbekistan | Uzbekistan, Tashkent, Uzbek | 1 / 0 / 8 | `Uzbek` is surname noise — require `countries` / affiliation. |
| Kyrgyzstan | Kyrgyzstan, Bishkek | 0 / 0 | Empty. |
| Tajikistan | Tajikistan, Dushanbe, Tajik | 1 / 0 / 2 | Archaeology sample geography — expect 0 after filter. |
| Turkmenistan | Turkmenistan, Ashgabat | 0 / 0 | Empty. |

## Building manifests

```bash
python scripts/build_manifest.py kazakhstan astana
python scripts/build_manifest.py kazakhstan almaty
python scripts/build_manifest.py uzbekistan tashkent
python scripts/update_status.py --no-pride
```

Keep an accession only when the PRIDE record itself confirms the Central Asian
country. Refresh `status/plots/central_asia.svg` with
`python scripts/update_status.py --no-pride`.
