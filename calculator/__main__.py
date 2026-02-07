# calculator/__main__.py

# Entry point for running the calculator as a module
from calculator.repl import run_repl


def main() -> None:
    # Delegates execution to the REPL
    run_repl()


# Allows direct execution if needed
if __name__ == "__main__":
    main()
