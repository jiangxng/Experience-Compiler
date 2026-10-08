import unittest

from ec.learning.import_mapping import (
    ImportMappingExperienceServiceV010,
    ImportMappingExperienceV010,
    ImportMappingRecommendationRequestV010,
)
from ec.storage.memory import InMemoryKnowledgeRepository


class ImportMappingExperienceLearningTests(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryKnowledgeRepository()
        self.service = ImportMappingExperienceServiceV010(self.repo)

    def experience(
        self,
        *,
        tenant="enterprise-context:a",
        target="counterparty.subject",
        source="编码",
        target_field="code",
        job="import-1",
        headers=("名称", "编码", "地址"),
        human=True,
        dry=True,
        committed=True,
    ):
        return ImportMappingExperienceV010(
            contract_version="0.1.0",
            tenant_id=tenant,
            target_id=target,
            source_column=source,
            target_field_id=target_field,
            source_headers=tuple(headers),
            import_job_id=job,
            target_schema_digest="schema-a",
            human_confirmed=human,
            dry_run_passed=dry,
            commit_succeeded=committed,
            observed_at="2026-10-08T01:20:00Z",
        )

    def request(
        self,
        *,
        tenant="enterprise-context:a",
        target="counterparty.subject",
        columns=("联系电话", "编码", "客户名称", "开户行"),
        fields=("code", "displayName", "phone", "email"),
    ):
        return ImportMappingRecommendationRequestV010(
            contract_version="0.1.0",
            tenant_id=tenant,
            target_id=target,
            source_columns=tuple(columns),
            available_target_field_ids=tuple(fields),
            target_schema_digest="schema-b",
        )

    def test_human_confirmed_success_is_reused_across_different_table_structure(self):
        observation, pattern = self.service.observe_success(self.experience())

        self.assertEqual(observation.value["source_headers"], ["名称", "编码", "地址"])
        self.assertEqual(pattern.value["target_field_id"], "code")

        recommendations = self.service.recommend(self.request())

        self.assertEqual(len(recommendations), 1)
        recommendation = recommendations[0]
        self.assertEqual(recommendation.source_column, "编码")
        self.assertEqual(recommendation.target_field_id, "code")
        self.assertEqual(recommendation.confidence, 0.90)
        self.assertEqual(recommendation.support_count, 1)
        self.assertEqual(recommendation.conflict_count, 0)
        self.assertTrue(recommendation.advisory_only)

    def test_learning_is_tenant_scoped(self):
        self.service.observe_success(self.experience())
        recommendations = self.service.recommend(
            self.request(tenant="enterprise-context:b")
        )
        self.assertEqual(recommendations, ())

    def test_learning_is_target_object_scoped(self):
        self.service.observe_success(self.experience())
        recommendations = self.service.recommend(
            self.request(
                target="item.subject",
                fields=("code", "displayName"),
            )
        )
        self.assertEqual(recommendations, ())

    def test_unconfirmed_or_unsuccessful_mapping_cannot_be_learned(self):
        with self.assertRaisesRegex(
            ValueError,
            "IMPORT_MAPPING_HUMAN_CONFIRMATION_REQUIRED",
        ):
            self.service.observe_success(self.experience(human=False))

        with self.assertRaisesRegex(ValueError, "IMPORT_MAPPING_DRY_RUN_PASS_REQUIRED"):
            self.service.observe_success(self.experience(dry=False))

        with self.assertRaisesRegex(
            ValueError,
            "IMPORT_MAPPING_COMMIT_SUCCESS_REQUIRED",
        ):
            self.service.observe_success(self.experience(committed=False))

    def test_unavailable_target_field_is_never_recommended(self):
        self.service.observe_success(self.experience())
        recommendations = self.service.recommend(
            self.request(fields=("displayName", "phone"))
        )
        self.assertEqual(recommendations, ())

    def test_conflicting_equal_evidence_fails_closed(self):
        self.service.observe_success(self.experience(job="import-1"))
        self.service.observe_success(
            self.experience(target_field="displayName", job="import-2")
        )
        recommendations = self.service.recommend(self.request())
        self.assertEqual(recommendations, ())


if __name__ == "__main__":
    unittest.main()
