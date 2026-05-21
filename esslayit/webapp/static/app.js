const input = document.querySelector("#writing-input");
const maxSentenceWords = document.querySelector("#max-sentence-words");
const checkButton = document.querySelector("#check-button");
const clearButton = document.querySelector("#clear-button");
const summary = document.querySelector("#summary");
const issues = document.querySelector("#issues");

checkButton.addEventListener("click", async () => {
  const text = input.value.trim();

  if (!text) {
    summary.textContent = "Paste some text first.";
    issues.innerHTML = "";
    input.focus();
    return;
  }

  setLoading(true);

  try {
    const response = await fetch("/api/check", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text,
        max_sentence_words: Number(maxSentenceWords.value),
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "The checker could not run.");
    }

    renderResults(data);
  } catch (error) {
    summary.textContent = error.message;
    issues.innerHTML = "";
  } finally {
    setLoading(false);
  }
});

clearButton.addEventListener("click", () => {
  input.value = "";
  summary.textContent = "No text checked yet.";
  issues.innerHTML = "";
  input.focus();
});

function setLoading(isLoading) {
  checkButton.disabled = isLoading;
  checkButton.textContent = isLoading ? "Checking..." : "Check text";
}

function renderResults(data) {
  const count = data.issue_count || 0;

  if (count === 0) {
    summary.textContent = "No review prompts found.";
    issues.innerHTML = "";
    return;
  }

  summary.textContent = `${count} review prompt${count === 1 ? "" : "s"} found.`;
  issues.innerHTML = "";

  data.issues.forEach((issue) => {
    const card = document.createElement("article");
    card.className = "issue-card";

    const meta = document.createElement("div");
    meta.className = "issue-meta";
    meta.textContent = `${issue.rule_id} at line ${issue.line}, column ${issue.column}`;

    const message = document.createElement("p");
    message.textContent = issue.message;

    const suggestion = document.createElement("p");
    suggestion.textContent = `Suggestion: ${issue.suggestion}`;

    const excerpt = document.createElement("p");
    excerpt.className = "excerpt";
    excerpt.textContent = issue.excerpt;

    card.append(meta, message, suggestion, excerpt);
    issues.appendChild(card);
  });
}
