from __future__ import annotations

from ec.intelligence.advisory import assess_order_delay_risk


def apm_observation() -> dict[str, object]:
    """Small deterministic fixture shaped as facts EC expects from EVO Observation."""
    return {
        "enterprise": "Apex Precision Manufacturing",
        "customer": "Northstar Industrial Systems",
        "sales_order": "SO-20260918-0182",
        "product": "Critical Servo Module",
        "promise_date": "2026-09-18",
        "current_supplier_eta": "2026-09-20",
        "current_supplier_late_days": 2,
        "alternate_supplier": "Qualified Supplier B",
        "alternate_supplier_eta": "2026-09-15",
        "alternate_supplier_buffer_days": 3,
        "alternate_cost_delta_pct": 8.4,
        "revenue_at_risk": 280000,
    }


def run() -> dict[str, object]:
    observation = apm_observation()
    assessment = assess_order_delay_risk(observation)
    return {
        "enterprise": observation["enterprise"],
        "role": "Supply-chain / operations consultant",
        "status": "ADVISORY_ONLY",
        "assessment": {
            "title": assessment.title,
            "severity": assessment.severity,
            "diagnosis": assessment.diagnosis,
            "recommendation": assessment.recommendation,
            "expected_impact": assessment.expected_impact,
            "confidence": assessment.confidence,
            "authority_notice": assessment.authority_notice,
            "evidence": [
                {"label": item.label, "value": item.value, "source": item.source}
                for item in assessment.evidence
            ],
        },
    }
