import unittest

from esslayit import CheckConfig, check_text


class RuleTests(unittest.TestCase):
    def test_repeated_word_is_flagged(self):
        issues = check_text("This is very very clear.")
        self.assertTrue(any(issue.rule_id == "REPEATED_WORD" for issue in issues))

    def test_filler_phrase_is_flagged(self):
        issues = check_text("It is important to note that this sentence is indirect.")
        self.assertTrue(any(issue.rule_id == "FILLER_PHRASE" for issue in issues))

    def test_long_sentence_respects_config(self):
        issues = check_text(
            "One two three four five six.",
            CheckConfig(max_sentence_words=5),
        )
        self.assertTrue(any(issue.rule_id == "LONG_SENTENCE" for issue in issues))

    def test_line_and_column_are_reported(self):
        issues = check_text("First line.\nThis is really clear.")
        filler_issue = next(issue for issue in issues if issue.rule_id == "FILLER_PHRASE")
        self.assertEqual(filler_issue.line, 2)
        self.assertEqual(filler_issue.column, 9)

    def test_clear_text_has_no_issues(self):
        issues = check_text("The argument links the evidence to the claim.")
        self.assertEqual(issues, [])


if __name__ == "__main__":
    unittest.main()
