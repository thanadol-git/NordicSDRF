# Nordic cities for the PXD campaign

Reference list of the cities (and the institutions behind them) that generate
MS-proteomics depositions in PRIDE across the five Nordic countries. Use it to
scope new `lists/<country>/<city>.txt` manifests and to pick search terms.

**"PRIDE hits"** is the `total_records` returned by the PRIDE Archive v2
full-text search (`/pride/ws/archive/v2/search/projects?keyword=<city>`),
queried 2026-09-23 for the single city name. The live numbers (unioned over
all of a city's `search_terms` in `config.yml`, plus overlap with the
community corpus) are maintained by `scripts/update_status.py` in the README
and `status/<country>.md`; this file is the narrative reference. The hit count
is a rough size indicator, not a manifest count: the
search matches titles, descriptions and affiliation strings, so it both
over-counts (surnames, streets, other places with the same name) and
under-counts (submitters who wrote only the institute name). The Swedish
manifests already in this repo are 35–70 % of the raw hit counts after
curation.

> **Known trap.** `PXD001817` was removed from the Uppsala manifest because it is
> a Utrecht dataset: the lab PI's address is *"Uppsalalaan 8, 3584 CT Utrecht"*
> and PRIDE records `countries: [Netherlands]`. Keyword-built manifests can contain such
> false positives. The cheap, deterministic fix belongs in tier 1: fetch
> `/pride/ws/archive/v2/projects/<PXD>` and require the Nordic country in
> `countries` (or in a `submitters[].country` / `labPIs[].affiliation` string)
> before the accession is allowed through to screening.

## Sweden — in progress

| City | Search terms | Key institutions / facilities | PRIDE hits | Manifest |
|---|---|---|---:|---|
| Stockholm | Stockholm, Solna, Huddinge, Karolinska, KTH, SciLifeLab | Karolinska Institutet, KTH Royal Institute of Technology, Stockholm University, SciLifeLab (Solna), Karolinska University Hospital | 211 | `lists/sweden/stockholm.txt` (165) |
| Uppsala | Uppsala | Uppsala University, SLU, Uppsala University Hospital (Akademiska), SciLifeLab Uppsala | 196 | `lists/sweden/uppsala.txt` (69) — six confirmed affiliation false positives removed |
| Gothenburg | Gothenburg, Göteborg, Sahlgrenska, Chalmers | University of Gothenburg, Chalmers, Sahlgrenska University Hospital / Academy, GU Proteomics Core Facility | 166 + 18 | `lists/sweden/gothenburg.txt` (135) |
| Lund | Lund, Malmö, Skåne | Lund University (BMC, Medicon Village), Skåne University Hospital, Malmö campus | 503 + 16 | `lists/sweden/lund.txt` (163) — "Lund" is also a common surname |
| Umeå | Umeå, Umea | Umeå University, SLU Umeå | 45 | `lists/sweden/umea.txt` (39) — from the 2026-09-25 queue; 6 rejected affiliation hits omitted |
| Linköping | Linköping, Linkoping | Linköping University, Linköping University Hospital | 26 | `lists/sweden/linkoping.txt` (26) — from the 2026-09-25 queue |
| Örebro | Örebro, Orebro | Örebro University | 0 | not scoped |

## Denmark — not started (largest Nordic depositor)

| City | Search terms | Key institutions / facilities | PRIDE hits |
|---|---|---|---:|
| Copenhagen | Copenhagen, København, Frederiksberg, Rigshospitalet | University of Copenhagen; Novo Nordisk Foundation Center for Protein Research (CPR — Mann, Olsen, Jensen, Nielsen labs, very high volume); Rigshospitalet; Herlev/Gentofte; Statens Serum Institut; Novo Nordisk (Måløv/Bagsværd) | 552 + 13 |
| Odense | Odense, "University of Southern Denmark", SDU | SDU Department of Biochemistry & Molecular Biology (Jensen, Røssel Larsen labs), Odense University Hospital; Evosep is also based here | 548 |
| Aarhus | Aarhus, Århus | Aarhus University (iNANO, Biomedicine — Enghild lab), Aarhus University Hospital | 117 |
| Aalborg | Aalborg | Aalborg University, Aalborg University Hospital | 67 |
| Lyngby | Lyngby, DTU, "Technical University of Denmark" | DTU Bioengineering, DTU Proteomics Core | 37 |
| Roskilde | Roskilde | Roskilde University | 9 |

