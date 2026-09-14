import tempfile
import unittest
from pathlib import Path

from ec.storage.sqlite import SqliteKnowledgeRepository


class WindowsSqliteLifecycleTest(unittest.TestCase):
    def test_repository_releases_database_before_temp_directory_cleanup(self):
        with tempfile.TemporaryDirectory() as d:
            db_path = Path(d) / "ec.db"
            with SqliteKnowledgeRepository(db_path):
                self.assertTrue(db_path.exists())
            # Windows requires the SQLite handle to be released before unlink.
            db_path.unlink()
            self.assertFalse(db_path.exists())


if __name__ == "__main__":
    unittest.main()
