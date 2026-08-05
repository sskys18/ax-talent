#!/usr/bin/env python3
"""Scan a generated Markdown report for prohibited recommendation-like phrases.

The guru-avatar plugin must never issue buy, sell, or hold recommendations and
must never promise returns. This checker enforces that boundary by flagging any
prohibited phrase (English or Korean) found in the report.

Standard library only.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional, Tuple

# English phrases are matched case-insensitively. Korean phrases are matched as-is.
PROHIBITED_PHRASES: List[str] = [
    "buy now",
    "sell now",
    "strong buy",
    "guaranteed return",
    "guaranteed",
    "target return",
    "must buy",
    "must sell",
    "지금 매수",
    "지금 매도",
    "무조건",
    "확실한 수익",
    "수익 보장",
    "매수 추천",
    "매도 추천",
    "보유 추천",
]

REVISION_GUIDANCE = [
    "Replace any directive language (purchase, dispose, keep) with neutral, "
    "educational framing such as questions the investor should ask themselves.",
    "Remove any promise or forecast of returns; state that future performance is unknown.",
    "Keep next actions limited to safe, non-directive steps: watchlist, paper "
    "trading, review after earnings, position-size comparison, and same-sector comparison.",
    "Re-run this compliance check until the status is PASS before finalizing.",
]


def find_violations(text: str) -> List[Tuple[str, int]]:
    """Return (phrase, line_number) for every prohibited phrase occurrence."""
    violations: List[Tuple[str, int]] = []
    lines = text.splitlines()
    for idx, line in enumerate(lines, start=1):
        lowered = line.lower()
        for phrase in PROHIBITED_PHRASES:
            haystack = lowered if phrase.isascii() else line
            needle = phrase.lower() if phrase.isascii() else phrase
            if needle in haystack:
                violations.append((phrase, idx))
    return violations


def render_compliance_report(report_path: str, violations: List[Tuple[str, int]]) -> str:
    status = "FAIL" if violations else "PASS"
    lines: List[str] = []
    lines.append("# Compliance Check")
    lines.append("")
    lines.append(f"Status: {status}")
    lines.append("")
    lines.append(f"Scanned report: {report_path}")
    lines.append(f"Prohibited phrases checked: {len(PROHIBITED_PHRASES)}")
    lines.append("")
    lines.append("## Detected risky phrases")
    lines.append("")
    if violations:
        for phrase, line_no in violations:
            lines.append(f"- Line {line_no}: \"{phrase}\"")
    else:
        lines.append("None detected.")
    lines.append("")
    lines.append("## Suggested revision guidance")
    lines.append("")
    for tip in REVISION_GUIDANCE:
        lines.append(f"- {tip}")
    lines.append("")
    return "\n".join(lines)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check a report for prohibited recommendation phrases.")
    parser.add_argument("--report", required=True, help="Path to the Markdown report to scan")
    parser.add_argument("--out", required=True, help="Path to write the compliance report")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    with open(args.report, encoding="utf-8") as handle:
        text = handle.read()

    violations = find_violations(text)
    report = render_compliance_report(args.report, violations)

    with open(args.out, "w", encoding="utf-8") as handle:
        handle.write(report)

    status = "FAIL" if violations else "PASS"
    print(f"Compliance status: {status}")
    print(f"Wrote {args.out}")
    if violations:
        for phrase, line_no in violations:
            print(f"  Line {line_no}: {phrase}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
