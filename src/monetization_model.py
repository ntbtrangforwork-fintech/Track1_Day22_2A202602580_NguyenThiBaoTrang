"""Reproducible unit-economics model for the Day 22 assignment."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Assumptions:
    attempts: int = 1_000
    completion_rate: float = 0.92
    audio_minutes: float = 12.0
    fx_vnd_per_usd: float = 26_000.0
    stt_usd_per_minute: float = 0.0045
    fresh_input_tokens: int = 6_500
    cached_input_tokens: int = 2_500
    output_tokens: int = 1_000
    llm_input_usd_per_million: float = 0.75
    llm_cached_usd_per_million: float = 0.075
    llm_output_usd_per_million: float = 4.50
    retry_rate: float = 0.08
    infra_usd_per_attempt: float = 0.012
    observability_usd_per_attempt: float = 0.008
    qa_sample_rate: float = 0.03
    qa_minutes: float = 3.0
    qa_hourly_usd: float = 6.0
    included_jobs: int = 200
    minimum_monthly_vnd: float = 1_990_000.0
    overage_vnd_per_job: float = 10_000.0
    typical_completed_jobs: int = 360
    payback_months: int = 12
    ae_annual_quota_vnd: float = 2_400_000_000.0
    ae_workdays: int = 240
    cost_per_opportunity_vnd: float = 2_250_000.0
    win_rate: float = 0.30
    customer_lifetime_months: int = 18


def calculate(a: Assumptions) -> dict[str, float]:
    if not 0 < a.completion_rate <= 1:
        raise ValueError("completion_rate must be in (0, 1]")
    if not 0 < a.win_rate <= 1:
        raise ValueError("win_rate must be in (0, 1]")
    if a.attempts <= 0 or a.included_jobs <= 0 or a.typical_completed_jobs <= 0:
        raise ValueError("volumes must be positive")

    stt = a.audio_minutes * a.stt_usd_per_minute
    llm_fresh = a.fresh_input_tokens / 1_000_000 * a.llm_input_usd_per_million
    llm_cached = a.cached_input_tokens / 1_000_000 * a.llm_cached_usd_per_million
    llm_output = a.output_tokens / 1_000_000 * a.llm_output_usd_per_million
    api = stt + llm_fresh + llm_cached + llm_output
    retry = api * a.retry_rate
    qa = a.qa_sample_rate * a.qa_minutes / 60 * a.qa_hourly_usd
    cost_per_attempt = (
        api + retry + a.infra_usd_per_attempt + a.observability_usd_per_attempt + qa
    )
    completed = a.attempts * a.completion_rate
    monthly_cogs_usd = a.attempts * cost_per_attempt
    cost_per_job_usd = monthly_cogs_usd / completed
    cost_per_job_vnd = cost_per_job_usd * a.fx_vnd_per_usd
    floor_vnd = 3 * cost_per_job_vnd

    overage_jobs = max(0, a.typical_completed_jobs - a.included_jobs)
    monthly_revenue_vnd = (
        a.minimum_monthly_vnd + overage_jobs * a.overage_vnd_per_job
    )
    effective_price_vnd = monthly_revenue_vnd / a.typical_completed_jobs
    gross_margin = 1 - cost_per_job_vnd / effective_price_vnd

    conservative_price_usd = (
        a.minimum_monthly_vnd / a.included_jobs / a.fx_vnd_per_usd
    )
    breakeven_completion_60gm = cost_per_attempt / (0.40 * conservative_price_usd)

    cac_budget_vnd = monthly_revenue_vnd * gross_margin * a.payback_months
    acv_vnd = monthly_revenue_vnd * 12
    deals_per_year = a.ae_annual_quota_vnd / acv_vnd
    deals_per_day = deals_per_year / a.ae_workdays
    estimated_cac_vnd = a.cost_per_opportunity_vnd / a.win_rate
    cac_headroom = cac_budget_vnd / estimated_cac_vnd
    ltv_cac = (
        monthly_revenue_vnd
        * gross_margin
        * a.customer_lifetime_months
        / estimated_cac_vnd
    )

    return {
        "stt_usd_per_attempt": stt,
        "llm_usd_per_attempt": llm_fresh + llm_cached + llm_output,
        "api_usd_per_attempt": api,
        "retry_usd_per_attempt": retry,
        "qa_usd_per_attempt": qa,
        "cost_per_attempt_usd": cost_per_attempt,
        "completed_jobs": completed,
        "monthly_cogs_usd": monthly_cogs_usd,
        "cost_per_job_usd": cost_per_job_usd,
        "cost_per_job_vnd": cost_per_job_vnd,
        "floor_vnd_per_job": floor_vnd,
        "monthly_revenue_vnd": monthly_revenue_vnd,
        "effective_price_vnd_per_job": effective_price_vnd,
        "gross_margin": gross_margin,
        "breakeven_completion_60gm": breakeven_completion_60gm,
        "cac_budget_vnd": cac_budget_vnd,
        "acv_vnd": acv_vnd,
        "deals_per_year": deals_per_year,
        "deals_per_day": deals_per_day,
        "estimated_cac_vnd": estimated_cac_vnd,
        "cac_headroom": cac_headroom,
        "ltv_cac": ltv_cac,
    }


def sensitivity(a: Assumptions) -> list[dict[str, float]]:
    price_vnd = a.minimum_monthly_vnd / a.included_jobs
    rows = []
    for rate in (0.50, 0.60, 0.70, 0.80, 0.90, 0.92, 0.95):
        scenario = calculate(Assumptions(**{**asdict(a), "completion_rate": rate}))
        rows.append(
            {
                "completion_rate": rate,
                "cost_per_job_vnd": scenario["cost_per_job_vnd"],
                "gross_margin": 1 - scenario["cost_per_job_vnd"] / price_vnd,
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    args = parser.parse_args()
    assumptions = Assumptions()
    output = {
        "assumptions": asdict(assumptions),
        "results": calculate(assumptions),
        "sensitivity": sensitivity(assumptions),
    }
    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return
    r = output["results"]
    print(f"Cost/Job: {r['cost_per_job_vnd']:,.0f} VND")
    print(f"Price floor: {r['floor_vnd_per_job']:,.0f} VND")
    print(f"Effective price: {r['effective_price_vnd_per_job']:,.0f} VND")
    print(f"Gross margin: {r['gross_margin']:.1%}")
    print(f"Breakeven completion at 60% GM: {r['breakeven_completion_60gm']:.1%}")


if __name__ == "__main__":
    main()

