# IS601 Calculator (Assignment 3)

A command-line calculator implemented in Python featuring a REPL (Read–Eval–Print Loop), input validation, error handling, comprehensive unit tests, and CI enforcement of 100% test coverage.

## Features

- REPL interface for continuous user interaction
- Addition, subtraction, multiplication, and division
- Supports operation symbols and aliases:
  - `+` / `add` / `plus`
  - `-` / `sub` / `subtract` / `minus`
  - `*` / `mul` / `multiply` / `times`
  - `/` / `div` / `divide`
- Input validation for operations and numeric values
- Graceful error handling (invalid inputs, division by zero)
- Pytest unit tests + parameterized tests
- GitHub Actions CI runs tests on every push/PR and fails if coverage < 100%

## Project Structure

- `calculator/` - application package
  - `operations.py` - arithmetic functions
  - `repl.py` - REPL implementation and helper functions
  - `__main__.py` - module entrypoint (`python -m calculator`)
- `tests/` - pytest test suite
- `.github/workflows/ci.yml` - CI pipeline (tests + coverage gate)

## Setup

### 1) Create and activate a virtual environment

bash
python3 -m venv .venv
source .venv/bin/activate

### 2) Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

###Run the calculator from the repo root
python -m calculator

Quit the REPL by typing q, quit, or exit, during prompts

### Run tests and coverage
python -m pytest
