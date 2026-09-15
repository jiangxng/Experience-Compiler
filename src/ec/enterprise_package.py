from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence


EVO_ENTERPRISE_PACKAGE_V01_COMMIT = "d18fac50f0fc1bb29d9728fd6c5730463f8aeb71"
EVO_ENTERPRISE_PACKAGE_V01_SCHEMA_PATH = "contracts/enterprise-package-v0.1.schema.json"
EVO_ENTERPRISE_PACKAGE_V01_SCHEMA_SHA = "14a78892776746487759134124c0d90ae91faf36"


@dataclass(frozen=True, slots=True)
class EvoPackageContractPin:
    repository: str = "jiangxng/EVO"
    commit: str = EVO_ENTERPRISE_PACKAGE_V01_COMMIT
    schema_path: str = EVO_ENTERPRISE_PACKAGE_V01_SCHEMA_PATH
    schema_blob_sha: str = EVO_ENTERPRISE_PACKAGE_V01_SCHEMA_SHA
    package_schema_version: str = "0.1"


@dataclass(frozen=True, slots=True)
class DefinitionIntent:
    """EC-owned intent that must compile into the EVO-owned definition envelope."""

    kind: str
    key: str
    version: str | int
    spec: Mapping[str, Any]
    depends_on: Sequence[Mapping[str, Any]] = ()


@dataclass(frozen=True, slots=True)
class PackageIntent:
    package_id: str
    package_version: str
    name: str
    evo_runtime: str
    definitions: Sequence[DefinitionIntent]
    description: str | None = None
    requires_capabilities: Sequence[str] = ()
    dependencies: Sequence[Mapping[str, str]] = ()
    provenance: Mapping[str, Any] | None = None


class EnterprisePackageCompileError(ValueError):
    pass


class EnterprisePackageCompiler:
    """Compile EC intent to the EVO v0.1 package contract without redefining EVO semantics."""

    def __init__(self, *, supported_definition_kinds: Iterable[str]) -> None:
        self._supported_definition_kinds = frozenset(supported_definition_kinds)

    def compile(self, intent: PackageIntent) -> dict[str, Any]:
        definitions: list[dict[str, Any]] = []
        seen: set[tuple[str, str, str]] = set()

        for definition in intent.definitions:
            if definition.kind not in self._supported_definition_kinds:
                raise EnterprisePackageCompileError(
                    f"EVO contract does not advertise definition kind: {definition.kind}"
                )
            identity = (definition.kind, definition.key, str(definition.version))
            if identity in seen:
                raise EnterprisePackageCompileError(
                    f"duplicate definition identity: {definition.kind}/{definition.key}@{definition.version}"
                )
            seen.add(identity)
            compiled: dict[str, Any] = {
                "kind": definition.kind,
                "key": definition.key,
                "version": definition.version,
                "spec": dict(definition.spec),
            }
            if definition.depends_on:
                compiled["dependsOn"] = [dict(ref) for ref in definition.depends_on]
            definitions.append(compiled)

        package: dict[str, Any] = {
            "packageSchemaVersion": "0.1",
            "packageId": intent.package_id,
            "packageVersion": intent.package_version,
            "name": intent.name,
            "compatibility": {
                "evoRuntime": intent.evo_runtime,
                "requiresCapabilities": list(intent.requires_capabilities),
            },
            "dependencies": [dict(dep) for dep in intent.dependencies],
            "definitions": definitions,
        }
        if intent.description is not None:
            package["description"] = intent.description
        if intent.provenance is not None:
            package["provenance"] = dict(intent.provenance)
        return package


def validate_package_structure(package: Mapping[str, Any], schema: Mapping[str, Any]) -> tuple[str, ...]:
    """Local developer feedback only. EVO Validate remains authoritative.

    The caller supplies the EVO-owned schema obtained from the pinned contract or schema discovery.
    EC deliberately does not embed a parallel package schema here.
    """
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:  # pragma: no cover - installation guidance
        raise RuntimeError(
            "local Enterprise Package validation requires the 'jsonschema' package"
        ) from exc

    validator = Draft202012Validator(schema)
    issues = sorted(validator.iter_errors(dict(package)), key=lambda error: list(error.path))
    return tuple(
        f"/{'/'.join(str(part) for part in issue.absolute_path)}: {issue.message}"
        for issue in issues
    )
