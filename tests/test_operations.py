#pytest is the testing framework we are using
import pytest

#Importing the arithmetic functions we want to test
from calculator.operations import add, subtract, multiply, divide


# Parametrized test allows us to test multiple input/output
# combinations using a single test function.

@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 5),          # basic positive numbers
        (-2, 3, 1),         # negative + positive
        (0, 0, 0),          # zero case
        (1.5, 2.5, 4.0),    # floating point values
    ],
)
def test_add(a, b, expected):
    # NOTE: Assert that add() returns the expected result
    assert add(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (5, 3, 2),          # positive subtraction
        (3, 5, -2),         # result negative
        (0, 7, -7),         # zero minus positive
        (2.5, 0.5, 2.0),    # floating point subtraction
    ],
)
def test_subtract(a, b, expected):
    # NOTE: Testing subtraction logic
    assert subtract(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 6),          # positive multiplication
        (-2, 3, -6),        # negative * positive
        (0, 99, 0),         # zero multiplication
        (1.5, 2, 3.0),      # floating point multiplication
    ],
)
def test_multiply(a, b, expected):
    # NOTE: Testing multiplication logic
    assert multiply(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10, 2, 5.0),       # standard division
        (9, 3, 3.0),        # divisible numbers
        (-8, 2, -4.0),      # negative division
        (5, 2, 2.5),        # non-integer result
    ],
)
def test_divide(a, b, expected):
    # NOTE: Testing division logic for valid denominators
    assert divide(a, b) == expected


def test_divide_by_zero_raises():
    # NOTE:
    # Division by zero is an expected error case.
    # We verify that the function raises ZeroDivisionError
    # instead of crashing the program silently.
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
