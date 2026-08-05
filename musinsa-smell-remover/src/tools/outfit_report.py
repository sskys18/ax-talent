#!/usr/bin/env python3
"""Generate a wearable outfit report from clone risk scores."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from typing import Dict, Iterable, List, Tuple

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from clone_risk import avoid_conflicts, read_products, read_request  # noqa: E402

CATEGORY_ORDER = ["top", "bottom", "shoes", "bag", "accessory"]
REQUIRED_CATEGORIES = ["top", "bottom", "shoes"]
OPTIONAL_CATEGORIES = ["bag", "accessory"]


def read_scores(path: str) -> Dict[str, Dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as handle:
        return {row["product_id"]: row for row in csv.DictReader(handle)}


def to_int(value: object, default: int = 0) -> int:
    try:
        return int(float(value or default))
    except (TypeError, ValueError):
        return default


def product_summary(product: Dict[str, str]) -> str:
    details = [
        product.get("color", ""),
        product.get("silhouette", ""),
        product.get("material", ""),
    ]
    return ", ".join(part for part in details if part)


def less_common_reason(product: Dict[str, str], score: Dict[str, str]) -> str:
    reasons = []
    text = " ".join(
        product.get(key, "") for key in ("color", "silhouette", "material", "tags")
    ).lower()
    if any(token in text for token in ("linen", "seersucker", "ripstop", "suede", "tencel", "knit")):
        reasons.append("textured or less-default material")
    if any(token in text for token in ("sage", "ecru", "olive", "taupe", "sand", "stone", "brown", "natural", "stripe")):
        reasons.append("color choice avoids the default black-gray clone palette")
    if product.get("silhouette", "").lower() in {"regular", "straight", "tapered", "slim", "compact"}:
        reasons.append("controlled silhouette avoids the overfit formula")
    if not reasons:
        reasons.append("lower local clone-risk score than common alternatives")
    return "; ".join(reasons) + f" (risk {score.get('clone_risk_score')}/100)"


def candidate_products(
    products: List[Dict[str, str]],
    scores: Dict[str, Dict[str, str]],
    avoid_terms: Iterable[str],
) -> List[Dict[str, object]]:
    candidates: List[Dict[str, object]] = []
    for product in products:
        product_id = product["product_id"]
        score = scores.get(product_id)
        if not score:
            continue
        conflicts = avoid_conflicts(product, avoid_terms)
        if conflicts or score.get("avoid_conflict", "").strip():
            continue
        enriched: Dict[str, object] = dict(product)
        enriched["clone_risk_score"] = to_int(score.get("clone_risk_score"), 100)
        enriched["score_reasons"] = score.get("score_reasons", "")
        candidates.append(enriched)
    return candidates


def choose_outfit(candidates: List[Dict[str, object]], budget: int) -> List[Dict[str, object]]:
    by_category: Dict[str, List[Dict[str, object]]] = {category: [] for category in CATEGORY_ORDER}
    for product in candidates:
        category = str(product.get("category", ""))
        if category in by_category:
            by_category[category].append(product)

    for items in by_category.values():
        items.sort(key=lambda item: (to_int(item.get("clone_risk_score"), 100), to_int(item.get("price"), 0)))

    selected: List[Dict[str, object]] = []
    for category in REQUIRED_CATEGORIES:
        items = by_category.get(category) or []
        if items:
            selected.append(items[0])

    total = sum(to_int(item.get("price"), 0) for item in selected)
    for category in OPTIONAL_CATEGORIES:
        items = by_category.get(category) or []
        for item in items:
            price = to_int(item.get("price"), 0)
            if total + price <= budget:
                selected.append(item)
                total += price
                break

    while len(selected) > 3 and sum(to_int(item.get("price"), 0) for item in selected) > budget:
        selected.pop()

    if sum(to_int(item.get("price"), 0) for item in selected) <= budget:
        return selected

    best: List[Dict[str, object]] = []
    best_score: Tuple[int, int] | None = None
    tops = by_category.get("top", [])[:8]
    bottoms = by_category.get("bottom", [])[:8]
    shoes = by_category.get("shoes", [])[:8]
    for top in tops:
        for bottom in bottoms:
            for shoe in shoes:
                combo = [top, bottom, shoe]
                price = sum(to_int(item.get("price"), 0) for item in combo)
                if price > budget:
                    continue
                risk = sum(to_int(item.get("clone_risk_score"), 100) for item in combo)
                score_key = (risk, price)
                if best_score is None or score_key < best_score:
                    best = combo
                    best_score = score_key
    return best


def write_recommendation(
    outfit: List[Dict[str, object]],
    request: Dict[str, object],
    out_dir: str,
) -> str:
    os.makedirs(out_dir, exist_ok=True)
    user = request.get("user", {})
    total_price = sum(to_int(item.get("price"), 0) for item in outfit)
    recommendation = {
        "user_request": user,
        "total_price_krw": total_price,
        "budget_krw": user.get("budget_krw"),
        "budget_ok": total_price <= to_int(user.get("budget_krw"), 0),
        "items": [
            {
                "product_id": item.get("product_id"),
                "brand": item.get("brand"),
                "name": item.get("name"),
                "category": item.get("category"),
                "price": to_int(item.get("price"), 0),
                "clone_risk_score": to_int(item.get("clone_risk_score"), 100),
                "why_less_common_but_wearable": less_common_reason(item, {"clone_risk_score": str(item.get("clone_risk_score"))}),
            }
            for item in outfit
        ],
    }
    output_path = os.path.join(out_dir, "recommendation.json")
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(recommendation, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return output_path


def write_report(
    outfit: List[Dict[str, object]],
    request: Dict[str, object],
    scores: Dict[str, Dict[str, str]],
    out_dir: str,
) -> str:
    os.makedirs(out_dir, exist_ok=True)
    user = request.get("user", {})
    total_price = sum(to_int(item.get("price"), 0) for item in outfit)
    budget = to_int(user.get("budget_krw"), 0)
    all_scores = [to_int(row.get("clone_risk_score"), 0) for row in scores.values()]
    average_score = round(sum(all_scores) / len(all_scores), 1) if all_scores else 0
    outfit_average = round(
        sum(to_int(item.get("clone_risk_score"), 0) for item in outfit) / len(outfit), 1
    ) if outfit else 0

    lines = [
        "# Clone-look Risk and Style Diversity Report",
        "",
        "## User Request",
        "",
        f"- Gender: {user.get('gender')}",
        f"- Height: {user.get('height_cm')} cm",
        f"- Occasion: {user.get('occasion')}",
        f"- Divergence level: {user.get('divergence_level')}",
        f"- Budget: {budget:,} KRW",
        "",
        "## Avoided Style Factors",
        "",
    ]
    for avoid in user.get("avoid", []):
        lines.append(f"- {avoid}")

    lines.extend(
        [
            "",
            "## Clone Risk Summary",
            "",
            f"- Products scored: {len(scores)}",
            f"- Average local clone risk: {average_score}/100",
            f"- Recommended outfit average risk: {outfit_average}/100",
            "- Products with direct avoid conflicts were excluded from the outfit.",
            "",
            "## Recommended Outfit",
            "",
        ]
    )

    if not outfit:
        lines.append("No complete outfit could be generated within budget from the filtered data.")
    for item in outfit:
        lines.extend(
            [
                f"### {item.get('category')} - {item.get('brand')} {item.get('name')}",
                "",
                f"- Product ID: {item.get('product_id')}",
                f"- Price: {to_int(item.get('price'), 0):,} KRW",
                f"- Clone Risk Score: {to_int(item.get('clone_risk_score'), 100)}/100",
                f"- Details: {product_summary(item)}",
                f"- Why it works: {less_common_reason(item, {'clone_risk_score': str(item.get('clone_risk_score'))})}",
                "",
            ]
        )

    lines.extend(
        [
            "## Why This Outfit Feels Less Common",
            "",
            "The outfit keeps familiar summer-date categories while shifting away from the highest-saturation clone signals: black wide bottoms, oversized graphic tops, German army sneakers, and default minimal black accessories. Texture, softer colors, and controlled silhouettes make it different without making it hard to wear.",
            "",
            "## Budget Check",
            "",
            f"- Total: {total_price:,} KRW",
            f"- Budget: {budget:,} KRW",
            f"- Status: {'within budget' if total_price <= budget else 'over budget'}",
            "",
            "## Human Review Notes",
            "",
            "This report uses heuristic local scoring rather than live trend data. A human reviewer should check fit, exact sizing, availability, and whether the user's real wardrobe already contains similar pieces.",
            "",
        ]
    )

    output_path = os.path.join(out_dir, "musinsa_smell_removal_report.md")
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an outfit recommendation report.")
    parser.add_argument("--products", required=True)
    parser.add_argument("--scores", required=True)
    parser.add_argument("--request", required=True)
    parser.add_argument("--out-dir", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    products = read_products(args.products)
    scores = read_scores(args.scores)
    request = read_request(args.request)
    avoid_terms = request.get("user", {}).get("avoid", [])
    candidates = candidate_products(products, scores, avoid_terms)
    outfit = choose_outfit(candidates, to_int(request.get("user", {}).get("budget_krw"), 0))
    recommendation_path = write_recommendation(outfit, request, args.out_dir)
    report_path = write_report(outfit, request, scores, args.out_dir)
    print(f"Wrote {recommendation_path}")
    print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
