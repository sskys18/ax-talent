#!/usr/bin/env python3
"""Turn stock metrics and guru philosophy templates into a beginner-friendly
educational judgment report.

This tool is educational decision support only. It never emits buy, sell, or
hold recommendations and never predicts future returns. It reads local files,
applies each guru "lens" as a set of judgment questions, and writes reproducible
Markdown and JSON outputs.

Standard library only. No pandas, no external APIs, no live prices.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from typing import Callable, Dict, List, Optional

DISCLAIMER = (
    "This report is educational decision support, not financial advice. It does "
    "not tell you to purchase, dispose of, or keep any security, and it does not "
    "forecast future returns. All figures come from a local sample file and may "
    "be out of date. Verify every number against primary sources and consult a "
    "licensed professional before making any decision."
)

DEFENSIVE_SECTORS = {"Beverages", "Retail", "Consumer Staples", "Utilities", "Healthcare"}
CYCLICAL_SECTORS = {"Semiconductors", "Automotive", "Banking", "E-Commerce"}
COMPLEX_SECTORS = {"Semiconductors", "Banking", "Software"}

METRIC_FIELDS = [
    "revenue_growth",
    "operating_margin",
    "pe_ratio",
    "free_cash_flow",
    "price_change_6m",
    "debt_ratio",
    "dividend_yield",
    "volatility",
]


# --------------------------------------------------------------------------- #
# Input readers
# --------------------------------------------------------------------------- #
def read_metrics(path: str) -> Dict[str, Dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as handle:
        return {row["ticker"].strip().upper(): row for row in csv.DictReader(handle)}


def read_holdings(path: str) -> List[Dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_json(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


# --------------------------------------------------------------------------- #
# Formatting helpers
# --------------------------------------------------------------------------- #
def to_float(value: object, default: float = 0.0) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return default


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def numeric_metrics(row: Dict[str, str]) -> Dict[str, float]:
    return {field: to_float(row.get(field)) for field in METRIC_FIELDS}


# --------------------------------------------------------------------------- #
# Per-criterion evaluators
# Each evaluator returns a dict:
#   what_it_checks, supporting_signals, caution_signals, investor_questions
# --------------------------------------------------------------------------- #
def _result(what: str) -> Dict[str, object]:
    return {
        "what_it_checks": what,
        "supporting_signals": [],
        "caution_signals": [],
        "investor_questions": [],
    }


def eval_moat(m: Dict[str, float], ctx: dict) -> Dict[str, object]:
    r = _result("Whether the company shows a durable competitive advantage, often visible as a consistently high operating margin.")
    om = m["operating_margin"]
    if om >= 0.25:
        r["supporting_signals"].append(f"Operating margin of {pct(om)} suggests pricing power that can support a moat.")
    if om < 0.15:
        r["caution_signals"].append(f"Operating margin of {pct(om)} is thin, which may signal limited pricing power.")
    r["investor_questions"] += [
        "Can you explain in one sentence why competitors cannot easily copy this business?",
        "Has the margin been stable across several years, not just the latest one?",
    ]
    return r


def eval_cash_flow(m: Dict[str, float], ctx: dict) -> Dict[str, object]:
    r = _result("Whether the business generates real free cash flow, not just accounting profit.")
    fcf = m["free_cash_flow"]
    if fcf >= 5:
        r["supporting_signals"].append(f"Reported free cash flow of ${fcf:g}B indicates the business can fund itself from operations.")
    if fcf <= 1:
        r["caution_signals"].append(f"Free cash flow of ${fcf:g}B is low or not meaningful for this business type; confirm how the sector reports cash.")
    r["investor_questions"] += [
        "Where does the cash actually come from, and is it recurring?",
        "Is free cash flow growing or shrinking over recent years?",
    ]
    return r


def eval_margin_of_safety(m: Dict[str, float], ctx: dict) -> Dict[str, object]:
    r = _result("Whether today's price leaves room for error versus a conservative estimate of value, roughly approximated by the P/E ratio.")
    pe = m["pe_ratio"]
    if pe and pe < 20:
        r["supporting_signals"].append(f"A P/E of {pe:g} is relatively modest, which may leave more room for error.")
    if pe >= 35:
        r["caution_signals"].append(f"A P/E of {pe:g} is high, so the price already assumes strong future results.")
    r["investor_questions"] += [
        "What has to go right for the company to justify today's price?",
        "How far could the price fall if growth slows, and could you tolerate that?",
    ]
    return r


def eval_quality(m: Dict[str, float], ctx: dict) -> Dict[str, object]:
    r = _result("Overall business quality inferred from profitability and balance-sheet strength.")
    om, debt = m["operating_margin"], m["debt_ratio"]
    if om >= 0.20 and debt < 0.40:
        r["supporting_signals"].append(f"High margin ({pct(om)}) with a modest debt ratio ({pct(debt)}) points to a financially sturdy business.")
    if debt > 0.50:
        r["caution_signals"].append(f"Debt ratio of {pct(debt)} is elevated; understand how it behaves when rates rise.")
    r["investor_questions"].append("Would this business survive a bad year in its industry without distress?")
    return r


def eval_understandable_story(m: Dict[str, float], ctx: dict) -> Dict[str, object]:
    sector = ctx["sector"]
    r = _result("Whether a beginner can clearly explain what the company sells and how it earns money.")
    if sector in DEFENSIVE_SECTORS or sector in {"Consumer Electronics", "E-Commerce"}:
        r["supporting_signals"].append(f"The {sector} business model is often approachable for beginners.")
    if sector in COMPLEX_SECTORS:
        r["caution_signals"].append(f"The {sector} model can be complex; make sure you truly understand it before leaning on this analysis.")
    r["investor_questions"] += [
        "Can you explain this company to a friend in about 30 seconds?",
        "Do you personally use or understand its products?",
    ]
    return r


def eval_growth(m: Dict[str, float], ctx: dict) -> Dict[str, object]:
    r = _result("Whether revenue is expanding and how fast.")
    g = m["revenue_growth"]
    if g >= 0.15:
        r["supporting_signals"].append(f"Revenue growth of {pct(g)} is strong.")
    if g < 0.05:
        r["caution_signals"].append(f"Revenue growth of {pct(g)} is slow; the story may depend on factors other than growth.")
    r["investor_questions"] += [
        "Is the growth coming from new customers, price increases, or one-time effects?",
        f"Could this growth rate realistically hold over your {ctx['time_horizon']} horizon?",
    ]
    return r


def eval_valuation_versus_growth(m: Dict[str, float], ctx: dict) -> Dict[str, object]:
    r = _result("Whether the valuation is reasonable relative to growth, using a rough PEG-style sanity check.")
    pe, g = m["pe_ratio"], m["revenue_growth"]
    if g > 0:
        peg = pe / (g * 100)
        if peg < 1.5:
            r["supporting_signals"].append(f"P/E {pe:g} against growth {pct(g)} gives a rough PEG near {peg:.2f}, which is comparatively balanced.")
        if peg > 2.5:
            r["caution_signals"].append(f"P/E {pe:g} against growth {pct(g)} gives a rough PEG near {peg:.2f}, which looks stretched.")
    else:
        r["caution_signals"].append(f"With flat or negative growth ({pct(g)}), the P/E of {pe:g} cannot be justified by growth alone.")
    r["investor_questions"].append("If the growth rate halved, would the valuation still make sense to you?")
    return r


def eval_macro_cycle(m: Dict[str, float], ctx: dict) -> Dict[str, object]:
    sector = ctx["sector"]
    r = _result("How the company might behave across different phases of the economic cycle.")
    if sector in DEFENSIVE_SECTORS:
        r["supporting_signals"].append(f"As a {sector} name, demand may stay relatively steady across cycles.")
    if sector in CYCLICAL_SECTORS:
        r["caution_signals"].append(f"{sector} results can swing sharply with the economic cycle.")
    r["investor_questions"].append("In a recession, would people spend more or less on this product?")
    return r


def eval_diversification(m: Dict[str, float], ctx: dict) -> Dict[str, object]:
    r = _result("Whether adding this ticker would keep your overall portfolio balanced.")
    vol = m["volatility"]
    if vol > 0.35:
        r["caution_signals"].append(f"A single high-volatility name (volatility {pct(vol)}) can dominate a small portfolio.")
    r["investor_questions"] += [
        "What percent of your total portfolio would this position be?",
        f"Do you already own similar companies in {ctx['sector']}?",
    ]
    return r


def eval_interest_rate_sensitivity(m: Dict[str, float], ctx: dict) -> Dict[str, object]:
    r = _result("How sensitive the company may be to changes in interest rates.")
    pe, debt = m["pe_ratio"], m["debt_ratio"]
    if pe > 30:
        r["caution_signals"].append(f"High-valuation names like this (P/E {pe:g}) can be sensitive to rising rates.")
    if debt > 0.50:
        r["caution_signals"].append(f"Elevated debt ({pct(debt)}) raises interest-rate sensitivity.")
    if debt < 0.20 and pe and pe < 20:
        r["supporting_signals"].append(f"Low debt ({pct(debt)}) and a modest valuation reduce rate sensitivity.")
    r["investor_questions"].append("If interest rates rose sharply, how might this stock be affected?")
    return r


def eval_trend(m: Dict[str, float], ctx: dict) -> Dict[str, object]:
    r = _result("The recent price trend over the last six months.")
    ch = m["price_change_6m"]
    if ch > 0.10:
        r["supporting_signals"].append(f"Price is up {pct(ch)} over six months, an uptrend by this simple measure.")
    if ch < -0.05:
        r["caution_signals"].append(f"Price is down {pct(ch)} over six months.")
    r["caution_signals"].append("Past price movement does not indicate future price movement.")
    r["investor_questions"].append("Are you reacting to the recent price move rather than to the business itself?")
    return r


def eval_price_action(m: Dict[str, float], ctx: dict) -> Dict[str, object]:
    r = _result("Whether recent price action looks stable or erratic.")
    vol = m["volatility"]
    if vol < 0.25:
        r["supporting_signals"].append(f"Volatility of {pct(vol)} is relatively contained.")
    if vol > 0.40:
        r["caution_signals"].append(f"Volatility of {pct(vol)} is high; expect large swings in both directions.")
    r["investor_questions"].append("Could you stay calm if this dropped 30% in a single month?")
    return r


def eval_market_reaction(m: Dict[str, float], ctx: dict) -> Dict[str, object]:
    r = _result("How strongly the market tends to react to news for this name.")
    vol = m["volatility"]
    if vol > 0.40:
        r["caution_signals"].append(f"High volatility ({pct(vol)}) suggests sharp reactions to news.")
    r["caution_signals"].append("Market reaction to future news is unpredictable.")
    r["investor_questions"].append("Do you have a plan for what you would do on a large down day?")
    return r


def eval_dividend_stability(m: Dict[str, float], ctx: dict) -> Dict[str, object]:
    r = _result("Whether the stock pays a stable, meaningful dividend.")
    dy = m["dividend_yield"]
    if dy >= 0.02:
        r["supporting_signals"].append(f"Dividend yield of {pct(dy)} provides some income and often signals cash discipline.")
    if dy < 0.005:
        r["caution_signals"].append(f"Dividend yield of {pct(dy)} is minimal; income is not a meaningful part of the case here.")
    r["investor_questions"].append("Are you here for income, growth, or both, and does this stock match that?")
    return r


def eval_defensive_quality(m: Dict[str, float], ctx: dict) -> Dict[str, object]:
    sector = ctx["sector"]
    r = _result("Whether the stock tends to be defensive during downturns.")
    vol = m["volatility"]
    if vol < 0.20 and sector in DEFENSIVE_SECTORS:
        r["supporting_signals"].append(f"Low volatility ({pct(vol)}) in a {sector} business suggests defensive characteristics.")
    if vol > 0.35:
        r["caution_signals"].append(f"Volatility of {pct(vol)} is not defensive.")
    r["investor_questions"].append("Do you need this position to be stable, and does the data support that expectation?")
    return r


CRITERION_EVALUATORS: Dict[str, Callable[[Dict[str, float], dict], Dict[str, object]]] = {
    "moat": eval_moat,
    "cash flow": eval_cash_flow,
    "margin of safety": eval_margin_of_safety,
    "quality": eval_quality,
    "understandable story": eval_understandable_story,
    "growth": eval_growth,
    "valuation versus growth": eval_valuation_versus_growth,
    "macro cycle": eval_macro_cycle,
    "diversification": eval_diversification,
    "interest rate sensitivity": eval_interest_rate_sensitivity,
    "trend": eval_trend,
    "price action": eval_price_action,
    "market reaction": eval_market_reaction,
    "dividend stability": eval_dividend_stability,
    "defensive quality": eval_defensive_quality,
}


def evaluate_criterion(name: str, m: Dict[str, float], ctx: dict) -> Dict[str, object]:
    evaluator = CRITERION_EVALUATORS.get(name.strip().lower())
    if evaluator is None:
        result = _result(f"Judgment question about '{name}'.")
        result["investor_questions"].append(f"How does '{name}' apply to this company in your own words?")
        return result
    result = evaluator(m, ctx)
    result["criterion"] = name
    return result


# --------------------------------------------------------------------------- #
# Report assembly
# --------------------------------------------------------------------------- #
def build_report(
    ticker: str,
    metrics: Dict[str, Dict[str, str]],
    holdings: List[Dict[str, str]],
    lenses: dict,
    profile: dict,
) -> dict:
    ticker = ticker.strip().upper()
    if ticker not in metrics:
        raise SystemExit(
            f"Target ticker '{ticker}' not found in metrics file. Available: "
            + ", ".join(sorted(metrics))
        )

    row = metrics[ticker]
    m = numeric_metrics(row)
    ctx = {
        "sector": row.get("sector", "Unknown"),
        "time_horizon": profile.get("time_horizon", "your"),
    }

    guru_holdings = [
        {
            "guru_name": h.get("guru_name", ""),
            "holding_weight": h.get("holding_weight", ""),
            "reported_quarter": h.get("reported_quarter", ""),
            "notes": h.get("notes", ""),
        }
        for h in holdings
        if h.get("ticker", "").strip().upper() == ticker
    ]

    lens_reports = []
    for lens in lenses.get("lenses", []):
        criteria_reports = [
            evaluate_criterion(name, m, ctx) for name in lens.get("criteria", [])
        ]
        lens_reports.append(
            {
                "name": lens.get("name", "Unnamed Lens"),
                "philosophy": lens.get("philosophy", ""),
                "criteria": criteria_reports,
            }
        )

    beginner_safety_check = [
        "Can you explain what this company does without using jargon?",
        f"Would you be comfortable if this position fell 30% during your {ctx['time_horizon']} horizon?",
        f"Is this money you will not need during your {ctx['time_horizon']} horizon?",
        "Would this position be a reasonable share of your portfolio, not an oversized bet?",
        "Are you deciding from data and process, not from fear of missing out?",
        f"As a self-described {profile.get('experience', 'beginner')} investor with "
        f"{profile.get('risk_tolerance', 'unknown')} risk tolerance, does this fit your plan?",
    ]

    next_actions = [
        "Add this ticker to a watchlist and observe it over time.",
        "Track it with paper trading or mock tracking instead of real money first.",
        "Review the case again after the next earnings release.",
        "Compare an appropriate position size against the rest of your portfolio.",
        f"Compare alternative stocks in the same sector ({ctx['sector']}).",
    ]

    return {
        "target_ticker": ticker,
        "company": row.get("company", ""),
        "sector": ctx["sector"],
        "profile": profile,
        "metrics": {**{"ticker": ticker}, **{k: m[k] for k in METRIC_FIELDS}},
        "guru_holdings": guru_holdings,
        "lenses": lens_reports,
        "beginner_safety_check": beginner_safety_check,
        "next_actions": next_actions,
        "disclaimer": DISCLAIMER,
    }


# --------------------------------------------------------------------------- #
# Renderers
# --------------------------------------------------------------------------- #
def render_markdown(report: dict) -> str:
    lines: List[str] = []
    lines.append(f"# Guru Avatar Judgment Report: {report['company']} ({report['target_ticker']})")
    lines.append("")
    lines.append("> Educational decision support only. Not financial advice. "
                 "No purchase, disposal, or keep recommendation is given and no future return is predicted.")
    lines.append("")
    lines.append(f"- Sector: {report['sector']}")
    prof = report["profile"]
    lines.append(f"- Investor profile: {prof.get('experience', '?')} experience, "
                 f"{prof.get('risk_tolerance', '?')} risk tolerance, {prof.get('time_horizon', '?')} horizon")
    lines.append("")

    lines.append("## Snapshot Metrics")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("| --- | --- |")
    m = report["metrics"]
    lines.append(f"| Revenue growth | {pct(m['revenue_growth'])} |")
    lines.append(f"| Operating margin | {pct(m['operating_margin'])} |")
    lines.append(f"| P/E ratio | {m['pe_ratio']:g} |")
    lines.append(f"| Free cash flow | ${m['free_cash_flow']:g}B |")
    lines.append(f"| Price change (6m) | {pct(m['price_change_6m'])} |")
    lines.append(f"| Debt ratio | {pct(m['debt_ratio'])} |")
    lines.append(f"| Dividend yield | {pct(m['dividend_yield'])} |")
    lines.append(f"| Volatility | {pct(m['volatility'])} |")
    lines.append("")

    lines.append("## Guru Public Holdings Context")
    lines.append("")
    if report["guru_holdings"]:
        lines.append("These are illustrative public-filing references, not signals to act:")
        lines.append("")
        for h in report["guru_holdings"]:
            lines.append(f"- **{h['guru_name']}** ({h['reported_quarter']}), weight {h['holding_weight']}: {h['notes']}")
    else:
        lines.append("No guru in the sample file reported a position in this ticker.")
    lines.append("")

    lines.append("## Lens-by-Lens Educational Analysis")
    lines.append("")
    for lens in report["lenses"]:
        lines.append(f"### {lens['name']}")
        lines.append("")
        if lens["philosophy"]:
            lines.append(f"_{lens['philosophy']}_")
            lines.append("")
        for crit in lens["criteria"]:
            lines.append(f"#### {crit['criterion']}")
            lines.append("")
            lines.append(f"**What this lens checks:** {crit['what_it_checks']}")
            lines.append("")
            lines.append("**Supporting signals:**")
            if crit["supporting_signals"]:
                for s in crit["supporting_signals"]:
                    lines.append(f"- {s}")
            else:
                lines.append("- No clear supporting signal from the available data.")
            lines.append("")
            lines.append("**Caution signals:**")
            if crit["caution_signals"]:
                for s in crit["caution_signals"]:
                    lines.append(f"- {s}")
            else:
                lines.append("- No clear caution signal from the available data.")
            lines.append("")
            lines.append("**Questions for the investor:**")
            for q in crit["investor_questions"]:
                lines.append(f"- {q}")
            lines.append("")

    lines.append("## Beginner Safety Check")
    lines.append("")
    lines.append("Answer these honestly for yourself before doing anything:")
    lines.append("")
    for q in report["beginner_safety_check"]:
        lines.append(f"- [ ] {q}")
    lines.append("")

    lines.append("## Next Actions (safe, non-directive)")
    lines.append("")
    lines.append("None of these are recommendations to trade; they are ways to keep learning:")
    lines.append("")
    for a in report["next_actions"]:
        lines.append(f"- {a}")
    lines.append("")

    lines.append("## Disclaimer")
    lines.append("")
    lines.append(report["disclaimer"])
    lines.append("")

    return "\n".join(lines)


def render_investor_questions(report: dict) -> str:
    lines: List[str] = []
    lines.append(f"# Investor Questions: {report['company']} ({report['target_ticker']})")
    lines.append("")
    lines.append("Use these questions to build your own judgment. They are prompts, not answers.")
    lines.append("")
    for lens in report["lenses"]:
        lines.append(f"## {lens['name']}")
        lines.append("")
        for crit in lens["criteria"]:
            lines.append(f"### {crit['criterion']}")
            for q in crit["investor_questions"]:
                lines.append(f"- {q}")
            lines.append("")
    lines.append("## Beginner Safety Check")
    lines.append("")
    for q in report["beginner_safety_check"]:
        lines.append(f"- {q}")
    lines.append("")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a beginner-friendly guru-lens judgment report.")
    parser.add_argument("--metrics", required=True, help="Path to stock_metrics.csv")
    parser.add_argument("--holdings", required=True, help="Path to public_holdings.csv")
    parser.add_argument("--lenses", required=True, help="Path to guru_lenses.json")
    parser.add_argument("--profile", required=True, help="Path to user_profile.json")
    parser.add_argument("--out-dir", required=True, help="Directory for generated outputs")
    parser.add_argument("--ticker", default=None, help="Override target ticker (defaults to profile)")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)

    metrics = read_metrics(args.metrics)
    holdings = read_holdings(args.holdings)
    lenses = read_json(args.lenses)
    profile = read_json(args.profile)

    ticker = args.ticker or profile.get("target_ticker")
    if not ticker:
        raise SystemExit("No target ticker found: pass --ticker or set target_ticker in the profile.")

    report = build_report(ticker, metrics, holdings, lenses, profile)

    os.makedirs(args.out_dir, exist_ok=True)
    md_path = os.path.join(args.out_dir, "guru_avatar_report.md")
    json_path = os.path.join(args.out_dir, "guru_avatar_report.json")
    questions_path = os.path.join(args.out_dir, "investor_questions.md")

    with open(md_path, "w", encoding="utf-8") as handle:
        handle.write(render_markdown(report))
    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
    with open(questions_path, "w", encoding="utf-8") as handle:
        handle.write(render_investor_questions(report))

    print(f"Wrote {md_path}")
    print(f"Wrote {json_path}")
    print(f"Wrote {questions_path}")


if __name__ == "__main__":
    main()
