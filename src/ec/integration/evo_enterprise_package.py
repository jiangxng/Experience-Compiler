from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol


@dataclass(frozen=True, slots=True)
class PackageCapabilities:
    supported_package_schema_versions: tuple[str, ...]
    supported_definition_kinds: tuple[str, ...]
    evo_runtime_version: str | None = None


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    message: str
    path: str | None = None
    definition_key: str | None = None


@dataclass(frozen=True, slots=True)
class ValidationResult:
    valid: bool
    package_schema_version: str
    issues: tuple[ValidationIssue, ...] = ()


class EvoEnterprisePackagePort(Protocol):
    """Public-contract-only boundary. Implementations must not import EVO private modules."""

    def get_capabilities(self) -> PackageCapabilities: ...

    def get_schema(self, version: str) -> Mapping[str, Any]: ...

    def validate(self, package: Mapping[str, Any]) -> ValidationResult: ...

    def plan(
        self,
        enterprise_id: str,
        package: Mapping[str, Any],
        *,
        expected_base_version: str | int | None = None,
    ) -> Mapping[str, Any]: ...

    def deploy(
        self,
        enterprise_id: str,
        package: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_base_version: str | int | None = None,
    ) -> Mapping[str, Any]: ...

    def export_definition_only(self, enterprise_id: str) -> Mapping[str, Any]: ...


class RuntimeIntegrationNotReady(RuntimeError):
    pass


class ContractOnlyEvoEnterprisePackageAdapter:
    """Development adapter while EVO HTTP runtime integration remains in progress.

    Schema/capabilities/compile-time certification can proceed. Network Validate/Plan/Deploy/Export
    deliberately fail rather than pretending the production runtime exists.
    """

    def __init__(
        self,
        *,
        schema: Mapping[str, Any],
        capabilities: PackageCapabilities,
    ) -> None:
        self._schema = dict(schema)
        self._capabilities = capabilities

    def get_capabilities(self) -> PackageCapabilities:
        return self._capabilities

    def get_schema(self, version: str) -> Mapping[str, Any]:
        if version not in self._capabilities.supported_package_schema_versions:
            raise KeyError(f"unsupported EVO Enterprise Package schema version: {version}")
        return dict(self._schema)

    def validate(self, package: Mapping[str, Any]) -> ValidationResult:
        raise RuntimeIntegrationNotReady("EVO authoritative network Validate is not wired yet")

    def plan(self, enterprise_id: str, package: Mapping[str, Any], *, expected_base_version=None):
        raise RuntimeIntegrationNotReady("EVO deterministic network Plan/Diff is not wired yet")

    def deploy(
        self,
        enterprise_id: str,
        package: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_base_version=None,
    ):
        raise RuntimeIntegrationNotReady("EVO governed network Deploy is not wired yet")

    def export_definition_only(self, enterprise_id: str):
        raise RuntimeIntegrationNotReady("EVO DEFINITION_ONLY network Export is not wired yet")
