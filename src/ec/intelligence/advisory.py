from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


@dataclass(frozen=True, slots=True)
class AdvisoryEvidence:
    label: str
    value: str
    source: str


@dataclass(frozen=True, slots=True)
class AdvisoryAssessment:
    title: str
    severity: str
    diagnosis: str
    recommendation: str
    expected_impact: str
    evidence: tuple[AdvisoryEvidence, ...]
    confidence: float
    authority_notice: str = (
        "Advisory only — an authorized human/policy must decide; "
        "EVO must validate and authorize any business execution."
    )


def assess_order_delay_risk(observation: Mapping[str, Any]) -> AdvisoryAssessment:
    """Produce the Sprint-0 APM advisory assessment from governed observation facts.

    This function deliberately does not execute a command or mutate enterprise truth.
    It only interprets supplied facts and returns an evidence-grounded consultant view.
    """
    order = str(observation["sales_order"])
    promise_date = str(observation["promise_date"])
    supplier_eta = str(observation["current_supplier_eta"])
    alternate_eta = str(observation["alternate_supplier_eta"])
    revenue_at_risk = float(observation["revenue_at_risk"])
    alternate_cost_delta_pct = float(observation["alternate_cost_delta_pct"])
    current_late_days = int(observation["current_supplier_late_days"])
    alternate_buffer_days = int(observation["alternate_supplier_buffer_days"])

    evidence: Sequence[AdvisoryEvidence] = (
        AdvisoryEvidence("Sales order", order, "EVO observation"),
        AdvisoryEvidence("Customer promise date", promise_date, "EVO observation"),
        AdvisoryEvidence("Current supplier ETA", supplier_eta, "EVO observation"),
        AdvisoryEvidence("Current supplier lateness", f"{current_late_days} days", "derived from EVO observation"),
        AdvisoryEvidence("Alternate supplier ETA", alternate_eta, "EVO observation"),
        AdvisoryEvidence("Alternate schedule buffer", f"{alternate_buffer_days} days", "derived from EVO observation"),
        AdvisoryEvidence("Revenue at risk", f"${revenue_at_risk:,.0f}", "EVO observation"),
        AdvisoryEvidence("Alternate supplier cost delta", f"+{alternate_cost_delta_pct:.1f}%", "EVO observation"),
    )

    severity = "critical" if current_late_days >= 2 and revenue_at_risk >= 250_000 else "high"
    diagnosis = (
        f"{order} has material delivery risk: the current supplier is expected "
        f"{current_late_days} days beyond the customer promise date, placing "
        f"approximately ${revenue_at_risk:,.0f} of revenue at risk."
    )
    recommendation = (
        "Review a governed switch to the qualified alternate supplier before the "
        "procurement decision window closes. Do not execute automatically."
    )
    expected_impact = (
        f"If approved and operational assumptions hold, the alternate ETA restores "
        f"approximately {alternate_buffer_days} days of schedule buffer at an "
        f"estimated +{alternate_cost_delta_pct:.1f}% supplier cost delta."
    )

    return AdvisoryAssessment(
        title="Order delay risk requires management review",
        severity=severity,
        diagnosis=diagnosis,
        recommendation=recommendation,
        expected_impact=expected_impact,
        evidence=tuple(evidence),
        confidence=0.93,
    )
