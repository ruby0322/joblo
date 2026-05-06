import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from tests._path_setup import add_alignment_engine_src

add_alignment_engine_src()

from alignment_engine.db.models import Base  # noqa: E402
from alignment_engine.db.repository import JobRepository, UserRepository  # noqa: E402


class RepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def tearDown(self) -> None:
        self.session.close()
        self.engine.dispose()

    def test_user_repository_creates_user(self) -> None:
        user_repo = UserRepository(self.session)
        created = user_repo.create_user(email="dev@example.com")
        self.assertEqual(created.email, "dev@example.com")
        self.assertIsNotNone(created.id)

    def test_job_repository_upserts_by_source_and_url(self) -> None:
        job_repo = JobRepository(self.session)
        first = job_repo.upsert_job(
            title="Backend Engineer",
            company="ACME",
            location="Remote",
            description="Python",
            source="manual",
            url="https://example.com/job/1",
        )
        second = job_repo.upsert_job(
            title="Senior Backend Engineer",
            company="ACME",
            location="Remote",
            description="Python and SQL",
            source="manual",
            url="https://example.com/job/1",
        )

        self.assertEqual(first.id, second.id)
        self.assertEqual(second.title, "Senior Backend Engineer")

    def test_job_repository_lists_jobs(self) -> None:
        job_repo = JobRepository(self.session)
        job_repo.upsert_job(
            title="ML Engineer",
            company="Beta",
            location="Taipei",
            description="ML systems",
            source="manual",
            url="https://example.com/job/2",
        )
        jobs = job_repo.list_jobs()
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].company, "Beta")


if __name__ == "__main__":
    unittest.main()
