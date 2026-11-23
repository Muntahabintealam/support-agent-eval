"""Run every test case through the agent and report a pass rate.

Usage: python run_evals.py --label baseline
Results are saved to evals/results/<label>.json so you can compare versions.
"""
import argparse
import json
import pathlib

from agent import answer


def check(case: dict, out: dict) -> list:
    failures = []
    called = set(out["tools_called"])
    for tool in case["expect_tools"]:
        if tool not in called:
            failures.append(f"expected tool {tool}, got {sorted(called)}")
    if not case["expect_tools"] and called - {"search_help_center"}:
        failures.append(f"unexpected tool use: {sorted(called)}")
    text = out["text"].lower()
    for s in case["must_include"]:
        if s.lower() not in text:
            failures.append(f"missing text: {s!r}")
    for s in case["must_not_include"]:
        if s.lower() in text:
            failures.append(f"forbidden text: {s!r}")
    return failures


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="run")
    args = parser.parse_args()

    cases = [json.loads(l) for l in pathlib.Path("evals/cases.jsonl").read_text().splitlines() if l.strip()]
    results, passed = [], 0
    for case in cases:
        out = answer(case["question"])
        failures = check(case, out)
        passed += not failures
        results.append({"id": case["id"], "passed": not failures, "failures": failures, "reply": out["text"], "tools": out["tools_called"]})
        print(("PASS " if not failures else "FAIL ") + case["id"], failures if failures else "")

    rate = passed / len(cases)
    print(f"\n{passed}/{len(cases)} passed ({rate:.0%})")
    pathlib.Path("evals/results").mkdir(exist_ok=True)
    pathlib.Path(f"evals/results/{args.label}.json").write_text(json.dumps({"pass_rate": rate, "results": results}, indent=2))


if __name__ == "__main__":
    main()
