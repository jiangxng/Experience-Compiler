import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from ec.learning.import_mapping import (
    ImportMappingExperienceServiceV010,
    ImportMappingExperienceV010,
    ImportMappingRecommendationRequestV010,
)
from ec.storage.sqlite import SqliteKnowledgeRepository


class SqliteThreadSafetyTests(unittest.TestCase):
    def test_import_mapping_learning_and_recommendation_work_from_worker_threads(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = SqliteKnowledgeRepository(
                Path(directory) / "thread-safe-knowledge.sqlite"
            )
            service = ImportMappingExperienceServiceV010(repository)
            experience = ImportMappingExperienceV010(
                contract_version="0.1.0",
                tenant_id="proof-tenant",
                target_id="counterparty.subject",
                source_column="编码",
                target_field_id="code",
                source_headers=("名称", "编码", "地址"),
                import_job_id="proof-import-1",
                target_schema_digest="schema-a",
                human_confirmed=True,
                dry_run_passed=True,
                commit_succeeded=True,
                observed_at="2026-10-08T08:13:29Z",
            )
            request = ImportMappingRecommendationRequestV010(
                contract_version="0.1.0",
                tenant_id="proof-tenant",
                target_id="counterparty.subject",
                source_columns=("联系电话", "编码", "客户名称", "开户行"),
                available_target_field_ids=("code", "displayName", "phone"),
                target_schema_digest="schema-b",
            )

            try:
                with ThreadPoolExecutor(max_workers=2) as executor:
                    observation, pattern = executor.submit(
                        service.observe_success,
                        experience,
                    ).result()
                    recommendations = executor.submit(
                        service.recommend,
                        request,
                    ).result()

                self.assertTrue(observation.record_id)
                self.assertTrue(pattern.record_id)
                self.assertEqual(len(recommendations), 1)
                self.assertEqual(recommendations[0].source_column, "编码")
                self.assertEqual(recommendations[0].target_field_id, "code")
                self.assertEqual(recommendations[0].confidence, 0.90)
            finally:
                repository.close()


if __name__ == "__main__":
    unittest.main()
