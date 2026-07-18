from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pyswip import Prolog


# Locate files relative to the Week 5 project folder.
ROOT_DIR = Path(__file__).resolve().parents[1]
KB_PATH = ROOT_DIR / "implementation" / "knowledge_base.pl"
TEST_CASES_PATH = ROOT_DIR / "implementation" / "test_cases.json"
RESULTS_PATH = ROOT_DIR / "results" / "test_results.md"


def load_test_cases() -> list[dict[str, str]]:
    """Load natural-language questions and their symbolic Prolog queries."""
    if not TEST_CASES_PATH.exists():
        raise FileNotFoundError(f"Test-case file not found: {TEST_CASES_PATH}")

    with TEST_CASES_PATH.open("r", encoding="utf-8") as file:
        test_cases = json.load(file)

    if not isinstance(test_cases, list):
        raise ValueError("test_cases.json must contain a JSON list.")

    return test_cases


def simplify_solutions(
    solutions: list[dict[str, Any]],
) -> list[dict[str, str]]:
    """Convert PySwip values into readable strings."""
    return [
        {variable: str(value) for variable, value in solution.items()}
        for solution in solutions
    ]


def execute_query(
    prolog: Prolog,
    query: str,
) -> tuple[str, list[dict[str, str]], str]:
    """
    Run a Prolog query.

    Returns:
        actual_result: true, false, or error
        solutions: any variable bindings returned by Prolog
        feedback: error feedback from the symbolic solver
    """
    try:
        raw_solutions = list(prolog.query(query))
        solutions = simplify_solutions(raw_solutions)

        if raw_solutions:
            return "true", solutions, ""

        return "false", [], ""

    except Exception as error:
        feedback = f"{type(error).__name__}: {error}"
        return "error", [], feedback


def escape_markdown(value: str) -> str:
    """Prevent text from breaking the Markdown results table."""
    return value.replace("|", "\\|").replace("\n", " ")


def save_results(results: list[dict[str, Any]]) -> None:
    """Save a reproducible Markdown report of all tests."""
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    passed = sum(result["status"] == "PASS" for result in results)
    total = len(results)

    lines = [
        "# Logic-LM-Style Pipeline Test Results",
        "",
        "## Pipeline",
        "",
        "```text",
        "Natural-language question",
        "        ↓",
        "Symbolic Prolog query",
        "        ↓",
        "SWI-Prolog reasoning engine",
        "        ↓",
        "True, false/not derivable, or solver error",
        "```",
        "",
        f"**Tests passed:** {passed}/{total}",
        "",
        "| ID | Category | Natural-language question | Prolog query | Expected | Actual | Status |",
        "|---|---|---|---|---|---|---|",
    ]

    for result in results:
        lines.append(
            "| {id} | {category} | {question} | `{query}` | "
            "{expected} | {actual} | {status} |".format(
                id=escape_markdown(result["id"]),
                category=escape_markdown(result["category"]),
                question=escape_markdown(result["natural_language"]),
                query=escape_markdown(result["prolog_query"]),
                expected=result["expected"],
                actual=result["actual"],
                status=result["status"],
            )
        )

    lines.extend(
        [
            "",
            "## Solver Feedback and Returned Solutions",
            "",
        ]
    )

    for result in results:
        lines.append(f"### {result['id']}: {result['category']}")
        lines.append("")
        lines.append(f"- **Question:** {result['natural_language']}")
        lines.append(f"- **Symbolic query:** `{result['prolog_query']}`")
        lines.append(f"- **Result:** {result['actual']}")
        lines.append(f"- **Status:** {result['status']}")

        if result["solutions"]:
            lines.append(
                f"- **Returned solutions:** `{json.dumps(result['solutions'])}`"
            )

        if result["feedback"]:
            lines.append(
                f"- **Solver feedback:** `{escape_markdown(result['feedback'])}`"
            )

        lines.append("")

    lines.extend(
        [
            "## Interpretation Note",
            "",
            "A result of `false` means that Prolog could not derive the query "
            "from the available facts and rules. Under Prolog's closed-world "
            "assumption, an unsupported statement is treated as false or "
            "not derivable. This does not always prove that the statement is "
            "false in the real world.",
            "",
            "The malformed query demonstrates how the symbolic engine can "
            "detect invalid logic and return feedback. In the full Logic-LM "
            "approach, this feedback can be passed back to an LLM so that it "
            "can revise the generated logical program.",
        ]
    )

    RESULTS_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    if not KB_PATH.exists():
        raise FileNotFoundError(
            f"Knowledge base not found: {KB_PATH}\n"
            "Copy your Task 4 aiea_kb.pl file into the implementation folder."
        )

    test_cases = load_test_cases()

    prolog = Prolog()

    # Forward slashes work more reliably when SWI-Prolog receives Windows paths.
    prolog.consult(KB_PATH.as_posix())

    results: list[dict[str, Any]] = []

    print("\nLogic-LM-Style Symbolic Reasoning Tests")
    print("=" * 55)

    for test_case in test_cases:
        actual, solutions, feedback = execute_query(
            prolog,
            test_case["prolog_query"],
        )

        expected = test_case["expected"].lower()
        status = "PASS" if actual == expected else "FAIL"

        result = {
            **test_case,
            "expected": expected,
            "actual": actual,
            "status": status,
            "solutions": solutions,
            "feedback": feedback,
        }
        results.append(result)

        print(
            f"{test_case['id']}: {test_case['category']}\n"
            f"  Natural language: {test_case['natural_language']}\n"
            f"  Prolog query:     {test_case['prolog_query']}\n"
            f"  Expected:         {expected}\n"
            f"  Actual:           {actual}\n"
            f"  Status:           {status}\n"
        )

        if solutions:
            print(f"  Solutions:        {solutions}\n")

        if feedback:
            print(f"  Solver feedback:  {feedback}\n")

    save_results(results)

    passed = sum(result["status"] == "PASS" for result in results)

    print("=" * 55)
    print(f"Completed: {passed}/{len(results)} tests passed.")
    print(f"Results saved to: {RESULTS_PATH}")


if __name__ == "__main__":
    main()