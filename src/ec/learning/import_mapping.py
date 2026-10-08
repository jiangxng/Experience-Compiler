from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from ec.domain import EvidenceRef, Provenance, Scope, ScopeKind, new_id
from ec.knowledge.model import KnowledgeKind, KnowledgeRecord, KnowledgeStatus
from ec.ports import KnowledgeRepository


def _required(value: str, code: str) -> str:
    normalized = value.strip() if isinstance(value, str) else ""
    if not normalized:
        raise ValueError(code)
    return normalized


def normalize_source_term(value: str) -> str:
    """Normalize source-field wording without inventing semantic aliases."""
    return "".join(
        ch for ch in _required(value, "IMPORT_MAPPING_SOURCE_COLUMN_REQUIRED").casefold()
        if not ch.isspace() and ch not in "_-/()[]{}.:："
    )


@dataclass(frozen=True, slots=True)
class ImportMappingExperienceV010:
    contract_version: str
    tenant_id: str
    target_id: str
    source_column: str
    target_field_id: str
    source_headers: tuple[str, ...]
    import_job_id: str
    target_schema_digest: str
    human_confirmed: bool
    dry_run_passed: bool
    commit_succeeded: bool
    observed_at: str
    target_parameters: Mapping[str, Any] | None = None

    def validate(self) -> "ImportMappingExperienceV010":
        if self.contract_version != "0.1.0":
            raise ValueError("IMPORT_MAPPING_EXPERIENCE_VERSION_INVALID")
        _required(self.tenant_id, "IMPORT_MAPPING_TENANT_REQUIRED")
        _required(self.target_id, "IMPORT_MAPPING_TARGET_REQUIRED")
        _required(self.source_column, "IMPORT_MAPPING_SOURCE_COLUMN_REQUIRED")
        _required(self.target_field_id, "IMPORT_MAPPING_TARGET_FIELD_REQUIRED")
        _required(self.import_job_id, "IMPORT_MAPPING_JOB_REQUIRED")
        _required(self.target_schema_digest, "IMPORT_MAPPING_SCHEMA_DIGEST_REQUIRED")
        _required(self.observed_at, "IMPORT_MAPPING_OBSERVED_AT_REQUIRED")
        if not self.source_headers:
            raise ValueError("IMPORT_MAPPING_SOURCE_HEADERS_REQUIRED")
        if not self.human_confirmed:
            raise ValueError("IMPORT_MAPPING_HUMAN_CONFIRMATION_REQUIRED")
        if not self.dry_run_passed:
            raise ValueError("IMPORT_MAPPING_DRY_RUN_PASS_REQUIRED")
        if not self.commit_succeeded:
            raise ValueError("IMPORT_MAPPING_COMMIT_SUCCESS_REQUIRED")
        return self


@dataclass(frozen=True, slots=True)
class ImportMappingRecommendationV010:
    source_column: str
    target_field_id: str
    confidence: float
    support_count: int
    conflict_count: int
    supporting_record_ids: tuple[str, ...]
    rationale: str
    advisory_only: bool = True


@dataclass(frozen=True, slots=True)
class ImportMappingRecommendationRequestV010:
    contract_version: str
    tenant_id: str
    target_id: str
    source_columns: tuple[str, ...]
    available_target_field_ids: tuple[str, ...]
    target_schema_digest: str
    target_parameters: Mapping[str, Any] | None = None

    def validate(self) -> "ImportMappingRecommendationRequestV010":
        if self.contract_version != "0.1.0":
            raise ValueError("IMPORT_MAPPING_RECOMMENDATION_VERSION_INVALID")
        _required(self.tenant_id, "IMPORT_MAPPING_TENANT_REQUIRED")
        _required(self.target_id, "IMPORT_MAPPING_TARGET_REQUIRED")
        _required(self.target_schema_digest, "IMPORT_MAPPING_SCHEMA_DIGEST_REQUIRED")
        if not self.source_columns:
            raise ValueError("IMPORT_MAPPING_SOURCE_COLUMNS_REQUIRED")
        if not self.available_target_field_ids:
            raise ValueError("IMPORT_MAPPING_TARGET_FIELDS_REQUIRED")
        return self


