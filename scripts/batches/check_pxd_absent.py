"""Fail before starting an SDRF when an accession is already annotated.

Usage: python scripts/batches/check_pxd_absent.py PXD012345 ... \
    --bigbio-repo /path/to/sdrf-annotated-datasets
"""

import argparse
import json
import re
import subprocess
from pathlib import Path


def run(*args: str) -> str:
    return subprocess.check_output(args, text=True)


def accession_in_path(path: str, accession: str) -> bool:
    return bool(re.search(rf"(?:^|/){accession}(?:[./-]|$)", path))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("accessions", nargs="+", help="PXD accessions to screen")
    parser.add_argument("--bigbio-repo", type=Path, required=True)
    parser.add_argument("--refresh", action="store_true", help="fetch BigBio upstream/main first")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    for accession in args.accessions:
        if not re.fullmatch(r"PXD\d{6}", accession):
            parser.error(f"invalid accession: {accession}")
    if args.refresh:
        subprocess.check_call(["git", "-C", str(args.bigbio_repo), "fetch", "upstream", "main"])

    local_paths = [str(path.relative_to(root)) for path in (root / "annotations").glob("PXD*")]
    refs = run("git", "-C", str(root), "for-each-ref", "--format=%(refname)",
               "refs/heads", "refs/remotes/origin").splitlines()
    local_refs = {
        ref: run("git", "-C", str(root), "ls-tree", "-r", "--name-only", ref, "annotations").splitlines()
        for ref in refs
    }
    bigbio_paths = run("git", "-C", str(args.bigbio_repo), "ls-tree", "-r", "--name-only",
                       "upstream/main", "datasets").splitlines()
    prs = json.loads(run("gh", "pr", "list", "--repo", "bigbio/sdrf-annotated-datasets",
                        "--state", "open", "--limit", "500", "--json",
                        "number,title,body,headRefName"))
    pr_files = {
        pr["number"]: run("gh", "api", f"repos/bigbio/sdrf-annotated-datasets/pulls/{pr['number']}/files",
                          "--paginate", "--jq", ".[].filename").splitlines()
        for pr in prs
    }

    found = False
    for accession in args.accessions:
        hits = [f"local:{path}" for path in local_paths if accession_in_path(path, accession)]
        hits += [f"{ref}:{path}" for ref, paths in local_refs.items()
                 for path in paths if accession_in_path(path, accession)]
        hits += [f"bigbio/main:{path}" for path in bigbio_paths
                 if accession_in_path(path, accession)]
        for pr in prs:
            fields = "\n".join(str(pr.get(key, "")) for key in ("title", "body", "headRefName"))
            if accession in fields or any(accession_in_path(path, accession)
                                          for path in pr_files[pr["number"]]):
                hits.append(f"bigbio/PR#{pr['number']}")
        if hits:
            found = True
            print(f"BLOCKED {accession}: " + "; ".join(sorted(set(hits))))
        else:
            print(f"CLEAR {accession}")
    return int(found)


if __name__ == "__main__":
    raise SystemExit(main())
