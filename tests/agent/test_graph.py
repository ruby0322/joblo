import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from alignment_engine.agent.graph import (  # noqa: E402
    AgentState,
    run_decision_node,
)


class GraphDecisionNodeTests(unittest.TestCase):
    def test_run_decision_node_triggers_optimizer_when_score_above_threshold(self) -> None:
        state = AgentState(user_id="u1", job_id="j1", match_score=0.81)
        updated_state = run_decision_node(state=state, threshold=0.7)

        self.assertEqual(updated_state.next_action, "resume_optimize")
        self.assertEqual(updated_state.decision_reason, "score_above_threshold")

    def test_run_decision_node_discards_when_score_not_above_threshold(self) -> None:
        state = AgentState(user_id="u1", job_id="j1", match_score=0.7)
        updated_state = run_decision_node(state=state, threshold=0.7)

        self.assertEqual(updated_state.next_action, "discard_or_log")
        self.assertEqual(updated_state.decision_reason, "score_not_above_threshold")


if __name__ == "__main__":
    unittest.main()