class ImportMappingExperienceServiceV010:
    """Tenant-scoped advisory learning for data-import field mappings.

    EC owns the learned experience. EVO remains the execution authority.
    A single successful Human-confirmed mapping is enough to create a
    tenant-scoped candidate pattern that EC may recommend later, but never
    enough to create universal/global truth.
    """

    def __init__(self, repository: KnowledgeRepository) -> None:
        self.repository = repository

    @staticmethod
    def _subject(target_id: str, source_column: str) -> str:
        return (
            "data-import-field:"
            + _required(target_id, "IMPORT_MAPPING_TARGET_REQUIRED")
            + ":"
            + normalize_source_term(source_column)
        )

    def observe_success(
        self,
        experience: ImportMappingExperienceV010,
    ) -> tuple[KnowledgeRecord, KnowledgeRecord]:
        experience.validate()
        run_id = new_id()
        scope = Scope(
            kind=ScopeKind.TENANT,
            key=experience.tenant_id,
            tenant_id=experience.tenant_id,
        )
        evidence = EvidenceRef(
            evidence_id=f"evo-import-job:{experience.import_job_id}",
            uri=(
                f"evo://{experience.tenant_id}/data-import/jobs/"
                f"{experience.import_job_id}"
            ),
            source_class="governed-runtime-evidence",
            publisher="EVO App Platform",
        )
        observation = KnowledgeRecord(
            kind=KnowledgeKind.CASE,
            subject=self._subject(experience.target_id, experience.source_column),
            predicate="human-confirmed-successful-mapping",
            value={
                "target_id": experience.target_id,
                "source_column": experience.source_column,
                "normalized_source_column": normalize_source_term(
                    experience.source_column
                ),
                "target_field_id": experience.target_field_id,
                "source_headers": list(experience.source_headers),
                "target_schema_digest": experience.target_schema_digest,
                "target_parameters": dict(experience.target_parameters or {}),
                "import_job_id": experience.import_job_id,
                "observed_at": experience.observed_at,
            },
            scope=scope,
            confidence=1.0,
            status=KnowledgeStatus.CANDIDATE,
            tags=("data-import", "mapping", "human-confirmed", "successful"),
            provenance=Provenance(
                actor_type="system",
                actor_id="evo-app-platform",
                method="human-confirmed-successful-import",
                run_id=run_id,
                evidence=(evidence,),
            ),
        )
        self.repository.append(observation)

        pattern = KnowledgeRecord(
            kind=KnowledgeKind.PATTERN,
            subject=observation.subject,
            predicate="maps-to-target-field",
            value={
                "target_id": experience.target_id,
                "source_column": experience.source_column,
                "normalized_source_column": normalize_source_term(
                    experience.source_column
                ),
                "target_field_id": experience.target_field_id,
                "target_schema_digest": experience.target_schema_digest,
            },
            scope=scope,
            confidence=0.90,
            status=KnowledgeStatus.CANDIDATE,
            tags=("data-import", "field-semantic-pattern", "tenant-scoped"),
            provenance=Provenance(
                actor_type="system",
                actor_id="experience-compiler",
                method="derive-field-mapping-pattern-from-confirmed-outcome",
                run_id=run_id,
                parent_record_ids=(observation.record_id,),
            ),
        )
        self.repository.append(pattern)
        return observation, pattern

    def recommend(
        self,
        request: ImportMappingRecommendationRequestV010,
    ) -> tuple[ImportMappingRecommendationV010, ...]:
        request.validate()
        available_targets = set(request.available_target_field_ids)
        patterns = self.repository.query(
            tenant_id=request.tenant_id,
            kinds=(KnowledgeKind.PATTERN.value,),
            limit=5000,
        )
        recommendations: list[ImportMappingRecommendationV010] = []

        for source_column in request.source_columns:
            subject = self._subject(request.target_id, source_column)
            matching = [
                record
                for record in patterns
                if record.subject == subject
                and record.predicate == "maps-to-target-field"
                and isinstance(record.value, dict)
                and record.value.get("target_id") == request.target_id
                and record.value.get("target_field_id") in available_targets
                and record.status not in {
                    KnowledgeStatus.SUPERSEDED,
                    KnowledgeStatus.QUARANTINED,
                    KnowledgeStatus.ARCHIVED,
                }
            ]
            if not matching:
                continue

            by_target: dict[str, list[KnowledgeRecord]] = {}
            for record in matching:
                target = str(record.value["target_field_id"])
                by_target.setdefault(target, []).append(record)

            ranked = sorted(
                by_target.items(),
                key=lambda item: (-len(item[1]), item[0]),
            )
            best_target, support_records = ranked[0]
            support_count = len(support_records)
            conflict_count = sum(
                len(records) for target, records in ranked[1:] if target != best_target
            )
            next_support = len(ranked[1][1]) if len(ranked) > 1 else 0

            # Fail closed on an unresolved tie. EC may surface ambiguity later,
            # but must not pretend a stable learned mapping exists.
            if next_support == support_count:
                continue

            confidence = min(
                0.99,
                max(0.0, 0.90 + 0.02 * (support_count - 1) - 0.15 * conflict_count),
            )
            recommendations.append(
                ImportMappingRecommendationV010(
                    source_column=source_column,
                    target_field_id=best_target,
                    confidence=confidence,
                    support_count=support_count,
                    conflict_count=conflict_count,
                    supporting_record_ids=tuple(
                        record.record_id for record in support_records
                    ),
                    rationale=(
                        f"{support_count} Human-confirmed successful import "
                        f"experience(s) in tenant scope support this mapping"
                        + (
                            f"; {conflict_count} conflicting experience(s) exist"
                            if conflict_count
                            else ""
                        )
                    ),
                )
            )

        return tuple(recommendations)
