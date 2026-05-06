import unittest
from pathlib import Path

import yaml


class OpenAPIContractTests(unittest.TestCase):
    def test_openapi_contains_required_mvp_paths(self) -> None:
        spec = yaml.safe_load(Path("api/openapi.yaml").read_text(encoding="utf-8"))
        paths = spec["paths"]
        required_paths = {
            "/resume/upload",
            "/resume/{user_id}",
            "/jobs/ingest",
            "/jobs",
            "/match/run",
            "/resume/optimize",
            "/agent/run",
        }
        self.assertTrue(required_paths.issubset(paths.keys()))


if __name__ == "__main__":
    unittest.main()