Copenhagen and Odense together are roughly the size of the whole Swedish
campaign; expect many multiplexed (TMT) and DIA studies from CPR and SDU.

## Norway — not started

| City | Search terms | Key institutions / facilities | PRIDE hits |
|---|---|---|---:|
| Bergen | Bergen, Haukeland, PROBE | University of Bergen, PROBE Proteomics Unit, Haukeland University Hospital | 217 — also matches Bergen (NJ, USA) and Bergen op Zoom (NL) |
| Oslo | Oslo, Rikshospitalet, Radiumhospitalet, Ullevål | University of Oslo, Oslo University Hospital (OUS Proteomics Core Facility), Norwegian Institute of Public Health | 124 |
| Trondheim | Trondheim, NTNU, PROMEC | NTNU, PROMEC (Proteomics and Modomics Experimental Core), St. Olavs Hospital | 48 |
| Ås | NMBU, "Norwegian University of Life Sciences" | NMBU (do not search the bare token "Ås") | 35 (noisy) |
| Tromsø | Tromsø, Tromso, UiT | UiT The Arctic University of Norway, University Hospital of North Norway | 14 |
| Stavanger | Stavanger | University of Stavanger, Stavanger University Hospital | 0 |

## Finland — in progress (Oulu, Tampere, Kuopio, Jyväskylä scoped)

| City | Search terms | Key institutions / facilities | PRIDE hits | Manifest |
|---|---|---|---:|---|
| Helsinki | Helsinki, Espoo, HiLIFE, Meilahti, FIMM, Aalto | University of Helsinki (Institute of Biotechnology, HiLIFE, Meilahti Clinical Proteomics Core Facility), Helsinki University Hospital (HUS), FIMM, Aalto University and VTT (Espoo) | 162 | not scoped |
| Turku | Turku, Åbo, "Turku Bioscience" | University of Turku, Åbo Akademi, Turku Bioscience Centre (Turku Proteomics Facility), Turku University Hospital | 98 | not scoped |
| Oulu | Oulu | University of Oulu, Biocenter Oulu | 11 | `lists/finland/oulu.txt` (11) — all 11 PRIDE hits confirmed Finland |
| Tampere | Tampere | Tampere University, Tampere University Hospital | 5 | `lists/finland/tampere.txt` (4) — 4/5 PRIDE hits confirmed Finland; PXD021494 rejected (Karolinska / Sweden) |
| Kuopio | Kuopio, "University of Eastern Finland" | University of Eastern Finland, Kuopio University Hospital | 10 | `lists/finland/kuopio.txt` (10) — all 10 PRIDE hits confirmed Finland |
| Jyväskylä | Jyväskylä, Jyvaskyla | University of Jyväskylä | 1 | `lists/finland/jyvaskyla.txt` (1) — the single PRIDE hit confirmed Finland |

## Iceland — not started (small)

| City | Search terms | Key institutions / facilities | PRIDE hits |
|---|---|---|---:|
| Reykjavík | Reykjavik, Reykjavík, Iceland, Landspítali, deCODE | University of Iceland, Landspítali National University Hospital, deCODE genetics | 4 (6 for "Iceland") |

Most Icelandic proteomics (deCODE) is affinity-based (Olink, SomaScan) and is
not deposited in PRIDE; Iceland can probably be handled as a single manifest.

## Country totals and suggested order

| Country | PRIDE hits (country name) | Suggested order | Why |
|---|---:|---|---|
| Sweden | 1149 | 1 — running | manifests exist |
| Denmark | 1600 | 2 | biggest volume; CPR + SDU are also the most template-diverse (TMT, DIA, PTM) |
| Norway | 461 | 3 | Bergen + Oslo cover most of it |
| Finland | 205 | 4 | Helsinki + Turku cover most of it |
| Iceland | 6 | 5 | one short manifest |

## Building the next manifests

1. Pull candidates with the city/institution search terms above (English
   spelling first; diacritic forms add only a handful).
2. Fetch each candidate's project record and keep it only if a Nordic country
   appears in `countries`, `submitters[].country`, or an affiliation string —
   this removes the *Uppsalalaan*-type false positives deterministically.
3. Dedup across cities and against `sdrf-annotated-datasets` before anything
   reaches `sdrf-metascreen`.
4. Add the city under the country in `config.yml` with its `pxd_count`.
