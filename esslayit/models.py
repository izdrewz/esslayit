"""Shared data models for Esslayit."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CheckConfig:
    """Configuration for writing checks."""

    max_sentence_words: int = 32
    max_commas_before_list_warning: int = 3


@dataclass(frozen=True)
class Issue:
    """A writing issue found by a rule."""

    rule_id: str
    message: str
    suggestion: str
    line: int
    column: int
    excerpt: str
    severity: str = "review"

    def format(self) -> str:
        location = f"line {self.line}, column {self.column}"
        return (
            f"[{self.severity}] {self.rule_id} at {location}\n"
            f"  {self.message}\n"
            f"  Suggestion: {self.suggestion}\n"
            f"  Text: {self.excerpt}"
        )
