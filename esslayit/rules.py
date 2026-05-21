"""Rule-based writing checks for Esslayit."""

from __future__ import annotations

import re
from collections.abc import Iterable

from .models import CheckConfig, Issue

WORD_RE = re.compile(r"\b[\w']+\b")
SENTENCE_RE = re.compile(r"[^.!?]+[.!?]?", re.MULTILINE)
REPEATED_WORD_RE = re.compile(r"\b(?P<word>[A-Za-z]+)\s+(?P=word)\b", re.IGNORECASE)
PASSIVE_HINT_RE = re.compile(
    r"\b(is|are|was|were|be|been|being)\s+([a-z]+ed|known|seen|made|given|taken|shown)\b",
    re.IGNORECASE,
)

FILLER_PHRASES = {
    "basically": "Use a more precise word or remove it.",
    "actually": "Remove it unless it changes the meaning.",
    "really": "Replace it with a specific description.",
    "very": "Replace it with a stronger or more exact word.",
    "in order to": "Use 'to' unless the longer phrase is needed for emphasis.",
    "it is important to note that": "State the point directly.",
    "due to the fact that": "Use 'because'.",
}


def check_text(text: str, config: CheckConfig | None = None) -> list[Issue]:
    """Run all built-in writing checks over text."""

    config = config or CheckConfig()
    issues: list[Issue] = []
    issues.extend(_check_repeated_words(text))
    issues.extend(_check_long_sentences(text, config))
    issues.extend(_check_filler_phrases(text))
    issues.extend(_check_list_heavy_sentences(text, config))
    issues.extend(_check_passive_voice_hints(text))
    return sorted(issues, key=lambda issue: (issue.line, issue.column, issue.rule_id))


def _check_repeated_words(text: str) -> Iterable[Issue]:
    for match in REPEATED_WORD_RE.finditer(text):
        word = match.group("word")
        yield _issue(
            text=text,
            start=match.start(),
            rule_id="REPEATED_WORD",
            message=f"'{word}' appears twice in a row.",
            suggestion=f"Remove one '{word}' unless the repetition is intentional.",
            excerpt=match.group(0),
        )


def _check_long_sentences(text: str, config: CheckConfig) -> Iterable[Issue]:
    for match in SENTENCE_RE.finditer(text):
        sentence = match.group(0).strip()
        if not sentence:
            continue
        words = WORD_RE.findall(sentence)
        if len(words) > config.max_sentence_words:
            yield _issue(
                text=text,
                start=match.start(),
                rule_id="LONG_SENTENCE",
                message=(
                    f"This sentence has {len(words)} words. The current limit is "
                    f"{config.max_sentence_words}."
                ),
                suggestion="Split the sentence or make the cause and effect easier to follow.",
                excerpt=_shorten(sentence),
            )


def _check_filler_phrases(text: str) -> Iterable[Issue]:
    for phrase, suggestion in FILLER_PHRASES.items():
        pattern = re.compile(rf"\b{re.escape(phrase)}\b", re.IGNORECASE)
        for match in pattern.finditer(text):
            yield _issue(
                text=text,
                start=match.start(),
                rule_id="FILLER_PHRASE",
                message=f"'{match.group(0)}' may weaken the sentence.",
                suggestion=suggestion,
                excerpt=match.group(0),
            )


def _check_list_heavy_sentences(text: str, config: CheckConfig) -> Iterable[Issue]:
    for match in SENTENCE_RE.finditer(text):
        sentence = match.group(0).strip()
        if not sentence:
            continue
        comma_count = sentence.count(",")
        if comma_count >= config.max_commas_before_list_warning:
            yield _issue(
                text=text,
                start=match.start(),
                rule_id="LIST_HEAVY_SENTENCE",
                message=f"This sentence has {comma_count} commas.",
                suggestion="Check whether the sentence is listing examples instead of explaining the point.",
                excerpt=_shorten(sentence),
            )


def _check_passive_voice_hints(text: str) -> Iterable[Issue]:
    for match in PASSIVE_HINT_RE.finditer(text):
        yield _issue(
            text=text,
            start=match.start(),
            rule_id="PASSIVE_VOICE_HINT",
            message=f"'{match.group(0)}' may be passive voice.",
            suggestion="Check whether the sentence needs the actor, or keep it if the actor is not relevant.",
            excerpt=match.group(0),
        )


def _issue(
    *,
    text: str,
    start: int,
    rule_id: str,
    message: str,
    suggestion: str,
    excerpt: str,
) -> Issue:
    line, column = _line_column(text, start)
    return Issue(
        rule_id=rule_id,
        message=message,
        suggestion=suggestion,
        line=line,
        column=column,
        excerpt=excerpt,
    )


def _line_column(text: str, start: int) -> tuple[int, int]:
    before = text[:start]
    line = before.count("\n") + 1
    last_newline = before.rfind("\n")
    column = start + 1 if last_newline == -1 else start - last_newline
    return line, column


def _shorten(value: str, limit: int = 120) -> str:
    clean = " ".join(value.split())
    if len(clean) <= limit:
        return clean
    return f"{clean[: limit - 1]}…"
