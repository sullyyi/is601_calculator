# calculator/repl.py

# Enables forward-compatible type hints (Python < 3.11 safety)
from __future__ import annotations

# Callable allows us to inject input() during tests
# TextIO allows us to inject an output stream (StringIO) during tests
from typing import Callable, TextIO

# Import arithmetic operations (business logic stays separate)
from calculator.operations import add, subtract, multiply, divide


def normalize_operation(raw: str) -> str:
    # Converts user input into a single canonical operation symbol
    # This allows flexible user input without duplicating logic later

    text = raw.strip().lower()

    # Maps all accepted aliases to a single operator
    mapping = {
        "+": "+",
        "add": "+",
        "plus": "+",
        "-": "-",
        "sub": "-",
        "subtract": "-",
        "minus": "-",
        "*": "*",
        "mul": "*",
        "multiply": "*",
        "times": "*",
        "/": "/",
        "div": "/",
        "divide": "/",
    }

    # If the input matches a known operation, return it
    if text in mapping:
        return mapping[text]

    # Any unsupported operation raises a ValueError
    raise ValueError("Invalid operation, try +, -, *, / or their aliases.")


def parse_number(raw: str) -> float:
    # Converts user input into a float
    # Raises ValueError if the input is empty or non-numeric

    text = raw.strip()

    if text == "":
        raise ValueError("Empty input")

    return float(text)


def calculate(op: str, a: float, b: float) -> float:
    # Routes the calculation to the correct arithmetic function
    # Keeps REPL logic clean and testable

    if op == "+":
        return add(a, b)

    if op == "-":
        return subtract(a, b)

    if op == "*":
        return multiply(a, b)

    if op == "/":
        return divide(a, b)

    # Defensive programming: should never occur if normalize_operation works
    raise ValueError("Invalid operation")


def run_repl(
    input_fn: Callable[[str], str] = input,
    output: TextIO | None = None,
) -> None:
    # Main REPL loop
    # input_fn and output are injectable to allow deterministic testing

    import sys

    # Default output is stdout unless overridden in tests
    out = output if output is not None else sys.stdout

    print("Calculator REPL. Type 'q' to quit.", file=out)
    print("Operations: +, -, *, / (or add/sub/mul/div)", file=out)

    while True:
        raw_op = input_fn("Operation: ")

        # Handle exit commands
        if raw_op.strip().lower() in {"q", "quit", "exit"}:
            print("Goodbye.", file=out)
            return

        # Normalize and validate operation input
        try:
            op = normalize_operation(raw_op)
        except ValueError:
            print("Invalid operation. Try +, -, *, /.", file=out)
            continue

        # Parse numeric inputs
        try:
            a = parse_number(input_fn("First number: "))
            b = parse_number(input_fn("Second number: "))
        except ValueError:
            print("Invalid number input. Please enter a valid numeric value.", file=out)
            continue

        # Perform calculation
        try:
            result = calculate(op, a, b)
        except ZeroDivisionError:
            print("Error: division by zero.", file=out)
            continue

        print(f"Result: {result}", file=out)
