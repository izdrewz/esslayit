import unittest

from esslayit.server import make_check_response


class ServerResponseTests(unittest.TestCase):
    def test_check_response_contains_issues(self):
        response = make_check_response("This is very very useful.")
        self.assertGreaterEqual(response["issue_count"], 1)
        self.assertTrue(any(issue["rule_id"] == "REPEATED_WORD" for issue in response["issues"]))

    def test_check_response_respects_sentence_limit(self):
        response = make_check_response("One two three four five six.", max_sentence_words=5)
        self.assertTrue(any(issue["rule_id"] == "LONG_SENTENCE" for issue in response["issues"]))


if __name__ == "__main__":
    unittest.main()
