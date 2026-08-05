# musinsa-smell-remover

Use this skill when the user wants a Codex workflow for Musinsa-scale fashion platform data that reduces clone-look risk and improves style-content diversity from local product, ranking, review, and request files.

This is not a generic fashion chatbot, brand critique, or shopping app. Do not invent products, browse shopping pages, or give taste-only advice. This is a data-driven clone-look risk and style-diversity workflow that reads local product, ranking, review, and user request files, calculates Clone Risk Score, filters avoided style factors, and writes reproducible output files for human review.

## Required inputs

Read these files before recommending anything:

- `examples/products.csv`
- `examples/rankings.csv`
- `examples/reviews.csv`
- `examples/user_request.json`

The user request contains budget, occasion, divergence level, and avoid keywords. Treat `avoid` entries as hard conflict signals for direct product matches.

## Required outputs

Write all of these files:

- `outputs/clone_risk_scores.csv`
- `outputs/recommendation.json`
- `outputs/musinsa_smell_removal_report.md`

## Workflow

1. Read the required input files.
2. Identify avoided style factors from `user_request.json`.
3. Calculate Clone Risk Score for every product from ranking, popularity, review commonness, avoid keyword matches, common style signals, material, color, and silhouette.
4. Filter out items that conflict with avoid keywords.
5. Recommend a balanced 3 to 5 item outfit candidate for style-content review within budget.
6. Explain why each recommendation is less common but still wearable for the occasion.
7. Save machine-readable outputs and a human-readable Markdown report.

## Clone Risk Score guidance

The Clone Risk Score must be 0 to 100.

Increase risk when products have:

- High rank or high popularity score
- High `commonness_signal`
- Direct matches with user avoid keywords
- Common style signals such as black, gray, oversized, wide, basic, minimal, or street

Decrease risk when products have:

- Lower ranking or lower popularity
- Less common materials
- Non-overfit silhouettes
- Less saturated or less default color choices
- Lower `commonness_signal`

## Recommendation rules

- Never recommend products that directly conflict with avoid keywords.
- Prefer lower clone risk products while keeping the outfit wearable.
- Balance categories such as top, bottom, shoes, bag, and accessory.
- Keep the total price within `budget_krw`.
- Explain why each item reduces clone-look risk without becoming costume-like or difficult to wear.
- Include human review notes because the scoring model is heuristic and local-data based.
