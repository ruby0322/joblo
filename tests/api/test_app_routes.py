import sys
import unittest
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from alignment_engine.main import create_app  # noqa: E402


class AppRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(create_app())

    def test_resume_upload_returns_201_and_resume_id(self) -> None:
        payload = {"user_id": str(uuid4()), "content": {"skills": ["python"]}, "raw_text": "Python engineer"}
        response = self.client.post("/resume/upload", json=payload)
        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertIn("resume_id", body)

    def test_agent_run_returns_202_and_status(self) -> None:
        payload = {"user_id": str(uuid4()), "type": "manual", "input": {"source": "test"}}
        response = self.client.post("/agent/run", json=payload)
        self.assertEqual(response.status_code, 202)
        body = response.json()
        self.assertIn("run_id", body)
        self.assertEqual(body["status"], "queued")


if __name__ == "__main__":
    unittest.main()
