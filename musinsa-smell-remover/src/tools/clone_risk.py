#!/usr/bin/env python3
"""Calculate clone-look risk for local Musinsa-style product data."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
from typing import Dict, Iterable, List, Tuple

COMMON_STYLE_SIGNALS = {
    "black": 8,
    "gray": 6,
    "grey": 6,
    "oversized": 10,
    "wide": 8,
    "basic": 7,
    "minimal": 6,
    "street": 7,
    "logo": 5,
    "graphic": 8,
}

LESS_COMMON_MATERIALS = {
    "linen": -7,
    "linen blend": -7,
    "seersucker": -9,
    "ripstop": -6,
    "cotton ripstop": -6,
    "ripstop cotton": -6,
    "oiled leather": -5,
    "suede": -4,
    "tencel": -5,
    "cotton linen": -6,
    "linen knit": -8,
}

NON_OVERFIT_SILHOUETTES = {
    "regular": -7,
    "straight": -6,
    "tapered": -8,
    "slim": -5,
    "compact": -4,
}

LESS_SATURATED_COLORS = {
    "sage": -6,
    "ecru": -5,
    "brown": -4,
    "olive": -4,
    "indigo": -4,
    "khaki": -4,
    "cream": -3,
    "stone": -5,
    "navy": -3,
    "taupe": -6,
    "sand": -5,
    "natural": -5,
    "blue stripe": -4,
}

CATEGORY_ALIASES = {
    "bottom": "pants trousers slacks shorts",
    "top": "top tee t shirt tshirt shirt polo",
    "shoes": "shoes sneaker sneakers footwear",
    "bag": "bag tote crossbody shoulder",
    "accessory": "accessory cap bracelet",
}


def normalize(value: object) -> str:
    text = str(value or "").lower()
    return re.sub(r"[^a-z0-9가-힣]+", " ", text).strip()


def read_csv_by_id(path: str) -> Dict[str, Dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as handle:
        return {row["product_id"]: row for row in csv.DictReader(handle)}


def read_products(path: str) -> List[Dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_request(path: str) -> Dict[str, object]:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def product_search_text(product: Dict[str, str], review: Dict[str, str] | None = None) -> str:
    parts: List[str] = []
    for key in ("brand", "name", "category", "color", "silhouette", "material", "tags"):
        parts.append(product.get(key, ""))
    category = normalize(product.get("category"))
    if category in CATEGORY_ALIASES:
        parts.append(CATEGORY_ALIASES[category])
    if review:
        parts.append(review.get("review_keywords", ""))
    return normalize(" ".join(parts))


def avoid_conflicts(product: Dict[str, str], avoid_terms: Iterable[str], review: Dict[str, str] | None = None) -> List[str]:
    text = product_search_text(product, review)
    conflicts: List[str] = []
    for term in avoid_terms:
        normalized = normalize(term)
        if not normalized:
            continue
        tokens = [token for token in normalized.split() if len(token) > 1]
        phrase_match = normalized in text
        token_match = bool(tokens) and all(token in text.split() for token in tokens)
        if phrase_match or token_match:
            conflicts.append(term)
    return conflicts


def _float(row: Dict[str, str], key: str, default: float = 0.0) -> float:
    try:
        return float(row.get(key, default) or default)
    except ValueError:
        return default


def calculate_clone_risk(
    product: Dict[str, str],
    ranking: Dict[str, str] | None,
    review: Dict[str, str] | None,
    avoid_terms: Iterable[str],
) -> Tuple[int, List[str], List[str]]:
    ranking = ranking or {}
    review = review or {}
    reasons: List[str] = []
    score = 28.0

    rank = _float(ranking, "rank", 999.0)
    if rank <= 10:
        score += 23
        reasons.append("top-10 ranking strongly increases clone exposure")
    elif rank <= 30:
        score += 16
        reasons.append("top-30 ranking increases clone exposure")
    elif rank <= 75:
        score += 9
        reasons.append("visible ranking increases clone exposure")
    elif rank >= 120:
        score -= 8
        reasons.append("lower ranking reduces clone exposure")
    else:
        score -= 3
        reasons.append("mid-low ranking slightly reduces clone exposure")

    popularity = _float(ranking, "popularity_score", 0.0)
    popularity_delta = (popularity / 100.0) * 18.0
    score += popularity_delta
    if popularity >= 80:
        reasons.append("high popularity score adds risk")
    elif popularity <= 35:
        score -= 5
        reasons.append("low popularity score reduces risk")

    commonness = _float(review, "commonness_signal", 0.0)
    score += (commonness / 100.0) * 20.0
    if commonness >= 70:
        reasons.append("review commonness signal is high")
    elif commonness <= 35:
        score -= 7
        reasons.append("review commonness signal is low")

    conflicts = avoid_conflicts(product, avoid_terms, review)
    if conflicts:
        score += min(30, 16 + 7 * len(conflicts))
        reasons.append("matches avoided style factor: " + ", ".join(conflicts))

    text = product_search_text(product, review)
    words = set(text.split())
    for signal, weight in COMMON_STYLE_SIGNALS.items():
        if signal in words:
            score += weight
            reasons.append(f"common style signal: {signal}")

    material = normalize(product.get("material"))
    for material_signal, weight in LESS_COMMON_MATERIALS.items():
        if normalize(material_signal) in material:
            score += weight
            reasons.append(f"less common material lowers risk: {material_signal}")
            break

    silhouette = normalize(product.get("silhouette"))
    if silhouette in NON_OVERFIT_SILHOUETTES:
        score += NON_OVERFIT_SILHOUETTES[silhouette]
        reasons.append(f"non-overfit silhouette lowers risk: {silhouette}")

    color = normalize(product.get("color"))
    if color in LESS_SATURATED_COLORS:
        score += LESS_SATURATED_COLORS[color]
        reasons.append(f"less default color lowers risk: {color}")

    score = max(0, min(100, round(score)))
    return int(score), reasons, conflicts


def write_scores(
    products: List[Dict[str, str]],
    rankings: Dict[str, Dict[str, str]],
    reviews: Dict[str, Dict[str, str]],
    avoid_terms: Iterable[str],
    out_dir: str,
) -> str:
    os.makedirs(out_dir, exist_ok=True)
    output_path = os.path.join(out_dir, "clone_risk_scores.csv")
    fieldnames = [
        "product_id",
        "brand",
        "name",
        "category",
        "price",
        "clone_risk_score",
        "avoid_conflict",
        "score_reasons",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for product in products:
            product_id = product["product_id"]
            score, reasons, conflicts = calculate_clone_risk(
                product,
                rankings.get(product_id),
                reviews.get(product_id),
                avoid_terms,
            )
            writer.writerow(
                {
                    "product_id": product_id,
                    "brand": product.get("brand", ""),
                    "name": product.get("name", ""),
                    "category": product.get("category", ""),
                    "price": product.get("price", ""),
                    "clone_risk_score": score,
                    "avoid_conflict": "; ".join(conflicts),
                    "score_reasons": " | ".join(reasons),
                }
            )
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Calculate clone-look risk scores.")
    parser.add_argument("--products", required=True)
    parser.add_argument("--rankings", required=True)
    parser.add_argument("--reviews", required=True)
    parser.add_argument("--request", required=True)
    parser.add_argument("--out-dir", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    products = read_products(args.products)
    rankings = read_csv_by_id(args.rankings)
    reviews = read_csv_by_id(args.reviews)
    request = read_request(args.request)
    avoid_terms = request.get("user", {}).get("avoid", [])
    output_path = write_scores(products, rankings, reviews, avoid_terms, args.out_dir)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
