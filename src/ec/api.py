from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

from ec.learning.import_mapping import (
    ImportMappingExperienceServiceV010,
    ImportMappingExperienceV010,
    ImportMappingRecommendationRequestV010,
)
from ec.storage.sqlite import SqliteKnowledgeRepository


class MappingExperiencePayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    contract_version: str = Field(alias="contractVersion")
    tenant_id: str = Field(alias="tenantId")
    target_id: str = Field(alias="targetId")
    source_column: str = Field(alias="sourceColumn")
    target_field_id: str = Field(alias="targetFieldId")
    source_headers: list[str] = Field(alias="sourceHeaders")
    import_job_id: str = Field(alias="importJobId")
    target_schema_digest: str = Field(alias="targetSchemaDigest")
    human_confirmed: bool = Field(alias="humanConfirmed")
    dry_run_passed: bool = Field(alias="dryRunPassed")
    commit_succeeded: bool = Field(alias="commitSucceeded")
    observed_at: str = Field(alias="observedAt")
    target_parameters: dict[str, Any] | None = Field(
        default=None,
        alias="targetParameters",
    )


class MappingRecommendationRequestPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    contract_version: str = Field(alias="contractVersion")
    tenant_id: str = Field(alias="tenantId")
    target_id: str = Field(alias="targetId")
    source_columns: list[str] = Field(alias="sourceColumns")
    available_target_field_ids: list[str] = Field(alias="availableTargetFieldIds")
    target_schema_digest: str = Field(alias="targetSchemaDigest")
    target_parameters: dict[str, Any] | None = Field(
        default=None,
        alias="targetParameters",
    )


def _repository() -> SqliteKnowledgeRepository:
    path = Path(os.getenv("EC_SQLITE_PATH", "/data/ec-knowledge.sqlite"))
    path.parent.mkdir(parents=True, exist_ok=True)
    return SqliteKnowledgeRepository(path)


repository = _repository()
service = ImportMappingExperienceServiceV010(repository)
app = FastAPI(
    title="Experience Compiler Advisory API",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "experience-compiler"}


@app.post("/v1/data-import/mapping-experiences")
def observe_mapping_experience(
    payload: MappingExperiencePayload,
) -> dict[str, Any]:
    observation, pattern = service.observe_success(
        ImportMappingExperienceV010(
            contract_version=payload.contract_version,
            tenant_id=payload.tenant_id,
            target_id=payload.target_id,
            source_column=payload.source_column,
            target_field_id=payload.target_field_id,
            source_headers=tuple(payload.source_headers),
            import_job_id=payload.import_job_id,
            target_schema_digest=payload.target_schema_digest,
            human_confirmed=payload.human_confirmed,
            dry_run_passed=payload.dry_run_passed,
            commit_succeeded=payload.commit_succeeded,
            observed_at=payload.observed_at,
            target_parameters=payload.target_parameters,
        )
    )
    return {
        "contractVersion": "0.1.0",
        "observationRecordId": observation.record_id,
        "patternRecordId": pattern.record_id,
        "status": "RECORDED",
    }


@app.post("/v1/data-import/mapping-recommendations")
def recommend_mappings(
    payload: MappingRecommendationRequestPayload,
) -> dict[str, Any]:
    recommendations = service.recommend(
        ImportMappingRecommendationRequestV010(
            contract_version=payload.contract_version,
            tenant_id=payload.tenant_id,
            target_id=payload.target_id,
            source_columns=tuple(payload.source_columns),
            available_target_field_ids=tuple(payload.available_target_field_ids),
            target_schema_digest=payload.target_schema_digest,
            target_parameters=payload.target_parameters,
        )
    )
    return {
        "contractVersion": "0.1.0",
        "recommendations": [
            {
                "sourceColumn": item.source_column,
                "targetFieldId": item.target_field_id,
                "confidence": item.confidence,
                "supportCount": item.support_count,
                "conflictCount": item.conflict_count,
                "supportingRecordIds": list(item.supporting_record_ids),
                "rationale": item.rationale,
                "advisoryOnly": item.advisory_only,
            }
            for item in recommendations
        ],
    }
