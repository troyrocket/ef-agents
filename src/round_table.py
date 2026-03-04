"""100-round Round Table debate between Alisa and Bob."""

import re
import anthropic
from rich.console import Console
from rich.rule import Rule

from .config import (
    MODEL, ALISA_SYSTEM, BOB_SYSTEM, ROUND_TABLE_AGENT_PROMPT,
    TOTAL_ROUNDS, EF_PURPLE, EF_ORANGE, get_phase
)

client = anthropic.Anthropic()
console = Console()


def parse_conviction(text: str) -> tuple[int, str]:
    """Extract conviction level and verdict from agent response."""
    conviction = 5
    verdict = "Maybe"

    match = re.search(r'CONVICTION:\s*(\d+)', text)
    if match:
        conviction = min(10, max(1, int(match.group(1))))

    match = re.search(r'VERDICT:\s*(Strong Yes|Yes|Lean Yes|Maybe|Lean No|No)', text)
    if match:
        verdict = match.group(1)

    return conviction, verdict


def conviction_to_bar(conviction: int) -> str:
    """Convert conviction level to a visual bar."""
    filled = "█" * conviction
    empty = "░" * (10 - conviction)
    return f"{filled}{empty}"


def run_round_table(
    alisa_eval: str,
    bob_eval: str,
    candidate_data: str,
    total_rounds: int = TOTAL_ROUNDS,
) -> dict:
    """Run the full round table debate. Streams output to CLI in real-time."""

    transcript_lines = []
    rounds_data = []
    alisa_conviction = 5
    bob_conviction = 5
    alisa_verdict = "Maybe"
    bob_verdict = "Maybe"

    _, alisa_verdict = parse_conviction(alisa_eval)
    _, bob_verdict = parse_conviction(bob_eval)

    console.print()
    console.print(Rule(f"[bold {EF_ORANGE}]ROUND TABLE — {total_rounds}-ROUND DEBATE[/]", style=EF_ORANGE))
    console.print()

    for round_num in range(1, total_rounds + 1):
        phase_name, phase_desc = get_phase(round_num)

        is_alisa = (round_num % 2 == 1)
        agent_name = "Alisa" if is_alisa else "Bob"
        agent_system = ALISA_SYSTEM if is_alisa else BOB_SYSTEM
        own_eval = alisa_eval if is_alisa else bob_eval
        other_eval = bob_eval if is_alisa else alisa_eval
        prev_conviction = alisa_conviction if is_alisa else bob_conviction

        transcript_str = "\n".join(transcript_lines[-30:]) if transcript_lines else "(No prior discussion)"

        prompt = ROUND_TABLE_AGENT_PROMPT.format(
            agent_name=agent_name,
            agent_system=agent_system,
            round_num=round_num,
            total_rounds=total_rounds,
            phase_name=phase_name,
            phase_desc=phase_desc,
            own_eval=own_eval,
            other_eval=other_eval,
            candidate_data=candidate_data[:3000],
            transcript=transcript_str,
        )

        # Phase header on transitions
        if round_num == 1 or get_phase(round_num)[0] != get_phase(round_num - 1)[0]:
            console.print()
            console.print(Rule(f"[bold {EF_ORANGE}]{phase_name}[/]", style=EF_ORANGE))
            console.print()

        # Agent color: Alisa=purple, Bob=orange
        ac = EF_PURPLE if is_alisa else EF_ORANGE

        # Round label
        console.print(f"  [bold {ac}][{agent_name}][/] [dim]Round {round_num}/{total_rounds}[/]")

        # Stream response
        full_response = ""
        with client.messages.stream(
            model=MODEL,
            max_tokens=300,
            system=f"You are {agent_name} in a debate. Be concise: 2-4 sentences max, then CONVICTION and VERDICT.",
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            console.print(f"  [dim]\"[/]", end="")
            for text in stream.text_stream:
                full_response += text
                if "CONVICTION:" not in full_response:
                    console.print(text, end="", highlight=False)

        conviction, verdict = parse_conviction(full_response)
        display_text = re.sub(r'\n*CONVICTION:.*$', '', full_response, flags=re.DOTALL).strip()

        # Conviction shift
        shifted = conviction != prev_conviction
        shift_indicator = ""
        if shifted:
            direction = "↑" if conviction > prev_conviction else "↓"
            shift_indicator = f" [bold {ac}]⚡ {prev_conviction}→{conviction}{direction}[/]"

        console.print(f"\"")
        bar = conviction_to_bar(conviction)
        console.print(
            f"  [dim]conviction:[/] [{ac}]{bar}[/] "
            f"[bold {ac}]{conviction}/10[/] → [bold]{verdict}[/]{shift_indicator}"
        )
        console.print()

        if is_alisa:
            alisa_conviction = conviction
            alisa_verdict = verdict
        else:
            bob_conviction = conviction
            bob_verdict = verdict

        transcript_lines.append(f"[Round {round_num}] {agent_name}: {display_text}")
        rounds_data.append({
            "round": round_num,
            "agent": agent_name,
            "phase": phase_name,
            "text": display_text,
            "conviction": conviction,
            "verdict": verdict,
            "shifted": shifted,
        })

    # Final summary
    console.print()
    console.print(Rule(f"[bold {EF_ORANGE}]DEBATE CONCLUDED[/]", style=EF_ORANGE))
    console.print(f"  [bold {EF_PURPLE}]Alisa[/] final: {alisa_conviction}/10 → {alisa_verdict}")
    console.print(f"  [bold {EF_ORANGE}]Bob[/]   final: {bob_conviction}/10 → {bob_verdict}")

    verdicts_match = alisa_verdict == bob_verdict
    if verdicts_match:
        console.print(f"\n  [bold {EF_ORANGE}]✓ Consensus: {alisa_verdict}[/]")
    else:
        console.print(f"\n  [bold {EF_ORANGE}]⚠ Split decision — flagged for human review[/]")
    console.print()

    return {
        "rounds": rounds_data,
        "transcript": transcript_lines,
        "alisa_final_conviction": alisa_conviction,
        "alisa_final_verdict": alisa_verdict,
        "bob_final_conviction": bob_conviction,
        "bob_final_verdict": bob_verdict,
        "consensus": verdicts_match,
        "final_verdict": alisa_verdict if verdicts_match else f"{alisa_verdict} / {bob_verdict} (split)",
    }
