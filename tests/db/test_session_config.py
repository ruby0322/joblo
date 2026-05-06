import importlib
import os
import unittest
from unittest.mock import patch

from tests._path_setup import add_alignment_engine_src

add_alignment_engine_src()


class SessionConfigTests(unittest.TestCase):
    def test_database_url_uses_environment_override(self) -> None:
        with patch.dict(os.environ, {"DATABASE_URL": "sqlite+pysqlite:///./custom.db"}, clear=False):
            import alignment_engine.db.session as session_module  # noqa: E402

            session_module = importlib.reload(session_module)
            self.assertEqual(session_module.DATABASE_URL, "sqlite+pysqlite:///./custom.db")

    def test_database_url_uses_default_when_env_missing(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            import alignment_engine.db.session as session_module  # noqa: E402

            session_module = importlib.reload(session_module)
            self.assertEqual(session_module.DATABASE_URL, "sqlite+pysqlite:///./alignment_engine.db")


if __name__ == "__main__":
    unittest.main()
