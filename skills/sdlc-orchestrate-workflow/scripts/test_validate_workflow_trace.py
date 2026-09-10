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


class ActiveIncrementTraceTests(unittest.TestCase):
    def validate_text(self, text):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trace.md"
            path.write_text(text)
            return validate(path, True)

    def test_historical_complete_downstream_rejected_when_later_increment_active(self):
        text = (
            "| Item | Type | Status | Current activity | Evidence | Missing or blocked | Next action |\n"
            "|---|---|---|---|---|---|---|\n"
            "| Project request | Foundation | Complete | Request Clarification | request approved | None | Run b-form-project-context |\n"
            "| Project context | Foundation | Complete | Project Context Formation | CR-0001 context approved | None | Run c-manage-product-requirements |\n"
            "| Initial requirements | Initial Release | Complete | Product Requirements Management | approved REQ-0002 / US-0006-US-0017 | None | Run d-design-product-architecture |\n"
            "| Architecture | Initial Release | Complete | Product Architecture Design | approved ARCH-002 for CR-0001 | None | Run e-sync-repository-requirements |\n"
            "| Repository preparation | Initial Release | Complete | Repository Requirements Synchronization | CR-0001/REQ-0002 issues created | None | Run f-establish-technical-foundation |\n"
            "| Technical foundation | Initial Release | Complete | Technical Foundation Establishment | initial-release foundation approved | None | Run g-implement-repository-work |\n"
            "| Implementation | Initial Release | Complete | Repository Work Implementation | issue #1 implemented locally | None | Run i-validate-user-story-completion |\n"
            "| User story validation | Initial Release | Complete | BDD User Story Completion Validation | BDD scenarios mapped for US-0001 through US-0005 | None | Run h-create-implementation-pull-request |\n"
            "| Pull request | Initial Release | Complete | Implementation Pull Request | PR #2 merged | None | Run j-prepare-release-deployment |\n"
            "| Release deployment | Initial Release | Not Started | — | — | Pull request complete | Run j-prepare-release-deployment |\n"
        )

        result = self.validate_text(text)

        self.assertFalse(result["passed"])
        joined_errors = " ".join(result["errors"])
        self.assertIn("Technical foundation: complete evidence covers only historical", joined_errors)
        self.assertIn("Implementation: complete evidence covers only historical", joined_errors)
        self.assertIn("User story validation: complete evidence covers only historical", joined_errors)
        self.assertIn("Pull request: complete evidence covers only historical", joined_errors)

    def test_repaired_active_increment_trace_allowed(self):
        text = (
            "| Item | Type | Status | Current activity | Evidence | Missing or blocked | Next action |\n"
            "|---|---|---|---|---|---|---|\n"
            "| Project request | Foundation | Complete | Request Clarification | request approved | None | Run b-form-project-context |\n"
            "| Project context | Foundation | Complete | Project Context Formation | CR-0001 context approved | None | Run c-manage-product-requirements |\n"
            "| Initial requirements | Initial Release | Complete | Product Requirements Management | approved REQ-0002 / US-0006-US-0017 | None | Run d-design-product-architecture |\n"
            "| Architecture | Initial Release | Complete | Product Architecture Design | approved ARCH-002 for CR-0001 | None | Run e-sync-repository-requirements |\n"
            "| Repository preparation | Initial Release | Complete | Repository Requirements Synchronization | CR-0001/REQ-0002 issues created | None | Run f-establish-technical-foundation |\n"
            "| Technical foundation | Initial Release | Not Started | Technical Foundation Establishment | Initial-release foundation complete; CR-0001 foundation update not started | CR-0001 foundation update not started | Run f-establish-technical-foundation |\n"
            "| Implementation | Initial Release | Not Started | Repository Work Implementation | Historical issue #1 implemented for REQ-0001; CR-0001 issues are not implemented yet | CR-0001 technical foundation update not complete | Run g-implement-repository-work after technical foundation update |\n"
            "| User story validation | Initial Release | Not Started | BDD User Story Completion Validation | Historical BDD validation exists for US-0001-US-0005; no CR-0001 validation evidence exists yet for US-0006-US-0017 | CR-0001 implementation not complete | Run i-validate-user-story-completion after implementation |\n"
            "| Pull request | Initial Release | Not Started | Implementation Pull Request | Historical PR #2 merged for REQ-0001; no CR-0001 pull request exists yet | CR-0001 user story validation not complete | Run h-create-implementation-pull-request after CR-0001 validation |\n"
            "| Release deployment | Initial Release | Not Started | — | — | CR-0001 pull request not complete | Run j-prepare-release-deployment after CR-0001 pull request |\n"
        )

        result = self.validate_text(text)

        self.assertTrue(result["passed"], result)


if __name__ == "__main__":
    unittest.main()
