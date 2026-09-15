import unittest

from ec.enterprise_package import (
    EVO_ENTERPRISE_PACKAGE_V01_COMMIT,
    DefinitionIntent,
    EnterprisePackageCompileError,
    EnterprisePackageCompiler,
    PackageIntent,
)
from ec.integration.evo_enterprise_package import (
    ContractOnlyEvoEnterprisePackageAdapter,
    PackageCapabilities,
    RuntimeIntegrationNotReady,
)


SUPPORTED_KINDS = (
    "enterprise",
    "domain",
    "transaction-type",
    "application-definition",
    "field-group",
    "field-definition",
    "command-definition",
    "capability-definition",
    "flow-definition",
    "sop-definition",
    "metric-definition",
    "dimension-definition",
    "ledger-definition",
    "posting-rule",
    "cost-policy",
    "valuation-policy",
    "authorization-template",
)


class EnterprisePackageV01Tests(unittest.TestCase):
    def test_contract_is_pinned_to_evo_handoff_commit(self):
        self.assertEqual(
            EVO_ENTERPRISE_PACKAGE_V01_COMMIT,
            "d18fac50f0fc1bb29d9728fd6c5730463f8aeb71",
        )

    def test_compiler_emits_evo_owned_v01_envelope(self):
        compiler = EnterprisePackageCompiler(supported_definition_kinds=SUPPORTED_KINDS)
        package = compiler.compile(
            PackageIntent(
                package_id="ec.apm.reference",
                package_version="0.1.0",
                name="APM Reference Enterprise Package",
                evo_runtime="1.x",
                requires_capabilities=("enterprise-package-v0.1",),
                definitions=(
                    DefinitionIntent(
                        kind="enterprise",
                        key="apm",
                        version="1",
                        spec={"name": "Apex Precision Manufacturing"},
                    ),
                    DefinitionIntent(
                        kind="domain",
                        key="procurement",
                        version="1",
                        depends_on=(
                            {"kind": "enterprise", "key": "apm", "version": "1"},
                        ),
                        spec={"name": "Procurement"},
                    ),
                ),
                provenance={"source": "EC", "sourceVersion": "sprint0"},
            )
        )
        self.assertEqual(package["packageSchemaVersion"], "0.1")
        self.assertEqual(package["definitions"][1]["dependsOn"][0]["key"], "apm")
        self.assertNotIn("businessData", package)
        self.assertNotIn("ledgerEntries", package)

    def test_unknown_definition_kind_fails_closed(self):
        compiler = EnterprisePackageCompiler(supported_definition_kinds=SUPPORTED_KINDS)
        with self.assertRaises(EnterprisePackageCompileError):
            compiler.compile(
                PackageIntent(
                    package_id="bad",
                    package_version="1",
                    name="bad",
                    evo_runtime="1.x",
                    definitions=(
                        DefinitionIntent("ec-invented-kind", "x", "1", {}),
                    ),
                )
            )

    def test_contract_only_adapter_does_not_fake_runtime_readiness(self):
        adapter = ContractOnlyEvoEnterprisePackageAdapter(
            schema={"$id": "urn:evo:enterprise-package:0.1"},
            capabilities=PackageCapabilities(("0.1",), SUPPORTED_KINDS, "contract-only"),
        )
        self.assertEqual(adapter.get_schema("0.1")["$id"], "urn:evo:enterprise-package:0.1")
        with self.assertRaises(RuntimeIntegrationNotReady):
            adapter.deploy("apm", {}, idempotency_key="test")


if __name__ == "__main__":
    unittest.main()
