# guru-avatar

Use this skill when the user wants a Codex workflow for KakaoPay Securities-style beginner investor education content: turn local stock metrics and investor-philosophy templates into a beginner-friendly decision-support draft, then run prohibited-phrase lint before human review.

## What this is and is not

- This is **not** a stock recommendation tool. It never tells anyone to purchase, dispose of, or keep a security.
- This is **not** a buy, sell, or hold signal generator, and it never predicts future returns.
- This **is** an educational research-writing workflow. It translates investor philosophies (guru "lenses") into judgment questions a beginner can answer for themselves.
- Every output must be framed as **decision support, not financial advice**.
- Every output must always include risk factors, caution signals, counterarguments, and beginner self-check questions.

## Hard rules

- Never output buy, sell, or hold recommendations, and never use directive phrasing such as "buy now", "sell now", "strong buy", "must buy", "must sell", or their Korean equivalents.
- Never promise, guarantee, or forecast returns.
- Always present both supporting signals and caution signals for each lens.
- Always run the prohibited-phrase lint before finalizing, and only treat the output as a human-review draft when no explicit prohibited phrases are detected.

## Required inputs

Read these files before writing anything:

- `examples/stock_metrics.csv`
- `examples/public_holdings.csv`
- `examples/guru_lenses.json`
- `examples/user_profile.json`

## Required outputs

Write all of these files:

- `outputs/guru_avatar_report.md`
- `outputs/guru_avatar_report.json`
- `outputs/investor_questions.md`
- `outputs/compliance_check.md`

## Workflow

1. Read the target ticker from `user_profile.json` (`target_ticker`).
2. Read the stock metrics for that ticker from `stock_metrics.csv`.
3. Read the guru lens definitions from `guru_lenses.json` and the public-holdings context from `public_holdings.csv`.
4. Generate a lens-by-lens educational analysis. For each lens and each criterion include:
   - What this lens checks
   - Supporting signals
   - Caution signals
   - Questions for the investor
5. Include supporting signals, caution signals, and investor questions for every lens.
6. Include a Beginner Safety Check section of honest self-check questions.
7. Include a Next Actions section limited to safe, non-directive steps only:
   - add to watchlist
   - paper trading / mock tracking
   - review after next earnings
   - compare position size
   - compare alternative stocks in the same sector
8. Run prohibited-phrase lint on the Markdown report before finalizing; if it reports risky phrases, revise and re-run before human review.

## How to run the tools

Generate the report:

```
python src/tools/guru_lens.py \
  --metrics src/examples/stock_metrics.csv \
  --holdings src/examples/public_holdings.csv \
  --lenses src/examples/guru_lenses.json \
  --profile src/examples/user_profile.json \
  --out-dir src/outputs
```

Check compliance:

```
python src/tools/compliance_check.py \
  --report src/outputs/guru_avatar_report.md \
  --out src/outputs/compliance_check.md
```

## Framing note

The scoring is heuristic and based only on local sample data. Always remind the reader to verify figures with primary sources and to treat the report as a starting point for their own study, not as advice.
