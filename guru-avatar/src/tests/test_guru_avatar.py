#!/usr/bin/env python3
"""Tests for the guru-avatar workflow plugin."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
TOOLS = os.path.join(SRC, "tools")
EXAMPLES = os.path.join(SRC, "examples")

if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

import compliance_check  # noqa: E402


class GuruAvatarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.out_dir = tempfile.mkdtemp(prefix="guru_avatar_")
        cls.report_md = os.path.join(cls.out_dir, "guru_avatar_report.md")
        cls.report_json = os.path.join(cls.out_dir, "guru_avatar_report.json")
        cls.questions_md = os.path.join(cls.out_dir, "investor_questions.md")
        cls.compliance_md = os.path.join(cls.out_dir, "compliance_check.md")

        gen = subprocess.run(
            [
                sys.executable,
                os.path.join(TOOLS, "guru_lens.py"),
                "--metrics", os.path.join(EXAMPLES, "stock_metrics.csv"),
                "--holdings", os.path.join(EXAMPLES, "public_holdings.csv"),
                "--lenses", os.path.join(EXAMPLES, "guru_lenses.json"),
                "--profile", os.path.join(EXAMPLES, "user_profile.json"),
                "--out-dir", cls.out_dir,
            ],
            capture_output=True,
            text=True,
        )
        assert gen.returncode == 0, f"guru_lens.py failed: {gen.stderr}"

        cls.compliance_proc = subprocess.run(
            [
                sys.executable,
                os.path.join(TOOLS, "compliance_check.py"),
                "--report", cls.report_md,
                "--out", cls.compliance_md,
            ],
            capture_output=True,
            text=True,
        )

    def test_report_markdown_generated(self) -> None:
        self.assertTrue(os.path.exists(self.report_md))

    def test_report_json_generated(self) -> None:
        self.assertTrue(os.path.exists(self.report_json))

    def test_investor_questions_generated(self) -> None:
        self.assertTrue(os.path.exists(self.questions_md))

    def test_compliance_report_generated(self) -> None:
        self.assertTrue(os.path.exists(self.compliance_md))

    def test_report_has_no_prohibited_phrases(self) -> None:
        with open(self.report_md, encoding="utf-8") as handle:
            text = handle.read()
        violations = compliance_check.find_violations(text)
        self.assertEqual(violations, [], f"Prohibited phrases found: {violations}")

    def test_every_lens_has_investor_questions(self) -> None:
        with open(self.report_json, encoding="utf-8") as handle:
            report = json.load(handle)
        self.assertTrue(report["lenses"], "No lenses in report")
        for lens in report["lenses"]:
            with self.subTest(lens=lens["name"]):
                total_questions = sum(len(c["investor_questions"]) for c in lens["criteria"])
                self.assertGreater(total_questions, 0, f"{lens['name']} has no investor questions")

    def test_beginner_safety_check_included(self) -> None:
        with open(self.report_md, encoding="utf-8") as handle:
            text = handle.read()
        self.assertIn("Beginner Safety Check", text)

    def test_compliance_returns_pass(self) -> None:
        self.assertEqual(self.compliance_proc.returncode, 0, self.compliance_proc.stdout)
        with open(self.compliance_md, encoding="utf-8") as handle:
            text = handle.read()
        self.assertIn("Status: PASS", text)


if __name__ == "__main__":
    unittest.main()
