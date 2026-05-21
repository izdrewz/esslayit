# Esslayit

Esslayit is an original essay-focused writing assistant starter project. It checks plain text and Markdown for issues that often make academic writing harder to read, including repeated words, long sentences, filler phrases, and list-heavy phrasing.

It is not a Grammarly clone and does not unlock or copy any proprietary Grammarly Premium features. The aim is to build a legal, open-source writing helper with its own rules, wording, and design.

## What is included

- A Python command-line checker.
- Lightweight writing rules with no paid API required.
- Unit tests using Python's built-in `unittest` module.
- A GitHub Action for running checks on pushes and pull requests.

## Quick start

Clone the repository and run the checker locally:

```bash
git clone https://github.com/izdrewz/esslayit.git
cd esslayit
python -m esslayit README.md
```

Run the tests:

```bash
python -m unittest
```

Check text from standard input:

```bash
echo "This is very very useful." | python -m esslayit --stdin
```

Fail when issues are found, which is useful for CI:

```bash
python -m esslayit README.md --fail-on-issues
```

## Rule types

Esslayit currently includes simple rule-based checks:

| Rule | What it looks for |
| --- | --- |
| `REPEATED_WORD` | The same word repeated next to itself. |
| `LONG_SENTENCE` | Sentences over a configurable word limit. |
| `FILLER_PHRASE` | Phrases that often weaken direct explanation. |
| `LIST_HEAVY_SENTENCE` | Sentences with several comma-separated examples. |
| `PASSIVE_VOICE_HINT` | Possible passive constructions that may need checking. |

These rules are deliberately cautious. A suggestion is not automatically a mistake; it is a prompt to review the sentence.

## Project direction

Useful next steps would be:

- Add a web interface for pasting essay paragraphs.
- Add a VS Code extension.
- Add optional LanguageTool support.
- Add modes for academic, personal statement, and everyday writing.
- Add clearer explanations for why each suggestion appears.

## License

This project is released under the MIT License.
