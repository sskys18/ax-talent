#!/usr/bin/env python3
"""End-to-end tests for the missing-doc-hunter workflow plugin."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
ROOT = os.path.dirname(SRC)

REQUESTS = os.path.join(SRC, "examples", "pbc_requests.csv")
EVIDENCE = os.path.join(SRC, "examples", "evidence_manifest.csv")
TRIAL_BALANCE = os.path.join(SRC, "examples", "trial_balance.csv")
OUT_DIR = os.path.join(SRC, "outputs")
MANIFEST = os.path.join(OUT_DIR, "submission_package_manifest.json")
REPORT = os.path.join(OUT_DIR, "missing_doc_hunter_report.md")
MISSING = os.path.join(OUT_DIR, "missing_items.md")
EMAIL = os.path.join(OUT_DIR, "followup_email_draft.md")

DOC_MATCHER = os.path.join(SRC, "tools", "doc_matcher.py")
REPORT_WRITER = os.path.join(SRC, "tools", "report_writer.py")


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise AssertionError(f"Command failed: {' '.join(cmd)}\n{result.stdout}\n{result.stderr}")
    return result


class MissingDocHunterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        run([sys.executable, DOC_MATCHER,
             "--requests", REQUESTS,
             "--evidence", EVIDENCE,
             "--trial-balance", TRIAL_BALANCE,
             "--out", MANIFEST])
        run([sys.executable, REPORT_WRITER,
             "--manifest", MANIFEST,
             "--out-dir", OUT_DIR])
        with open(MANIFEST, encoding="utf-8") as handle:
            cls.manifest = json.load(handle)
        cls.requests = cls.manifest["requests"]
        cls.by_id = {r["request_id"]: r for r in cls.requests}

    def test_manifest_generated(self):
        self.assertTrue(os.path.exists(MANIFEST))

    def test_all_five_requests_present(self):
        self.assertEqual(len(self.requests), 5)
        for rid in ("AR-03", "CUT-01", "JE-02", "INV-04", "RP-05"):
            self.assertIn(rid, self.by_id)

    def test_at_least_one_ready(self):
        self.assertTrue(any(r["status"] == "Ready" for r in self.requests))

    def test_at_least_one_partially_ready(self):
        self.assertTrue(any(r["status"] == "Partially ready" for r in self.requests))

    def test_at_least_one_missing_or_needs_review(self):
        self.assertTrue(any(r["status"] in ("Missing", "Needs human review") for r in self.requests))

    def test_ar_required_keys(self):
        keys = self.by_id["AR-03"]["required_keys"]
        for key in ("customer_id", "invoice_id", "due_date", "amount"):
            self.assertIn(key, keys)

    def test_report_generated(self):
        self.assertTrue(os.path.exists(REPORT))
        with open(REPORT, encoding="utf-8") as handle:
            content = handle.read()
        for heading in (
            "# Missing Doc Hunter Report",
            "## Summary",
            "## Request-by-Request Review",
            "## Missing or Insufficient Documents",
            "## Human Review Notes",
            "## Submission Readiness",
        ):
            self.assertIn(heading, content)

    def test_missing_items_generated(self):
        self.assertTrue(os.path.exists(MISSING))

    def test_followup_email_generated(self):
        self.assertTrue(os.path.exists(EMAIL))

    def test_manifest_includes_issue_types(self):
        issue_types = set()
        for r in self.requests:
            for issue in r["issues"]:
                issue_types.add(issue["type"])
        self.assertTrue(
            issue_types & {"missing_document", "missing_required_columns"},
            f"expected missing_document or missing_required_columns in {issue_types}",
        )

    def test_each_request_has_required_fields(self):
        fields = {
            "request_id", "request_text", "inferred_purpose", "request_type",
            "required_evidence", "required_keys", "matched_files",
            "missing_items", "issues", "status", "next_actions",
        }
        for r in self.requests:
            self.assertTrue(fields.issubset(r.keys()), f"{r['request_id']} missing fields")


if __name__ == "__main__":
    unittest.main()
