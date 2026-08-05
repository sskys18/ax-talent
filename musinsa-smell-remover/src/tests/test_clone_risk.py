import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from clone_risk import (  # noqa: E402
    avoid_conflicts,
    calculate_clone_risk,
    read_csv_by_id,
    read_products,
    read_request,
)


class CloneRiskWorkflowTest(unittest.TestCase):
    def setUp(self):
        self.products_path = ROOT / "examples" / "products.csv"
        self.rankings_path = ROOT / "examples" / "rankings.csv"
        self.reviews_path = ROOT / "examples" / "reviews.csv"
        self.request_path = ROOT / "examples" / "user_request.json"
        self.products = read_products(str(self.products_path))
        self.rankings = read_csv_by_id(str(self.rankings_path))
        self.reviews = read_csv_by_id(str(self.reviews_path))
        self.request = read_request(str(self.request_path))
        self.avoid_terms = self.request["user"]["avoid"]

    def score_for(self, product_id):
        product = next(item for item in self.products if item["product_id"] == product_id)
        score, reasons, conflicts = calculate_clone_risk(
            product,
            self.rankings[product_id],
            self.reviews[product_id],
            self.avoid_terms,
        )
        return score, reasons, conflicts

    def test_clone_risk_score_is_between_zero_and_100(self):
        for product in self.products:
            score, _, _ = calculate_clone_risk(
                product,
                self.rankings[product["product_id"]],
                self.reviews[product["product_id"]],
                self.avoid_terms,
            )
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 100)

    def test_avoid_keyword_products_receive_higher_risk(self):
        german_army_score, _, conflicts = self.score_for("P003")
        linen_shirt_score, _, _ = self.score_for("P005")
        self.assertIn("german army sneakers", conflicts)
        self.assertGreater(german_army_score, linen_shirt_score)

    def test_clone_risk_scores_csv_is_generated(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools" / "clone_risk.py"),
                    "--products",
                    str(self.products_path),
                    "--rankings",
                    str(self.rankings_path),
                    "--reviews",
                    str(self.reviews_path),
                    "--request",
                    str(self.request_path),
                    "--out-dir",
                    tmpdir,
                ],
                check=True,
            )
            output = Path(tmpdir) / "clone_risk_scores.csv"
            self.assertTrue(output.exists())
            with output.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), len(self.products))

    def test_recommendation_json_is_generated_without_avoid_conflicts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools" / "clone_risk.py"),
                    "--products",
                    str(self.products_path),
                    "--rankings",
                    str(self.rankings_path),
                    "--reviews",
                    str(self.reviews_path),
                    "--request",
                    str(self.request_path),
                    "--out-dir",
                    tmpdir,
                ],
                check=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools" / "outfit_report.py"),
                    "--products",
                    str(self.products_path),
                    "--scores",
                    str(Path(tmpdir) / "clone_risk_scores.csv"),
                    "--request",
                    str(self.request_path),
                    "--out-dir",
                    tmpdir,
                ],
                check=True,
            )
            output = Path(tmpdir) / "recommendation.json"
            self.assertTrue(output.exists())
            with output.open(encoding="utf-8") as handle:
                recommendation = json.load(handle)
            self.assertGreaterEqual(len(recommendation["items"]), 3)
            self.assertLessEqual(len(recommendation["items"]), 5)
            self.assertTrue(recommendation["budget_ok"])
            product_by_id = {product["product_id"]: product for product in self.products}
            for item in recommendation["items"]:
                product = product_by_id[item["product_id"]]
                self.assertEqual(avoid_conflicts(product, self.avoid_terms), [])


if __name__ == "__main__":
    unittest.main()
