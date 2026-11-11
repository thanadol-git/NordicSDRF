"""Build SDRF with repeated cleavage columns for sequential digestion.

Uses sdrf-skills' parser, contract, coordinate checks, and writer. The current
contract marks cleavage as singular even though SDRF permits repeated columns.
"""
import argparse
import json
from pathlib import Path
from tools import build as b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--samples', required=True)
    ap.add_argument('--technical', required=True)
    ap.add_argument('--files', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('-t', '--template', action='append', required=True)
    args = ap.parse_args()
    contract = b.template_contract(args.template)
    cleavage = next(c for c in contract.columns if c.name == 'comment[cleavage agent details]')
    cleavage.multiple = True
    header, sample_rows = b.read_table(args.samples)
    samples = b.parse_samples(header, sample_rows)
    tech = b.parse_technical(b.read_table(args.technical)[1])
    files = json.loads(Path(args.files).read_text())
    if isinstance(files, dict):
        files = files.get('files', [])
    b.check_files(samples, files)
    b.check_channels(samples)
    b.check_coordinates(samples)
    out_header, out_rows = b.expand(samples, tech, contract)
    b.write_sdrf(out_header, out_rows, args.out)
    print(f'wrote {args.out}: {len(out_rows)} rows x {len(out_header)} columns')


if __name__ == '__main__':
    main()
