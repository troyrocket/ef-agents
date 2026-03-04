"""Alisa & Bob evaluation agents using Claude API."""

import anthropic
from .config import MODEL, ALISA_SYSTEM, BOB_SYSTEM, ALISA_EVAL_PROMPT, BOB_EVAL_PROMPT


client = anthropic.Anthropic()


def run_alisa_evaluation(candidate_data: str) -> str:
    """Run Alisa's Founder Edge evaluation. Returns raw evaluation text."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=ALISA_SYSTEM,
        messages=[{
            "role": "user",
            "content": ALISA_EVAL_PROMPT.format(candidate_data=candidate_data)
        }]
    )
    return response.content[0].text


def run_bob_evaluation(candidate_data: str) -> str:
    """Run Bob's Taste & Network evaluation. Returns raw evaluation text."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=BOB_SYSTEM,
        messages=[{
            "role": "user",
            "content": BOB_EVAL_PROMPT.format(candidate_data=candidate_data)
        }]
    )
    return response.content[0].text


def parse_scores(eval_text: str) -> dict:
    """Parse score lines from evaluation text into a dict."""
    scores = {}
    for line in eval_text.strip().split("\n"):
        if "_SCORE:" in line:
            parts = line.split(":", 1)
            key = parts[0].strip()
            try:
                scores[key] = float(parts[1].strip())
            except (ValueError, IndexError):
                pass
        elif line.startswith("OVERALL_SCORE:"):
            try:
                scores["OVERALL_SCORE"] = float(line.split(":", 1)[1].strip())
            except (ValueError, IndexError):
                pass
        elif line.startswith("INITIAL_VERDICT:"):
            scores["INITIAL_VERDICT"] = line.split(":", 1)[1].strip()
        elif line.startswith("EDGE_TYPE:"):
            scores["EDGE_TYPE"] = line.split(":", 1)[1].strip()
        elif line.startswith("SUMMARY:"):
            scores["SUMMARY"] = line.split(":", 1)[1].strip()
    return scores
