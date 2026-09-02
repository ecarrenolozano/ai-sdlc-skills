---
name: 'Python Best Practices'
description: 'Python coding conventions and guidelines'
applyTo: '**/*.py'
---



# Python Best Practices and Coding Standards

Version: 1.0.0
Last Updated: 2026-02-10


## Python Instructions

- Write clear and concise comments for each function.
- Ensure functions have descriptive names and include type hints.
- Provide docstrings following PEP 257 conventions.
- Use the `typing` module for type annotations (e.g., `List[str]`, `Dict[str, int]`).
- Break down complex functions into smaller, more manageable functions.

## General Instructions

- Always prioritize readability and clarity.
- For algorithm-related code, include explanations of the approach used, diagrams in mermaid and pseudocode.
- Write code with good maintainability practices, including comments on why certain design decisions were made.
- Handle edge cases and write clear exception handling.
- For libraries or external dependencies, mention their usage and purpose in comments.
- Use consistent naming conventions and follow language-specific best practices.
- Write concise, efficient, and idiomatic code that is also easily understandable.

## Exception handling
- Use specific exception types rather than catching all exceptions with a generic `except` statement.
- Provide informative error messages when raising exceptions.
- Avoid using exceptions for control flow; instead, use them for handling unexpected situations.
- Favor the use of logger.exception() for logging exceptions, as it provides a stack trace along with the error message.
- Example:
```python
import logging

def divide(a: float, b: float) -> float:
    """Divide two numbers and handle potential exceptions.
    
    Parameters:
    a (float): The numerator.
    b (float): The denominator.
    
    Returns:
    float: The result of the division.
    
    Raises:
    ValueError: If the denominator is zero.
    """
    if b == 0:
        logging.exception("Attempted to divide by zero.")
        raise ValueError("Denominator cannot be zero.")
    return a / b
```

## Code Style and Formatting

- Follow the **PEP 8** style guide for Python.
- Maintain proper indentation (use 4 spaces for each level of indentation).
- Ensure lines do not exceed 79 characters.
- Place function and class docstrings immediately after the `def` or `class` keyword in Google Style.
- Use blank lines to separate functions, classes, and code blocks where appropriate.

## Edge Cases and Testing

- Before writing any test, create a test plan that outlines the scenarios to be tested, including edge cases.
- Always include test cases for critical paths of the application.
- Account for common edge cases like empty inputs, invalid data types, and large datasets.
- Include comments for edge cases and the expected behavior in those cases.
- Write unit tests for functions and document them with docstrings explaining the test cases.
- Use only `pytest` for testing and ensure that tests are organized in a separate directory (e.g., `tests/`).
- Use a template for test cases that includes a description of the test, the input data, the expected output, and any relevant edge cases.


### Considerations for testing
- Never use direct equality (==) or inequality (!=) comparisons with floating point numbers.
- Use math.isclose() or pytest.approx() for comparing floating point values, specifying a relative or absolute tolerance as appropriate.
- Example:
    - Instead of: `assert result == 0.1`
    - Use: `assert math.isclose(result, 0.1, rel_tol=1e-9)`
    - Or in pytest: `assert result == pytest.approx(0.1)`

## Example of Proper Documentation

```python
def calculate_area(radius: float) -> float:
    """
    Calculate the area of a circle given the radius.
    
    Parameters:
    radius (float): The radius of the circle.
    
    Returns:
    float: The area of the circle, calculated as π * radius^2.
    """
    import math
    return math.pi * radius ** 2
```

## Template for unit tests

This is a template for unit tests that includes a description of the test, the input data, the expected output, and any relevant edge cases. The tests are organized into:

- nominal case tests
- negative case tests
- edge case tests
- regression unit tests.

```python
"""
Unit test organization:
    - Nominal Case Tests: Test the nominal case where the function is expected to work correctly with typical input values.

    - Negative Case Tests: Test cases that involve invalid input values or scenarios where the function should handle errors gracefully.
    
    - Edge Case Tests: Test cases that involve boundary conditions or unusual input values that may not be common but should still be handled correctly by the function.
    
    - Regression Unit Tests: Test cases that ensure that previously fixed bugs do not reoccur and that existing functionality remains intact after changes to the codebase.

"""
# Standard imports
import math

# Third-party imports
import pytest

# Local imports
from my_module import calculate_area

# =============================================================================
# ==== Fixtures and Setup
# =============================================================================
@pytest.fixture
def setup_data():
    """Fixture to set up any necessary data for the tests.
    """
    # Set up data here
    return data 

# =============================================================================
# ==== Class Test Cases
# =============================================================================
class TestCalculateArea:
    """
    Test cases for the calculate_area function.
    """

    # ---- Nominal Case Tests
    def test_nominal_case(self):
        """
        Test the nominal case where radius is a positive number.
        The function should return the correct area of the circle.
        """
        from math import pi
        assert calculate_area(5) == pytest.approx(pi * 25)

    # ---- Negative Case Tests
    def test_negative_radius(self):
        """
        Test the case where radius is a negative number.
        The function should return 0, as negative radius is not valid.
        """
        assert calculate_area(-1) == 0
    
    #---- Edge Case Tests
    def test_zero_radius(self):
        """
        Test the case where radius is zero.
        The function should return 0, as the area of a circle with zero radius is zero.
        """
        assert calculate_area(0) == 0

    # ---- Regression Unit Tests
    def test_regression_case(self):
        """
        Test a regression case to ensure that previous functionality is not broken.
        For example, if there was a bug related to large radius values, we can test that here.
        """
        from math import pi
        assert calculate_area(1e6) == pytest.approx(pi * (1e6 ** 2))


# =============================================================================
# ==== Function Test Cases
# =============================================================================

# Function name: calculate_area
# ---- Nominal Case Tests
def test_calculate_area_nominal():
    """Test the nominal case where radius is a positive number.
The function should return the correct area of the circle.
    """
    from math import pi
    assert calculate_area(5) == pytest.approx(pi * 25)

# ---- Negative Case Tests
def test_calculate_area_negative_radius():
    """Test the case where radius is a negative number.
The function should return 0, as negative radius is not valid.
    """
    assert calculate_area(-1) == 0

# ---- Edge Case Tests
def test_calculate_area_zero_radius():
    """Test the case where radius is zero.
The function should return 0, as the area of a circle with zero radius is zero.
    """
    assert calculate_area(0) == 0

# ---- Regression Unit Tests
def test_calculate_area_regression():
    """Test a regression case to ensure that previous functionality is not broken.
For example, if there was a bug related to large radius values, we can test that here.
    """
    from math import pi
    assert calculate_area(1e6) == pytest.approx(pi * (1e6 ** 2))



```



