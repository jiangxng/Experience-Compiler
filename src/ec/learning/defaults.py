from ec.learning.model import LearningStrategy

def external_regulation_strategy() -> LearningStrategy:
    return LearningStrategy(
        strategy_id="external-regulation-research",
        version="1.0.0",
        name="External regulation research",
        applicable_domains=("*",),
        applicable_knowledge_kinds=("claim", "fact", "policy", "rule"),
        source_priority=("regulator-primary", "official-gazette", "standards-body", "court-or-enforcement", "industry-association", "secondary"),
        minimum_independent_sources=2,
        freshness_days=30,
        contradiction_policy="preserve-all-claims-and-escalate",
        confidence_threshold=0.90,
        stop_conditions=("primary-authority-confirmed", "material-contradictions-resolved", "budget-exhausted"),
        review_policy="human-review-before-high-impact-policy-promotion",
        steps=(
            "identify jurisdiction and effective date",
            "retrieve primary text and amendment history",
            "extract atomic claims with citations",
            "cross-check authoritative interpretation",
            "resolve temporal applicability",
            "record contradictions explicitly",
            "promote only with provenance and confidence",
        ),
    )

def case_outcome_learning_strategy() -> LearningStrategy:
    return LearningStrategy(
        strategy_id="case-outcome-learning",
        version="1.0.0",
        name="Case decision outcome learning",
        applicable_domains=("*",),
        applicable_knowledge_kinds=("case", "decision", "outcome", "lesson", "pattern"),
        source_priority=("evo-event", "human-evaluation", "system-measurement"),
        minimum_independent_sources=1,
        freshness_days=None,
        contradiction_policy="retain-cohorts-and-segment-before-generalizing",
        confidence_threshold=0.75,
        stop_conditions=("outcome-window-complete", "insufficient-outcome-data"),
        review_policy="automatic-candidate-human-or-policy-gated-promotion",
        steps=("bind situation", "record decision", "observe outcome", "normalize measures", "compare cohorts", "derive lesson", "evaluate repeatability", "promote pattern"),
    )
