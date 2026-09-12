#!/usr/bin/env python3
"""Prepare blind behavioral cases or summarize recorded outputs; no API/model calls."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "summarize"))
    parser.add_argument("--results", type=Path, help="JSON array of {id, output, action}")
    parser.add_argument("--preview", action="store_true", help="Force preview for non-option cases")
    args = parser.parse_args()
    cases = json.loads((ROOT / "evals/cases.json").read_text(encoding="utf-8"))
    if args.command == "prepare":
        prepared = []
        for case in cases:
            request = case["input"]
            if args.preview and case["kind"] != "options":
                request = request.replace("/promptly ", "/promptly --show ", 1)
            prepared.append({"id": case["id"], "input": request, "context": case["context"]})
        print(json.dumps(prepared, indent=2, ensure_ascii=False))
        return 0
    if not args.results:
        parser.error("summarize requires --results")
    outputs = json.loads(args.results.read_text(encoding="utf-8-sig"))
    by_id = {case["id"]: case for case in cases}
    seen = set()
    summaries = []
    for row in outputs:
        identifier = row["id"]
        if identifier not in by_id or identifier in seen:
            parser.error(f"Unknown or duplicate case: {identifier}")
        seen.add(identifier)
        words = len(row["output"].split())
        summaries.append({"id": identifier, "words": words,
                          "soft_limit": by_id[identifier]["max_words"],
                          "over_soft_limit": words > by_id[identifier]["max_words"],
                          "reported_action": row.get("action", "unrecorded")})
    print(json.dumps({"recorded": len(seen), "total": len(cases),
                      "missing": sorted(set(by_id) - seen), "results": summaries,
                      "note": "Length/action metadata only. Apply the semantic rubric manually."},
                     indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
