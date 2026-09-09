"""Regression coverage for requirements-to-architecture blocker consistency."""
import tempfile
import unittest
from pathlib import Path
from validate_workflow_trace import validate


class ArchitectureHandoffTests(unittest.TestCase):
    def check_trace(self, requirement_status, blocker):
        text = (
            "| Item | Type | Status | Current activity | Evidence | Missing or blocked | Next action |\n"
            "|---|---|---|---|---|---|---|\n"
            f"| Initial requirements | Initial Release | {requirement_status} | Product Requirements Management | requirements.md | None | Run d-design-product-architecture |\n"
            f"| Architecture | Initial Release | Not Started | Product Architecture Design | requirements.md | {blocker} | Run d-design-product-architecture |\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trace.md"
            path.write_text(text)
            return validate(path, False)

    def test_stale_blocker_rejected(self):
        result = self.check_trace("Complete", "Approved requirements missing")
        self.assertFalse(result["passed"])
        self.assertIn("stale blocker", " ".join(result["errors"]))

    def test_pending_requirements_allowed(self):
        self.assertTrue(self.check_trace("Not Started", "Approved requirements missing")["passed"])

    def test_ready_handoff_allowed(self):
        self.assertTrue(self.check_trace("Complete", "Architecture baseline not created")["passed"])

    def test_other_blocker_preserved(self):
        self.assertTrue(self.check_trace("Complete", "Architect review required")["passed"])


if __name__ == "__main__":
    unittest.main()
