"""Expand repeated MaxQuant search modifications in builder-produced SDRFs."""

import csv
from pathlib import Path


root = Path(__file__).resolve().parents[2]
work = root / "scratchpad/PXD066033"
for arm in ("cellular", "in-vitro"):
    path = root / f"annotations/PXD066033-{arm}.sdrf.tsv"
    with (work / f"{arm}-technical.tsv").open(newline="") as handle:
        mods = [r["value"] for r in csv.DictReader(handle, delimiter="\t") if r["column"] == "comment[modification parameters]"]
    assert len(mods) == 4
    with path.open(newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        header = next(reader)
        rows = list(reader)
    key = "comment[modification parameters]"
    assert header.count(key) == 1
    index = header.index(key)
    assert all(row[index] == mods[-1] for row in rows)
    header[index:index] = [key] * (len(mods) - 1)
    for row in rows:
        row[index:index] = mods[:-1]
    assert "comment[filename date code]" not in header
    file_index = header.index("comment[data file]")
    header.insert(file_index + 1, "comment[filename date code]")
    for row in rows:
        code = row[file_index].split("_", 1)[0]
        assert code in {"20250220", "20250303"}
        row.insert(file_index + 1, code)
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)
    print(path.relative_to(root), len(rows), "rows", header.count(key), "modification columns")
