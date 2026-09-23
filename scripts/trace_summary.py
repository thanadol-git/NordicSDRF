#!/usr/bin/env python3
"""Summarise a headless Claude Code trace (results/logs/<PXD>.<ts>.jsonl).

    python scripts/trace_summary.py results/logs/PXD001817.*.jsonl        # one line per trace
    python scripts/trace_summary.py -v results/logs/PXD001817.20260923-204007.jsonl   # + every tool call

Works on a trace that is still being written: the last line is the current state.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path


def tool_arg(inp: dict) -> str:
    for k in ("command", "file_path", "pattern", "url", "query", "project_accession", "uri"):
        if k in inp:
            return str(inp[k])
    return json.dumps(inp, ensure_ascii=False)


def summarise(path: Path, verbose: bool) -> None:
    events = []
    for line in path.read_text().splitlines():
        if line.strip():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                pass  # partial last line of a live trace
    if not events:
        print(f"{path.name}: empty")
        return

    tools, ctx, compactions, result = [], 0, 0, None
    for e in events:
        t = e.get("type")
        if t == "assistant":
            ctx = e["message"].get("usage", {}).get("input_tokens") or ctx
            for b in e["message"].get("content", []):
                if b.get("type") == "tool_use":
                    tools.append((b["name"], tool_arg(b.get("input", {}))))
        elif t == "system" and e.get("subtype") == "status" and e.get("status") == "compacting":
            compactions += 1
        elif t == "result":
            result = e

    age = time.time() - path.stat().st_mtime
    if result:
        text = (result.get("result") or "").strip().replace("\n", " ")
        state = (f"FINISHED {result.get('subtype')} after {result.get('num_turns')} turns, "
                 f"{result.get('duration_ms', 0) / 60000:.0f} min"
                 + (f" — {text[:80]}" if text.startswith("API Error") else ""))
    else:
        state = f"RUNNING (last write {age / 60:.0f} min ago" + (", looks stalled" if age > 900 else "") + ")"
    last = f"{tools[-1][0]}({tools[-1][1][:60]})" if tools else "no tool calls yet"
    print(f"{path.name}: {state}; {len(tools)} tool calls; context {ctx // 1000}k; "
          f"{compactions} compactions; last tool: {last}")

    if verbose:
        for i, (name, arg) in enumerate(tools, 1):
            print(f"  {i:3d} {name:<42} {arg[:100]}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("trace", nargs="+", type=Path)
    ap.add_argument("-v", "--verbose", action="store_true", help="list every tool call")
    args = ap.parse_args()
    for p in args.trace:
        if not p.exists():
            print(f"{p}: not found", file=sys.stderr)
            continue
        summarise(p, args.verbose)


if __name__ == "__main__":
    main()
