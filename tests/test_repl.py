# tests/test_repl.py

# io.StringIO is used to capture printed output
import io

# pytest is the testing framework
import pytest

# Import functions under test
from calculator.repl import normalize_operation, parse_number, calculate, run_repl


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("+", "+"),
        (" add ", "+"),
        ("PLUS", "+"),
        ("-", "-"),
        ("subtract", "-"),
        ("mul", "*"),
        ("times", "*"),
        ("DIVIDE", "/"),
        ("/", "/"),
    ],
)
def test_normalize_operation_valid(raw, expected):
    # Ensures valid aliases normalize correctly
    assert normalize_operation(raw) == expected


def test_normalize_operation_invalid():
    # Invalid operations must raise ValueError
    with pytest.raises(ValueError):
        normalize_operation("power")


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("3", 3.0),
        ("  3.5 ", 3.5),
        ("-2", -2.0),
    ],
)
def test_parse_number_valid(raw, expected):
    # Valid numeric strings convert to float
    assert parse_number(raw) == expected


@pytest.mark.parametrize("raw", ["", "   ", "abc"])
def test_parse_number_invalid(raw):
    # Invalid numeric input raises ValueError
    with pytest.raises(ValueError):
        parse_number(raw)


def test_calculate_invalid_operation():
    # Defensive branch coverage
    with pytest.raises(ValueError):
        calculate("%", 1.0, 2.0)


def test_run_repl_quit_immediately():
    # REPL should exit cleanly on first input
    inputs = iter(["q"])
    out = io.StringIO()

    run_repl(input_fn=lambda _: next(inputs), output=out)

    text = out.getvalue()
    assert "Calculator REPL" in text
    assert "Goodbye." in text


def test_run_repl_invalid_operation_then_quit():
    # Invalid operation should print error and continue
    inputs = iter(["nope", "q"])
    out = io.StringIO()

    run_repl(input_fn=lambda _: next(inputs), output=out)

    text = out.getvalue()
    assert "Invalid operation" in text
    assert "Goodbye." in text


def test_run_repl_invalid_number_then_quit():
    # Non-numeric input should be handled gracefully
    inputs = iter(["+", "abc", "2", "q"])
    out = io.StringIO()

    run_repl(input_fn=lambda _: next(inputs), output=out)

    text = out.getvalue()
    assert "Invalid number input" in text
    assert "Goodbye." in text


def test_run_repl_divide_by_zero_then_quit():
    # Division by zero must not crash the REPL
    inputs = iter(["/", "10", "0", "q"])
    out = io.StringIO()

    run_repl(input_fn=lambda _: next(inputs), output=out)

    text = out.getvalue()
    assert "division by zero" in text
    assert "Goodbye." in text

# runpy allows executing a module as if it were run with: python -m module
import runpy

# Import the module so we can monkeypatch calculator.repl.run_repl safely
import calculator.repl


@pytest.mark.parametrize(
    "op,a,b,expected",
    [
        ("+", 2.0, 3.0, 5.0),    # covers add branch in calculate()
        ("-", 5.0, 3.0, 2.0),    # covers subtract branch in calculate()
        ("*", 2.0, 4.0, 8.0),    # covers multiply branch in calculate()
        ("/", 9.0, 3.0, 3.0),    # covers divide branch in calculate() in a normal case too
    ],
)
def test_calculate_all_operations(op, a, b, expected):
    # Covers all calculate() branches, not just error paths
    assert calculate(op, a, b) == expected


def test_run_repl_with_default_stdout_output(capsys):
    # Covers the branch where output is None and run_repl defaults to sys.stdout
    inputs = iter(["q"])

    run_repl(input_fn=lambda _: next(inputs), output=None)

    captured = capsys.readouterr()
    assert "Calculator REPL" in captured.out
    assert "Goodbye." in captured.out


def test___main___executes_main(monkeypatch):
    # Covers calculator/__main__.py by executing it as __main__ (no real REPL interaction)
    calls = {"count": 0}

    def fake_run_repl(*args, **kwargs):
        # Proves that main() called run_repl(), without starting interactive prompts
        calls["count"] += 1

    # Patch calculator.repl.run_repl BEFORE running calculator.__main__
    monkeypatch.setattr(calculator.repl, "run_repl", fake_run_repl)

    # Execute module like: python -m calculator
    runpy.run_module("calculator.__main__", run_name="__main__")

    assert calls["count"] == 1
    
def test_run_repl_success_path_prints_result(capsys):
    # Uses a prompt-aware input function so each prompt gets the correct response.
    # This guarantees the REPL reaches the "Result: ..." print line.

    responses = {
        "Operation: ": "+",
        "First number: ": "2",
        "Second number: ": "3",
    }

    calls = {"op_count": 0}

    def fake_input(prompt: str) -> str:
        # After one successful operation, quit on the next Operation prompt
        if prompt == "Operation: ":
            if calls["op_count"] == 0:
                calls["op_count"] += 1
                return responses[prompt]
            return "q"
        return responses[prompt]

    run_repl(input_fn=fake_input, output=None)

    captured = capsys.readouterr()
    assert "Result: 5.0" in captured.out
    assert "Goodbye." in captured.out
