import unittest


from tests._path_setup import add_alignment_engine_src

add_alignment_engine_src()

from alignment_engine.agent.flow import (  # noqa: E402
    MatchResult,
    build_resume_optimizer_payload,
    should_trigger_resume_optimizer,
)


class FlowDecisionTests(unittest.TestCase):
    def test_should_trigger_resume_optimizer_when_score_above_threshold(self) -> None:
        self.assertTrue(should_trigger_resume_optimizer(score=0.82, threshold=0.7))

    def test_should_not_trigger_resume_optimizer_when_score_equals_threshold(self) -> None:
        self.assertFalse(should_trigger_resume_optimizer(score=0.7, threshold=0.7))


class ResumePayloadTests(unittest.TestCase):
    def test_build_resume_optimizer_payload_contains_constraints_and_summary(self) -> None:
        match_result = MatchResult(
            score=0.82,
            skill_overlap=["python", "fastapi"],
            missing_skills=["system design"],
            reasoning="Strong backend overlap.",
        )

        payload = build_resume_optimizer_payload(
            user_id="user-123",
            job_id="job-456",
            match_result=match_result,
        )

        self.assertEqual(payload["user_id"], "user-123")
        self.assertEqual(payload["job_id"], "job-456")
        self.assertEqual(payload["match_score"], 0.82)
        self.assertIn("python, fastapi", payload["changes_summary"])
        self.assertIn("system design", payload["changes_summary"])
        self.assertEqual(payload["constraints"]["invent_experience"], False)
        self.assertEqual(payload["constraints"]["allowed_actions"], ["reframe", "reorder", "highlight_keywords"])


if __name__ == "__main__":
    unittest.main()
