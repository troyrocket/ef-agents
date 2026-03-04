```
███████╗███████╗     █████╗  ██████╗ ███████╗███╗   ██╗████████╗███████╗
██╔════╝██╔════╝    ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝██╔════╝
█████╗  █████╗      ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   ███████╗
██╔══╝  ██╔══╝      ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   ╚════██║
███████╗██║         ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   ███████║
╚══════╝╚═╝         ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝
```

**Three AI minds. One decision. Zero bias.**

A Multi-Agent system that evaluates startup founder candidates for [Entrepreneurs First (EF)](https://www.joinef.com/). Two AI agents independently assess a candidate, then engage in a 100-round structured debate to reach a final verdict — all streamed live in your terminal.

## How It Works

```
LinkedIn / Twitter / GitHub URLs
         ↓
   ┌─────────────┐    ┌─────────────┐
   │    Alisa     │    │     Bob     │
   │ Founder Edge │    │Taste & Net  │
   └──────┬──────┘    └──────┬──────┘
          └───────┬──────────┘
                  ↓
         ┌──────────────┐
         │  Round Table  │
         │ 100-Round     │
         │   Debate      │
         └──────┬───────┘
                ↓
         EF-Style PPT Memo
```

### Alisa — Founder Edge Analyst
Former YC partner. Evaluates track record, domain expertise, execution signal, and founder-market fit from LinkedIn data.

### Bob — Taste & Network Analyst
Former a16z crypto researcher. Evaluates information diet, thought leadership, network quality, and builder signal from Twitter/GitHub data.

### Round Table
A structured 100-round debate with 4 phases:
1. **Opening Statements** (Rounds 1-5)
2. **Deep Dive & Challenge** (Rounds 6-40)
3. **Stress Test** (Rounds 41-80)
4. **Convergence & Verdict** (Rounds 81-100)

Each agent's conviction level shifts in real-time. The debate produces a final consensus verdict or flags a split decision for human review.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key
cp .env.example .env
# Edit .env and add your Anthropic API key

# Run with candidate URLs
python3 main.py \
  --linkedin "https://linkedin.com/in/someone" \
  --twitter "https://x.com/someone" \
  --github "https://github.com/someone"

# Or try demo mode (no API key needed)
python3 main.py --demo
```

## Demo Mode

Run a full demo with pre-scripted evaluations and a 100-round debate — no API key required:

```bash
python3 main.py --demo
python3 main.py --demo --rounds 20  # shorter demo
```

## Output

The tool generates an EF-branded PowerPoint memo with:
- **Cover** — Candidate name, verdict, edge classification
- **Founder Edge** — Alisa's scores with visual bars
- **Taste & Network** — Bob's scores with visual bars
- **Round Table** — Key turning points from the debate
- **Final Verdict** — Consensus or split decision summary

Output is saved to `./output/<candidate>_memo.pptx`.

## Tech Stack

- **Claude** (Anthropic) — Powers both agents and the debate
- **Rich** — Styled CLI output with real-time streaming
- **python-pptx** — EF-branded PowerPoint generation
- **Jina Reader** — Web scraping for Twitter/LinkedIn profiles
- **GitHub API** — Public profile and repo data

## Project Structure

```
├── main.py              # CLI entry point + demo mode
├── src/
│   ├── config.py        # Colors, prompts, agent personas
│   ├── data_collector.py # GitHub API + Jina web scraping
│   ├── agents.py        # Alisa & Bob evaluations
│   ├── round_table.py   # 100-round debate engine
│   └── ppt_generator.py # PPT memo generation
├── requirements.txt
└── .env.example
```

## License

MIT
