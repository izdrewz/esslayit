"""Command-line interface for Esslayit."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .models import CheckConfig, Issue
from .rules import check_text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="esslayit",
        description="Check text and Markdown for essay-writing issues.",
    )
    parser.add_argument("paths", nargs="*", help="Text or Markdown files to check.")
    parser.add_argument("--stdin", action="store_true", help="Read text from standard input.")
    parser.add_argument(
        "--max-sentence-words",
        type=int,
        default=CheckConfig.max_sentence_words,
        help="Flag sentences above this word count.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    parser.add_argument(
        "--fail-on-issues",
        action="store_true",
        help="Exit with status 1 when review prompts are found.",
    )

    args = parser.parse_args(argv)
    if not args.stdin and not args.paths:
        parser.error("provide at least one file path or use --stdin")

    config = CheckConfig(max_sentence_words=args.max_sentence_words)
    reports: list[dict[str, object]] = []
    read_errors = 0

    if args.stdin:
        text = sys.stdin.read()
        reports.append(_check_source("<stdin>", text, config))

    for path_value in args.paths:
        path = Path(path_value)
        if path.is_dir():
            print(f"Skipping directory: {path}", file=sys.stderr)
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            read_errors += 1
            print(f"Could not read {path}: {exc}", file=sys.stderr)
            continue
        reports.append(_check_source(str(path), text, config))

    issue_count = sum(len(report["issues"]) for report in reports)
    if args.format == "json":
        print(json.dumps({"issue_count": issue_count, "reports": reports}, indent=2))
    else:
        _print_text_report(reports, issue_count)

    if read_errors:
        return 2
    if args.fail_on_issues and issue_count:
        return 1
    return 0


def _check_source(source: str, text: str, config: CheckConfig) -> dict[str, object]:
    issues = check_text(text, config)
    return {
        "source": source,
        "issues": [_issue_to_dict(issue) for issue in issues],
    }


def _issue_to_dict(issue: Issue) -> dict[str, object]:
    return {
        "rule_id": issue.rule_id,
        "severity": issue.severity,
        "message": issue.message,
        "suggestion": issue.suggestion,
        "line": issue.line,
        "column": issue.column,
        "excerpt": issue.excerpt,
    }


def _print_text_report(reports: list[dict[str, object]], issue_count: int) -> None:
    for report in reports:
        source = report["source"]
        issues = report["issues"]
        if not issues:
            print(f"{source}: no review prompts found")
            continue
        print(f"{source}:")
        for issue in issues:
            print(
                f"  {issue['line']}:{issue['column']} "
                f"{issue['rule_id']} - {issue['message']}"
            )
            print(f"    Suggestion: {issue['suggestion']}")
            print(f"    Text: {issue['excerpt']}")
    print(f"\nReview prompts found: {issue_count}")


if __name__ == "__main__":
    raise SystemExit(main())
