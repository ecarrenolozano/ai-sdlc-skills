"""
Regression test for <issue or confirmed defect>.

Defect:
    <Describe the reproduced defect.>

Protected behavior:
    <Describe the expected behavior after correction.>
"""

# Standard library imports

# Third-party imports
import pytest

# Local application imports


pytestmark = [
    pytest.mark.regression,
    pytest.mark.unit,  # Replace with integration when appropriate.
]


def test_confirmed_defect_does_not_recur() -> None:
    """Reproduce the defect before the fix and protect the correction."""
    raise NotImplementedError
