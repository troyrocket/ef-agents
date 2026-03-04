# EF Agents

> **Three AI minds. One decision. Zero bias.**
>
> EF Agents is a Multi-Agent collaboration system that simulates EF's internal candidate review process — three AI reviewers each conduct independent research, engage in real-time debate, reach consensus, and produce a polished investment Memo.

---

## 1. Vision

EF receives thousands of applications every year, and the review team must screen candidates under tight time constraints. EF Agents automates this process — not as a simple scoring system, but as a **simulated investment committee** where three Agents research, discuss, and debate like real partners, ultimately delivering a well-reasoned judgment.

**Core philosophy:** AI doesn't replace human judgment — it uses Multi-Agent debate to reduce individual bias, making evaluation more comprehensive and transparent.

---

## 2. The Three Agents

### Alisa — Founder Edge Analyst
- **Role:** Hard skills & track record evaluator
- **Persona:** Former YC partner, reviewed 5,000+ founders, excels at identifying "outlier signals" from resumes and career trajectories
- **Evaluation Dimensions:**
  - **Track Record:** Do past achievements outperform their peer group? Any 0-to-1 experience?
  - **Domain Expertise:** Depth of expertise in target domain. Any unfair advantages?
  - **Execution Signal:** Completion rate, speed, and impact of past projects
  - **Founder-Market Fit:** Why is this person the right one to build this?
- **Data Source:** LinkedIn Profile (career history, education, skill endorsements)
- **Personality:** Rigorous, data-driven, hard to impress — but gets genuinely excited when she spots a true outlier

### Bob — Taste & Network Analyst
- **Role:** Soft skills & taste evaluator
- **Persona:** Former a16z crypto researcher, deeply embedded in the Web3/AI community, skilled at judging thinking quality from social behavior
- **Evaluation Dimensions:**
  - **Information Diet:** Who do they follow? What do they read? Quality of information sources
  - **Thought Leadership:** Depth and influence of original content
  - **Network Quality:** Connection density with top industry figures
  - **Builder Signal:** GitHub activity, open-source contributions, technical taste
- **Data Source:** Twitter Profile, GitHub Profile
- **Personality:** Sharp intuition, bold opinions, loves discovering talent from unconventional angles

### Carol — Matching Strategist
- **Role:** Co-founder matching strategist
- **Persona:** Former EF Head of Operations, successfully matched 200+ co-founder pairs, deeply understands the chemistry of CEO+CTO pairing
- **Evaluation Dimensions:**
  - **Skill Complementarity:** Technical vs. commercial, product vs. engineering
  - **Vision Alignment:** Match on startup direction and ambition level
  - **Working Style Fit:** Communication style, decision-making preferences, pace
  - **Combined Founder-Market Fit:** Does the pair collectively cover all critical capabilities?
- **Data Source:** Combined results from Alisa and Bob's evaluations + candidate pool data
- **Personality:** Patient, skilled at finding non-obvious complementary relationships, matchmaker's intuition

---

## 3. Product Features

### Feature 1: Individual Candidate Evaluation

**Input:**
```
ef-agents evaluate \
  --linkedin "https://linkedin.com/in/candidate" \
  --twitter "https://twitter.com/candidate" \
  --github "https://github.com/candidate"
```

**Flow (real-time CLI display):**

```
Step 1: Data Collection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Alisa] Scraping LinkedIn profile...        ✓
[Bob]   Scraping Twitter profile...         ✓
[Bob]   Scraping GitHub profile...          ✓

Step 2: Independent Evaluation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Alisa] Analyzing founder edge...           ✓
  → Track Record: 8.5/10
  → Domain Expertise: 9/10
  → Execution Signal: 7/10
  → Founder-Market Fit: 8/10

[Bob]   Analyzing taste & network...        ✓
  → Information Diet: 9/10
  → Thought Leadership: 7.5/10
  → Network Quality: 8/10
  → Builder Signal: 8.5/10

Step 3: Round Table (100-Round Debate)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Alisa] "This candidate has an exceptional track record
         at Google DeepMind, but I'm concerned about the
         lack of 0-to-1 startup experience..."

[Bob]   "I disagree — look at their GitHub. They shipped
         3 open-source projects with 2k+ stars in the last
         year. That's a stronger execution signal than any
         corporate resume line."

[Alisa] "Fair point. The open-source work does demonstrate
         independent initiative. Let me revise my execution
         signal score..."

[Bob]   "Also worth noting — they follow all the key people
         in the AI infra space. Their information diet is
         extremely high-signal."

[Alisa] "Agreed. Updated assessment: STRONG YES with a note
         on cofounder pairing — they need a commercial
         counterpart."

  → 100-round debate completed. Consensus reached.

Step 4: Generate Memo
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[System] Generating EF-style PPT Memo...    ✓
  → Saved to: ./output/candidate_memo.pptx
```

**Output: EF-Style PPT Memo**
- **Slide 1 — Cover:** Candidate name + one-line positioning + avatar
- **Slide 2 — Founder Edge:** Alisa's evaluation summary + radar chart
- **Slide 3 — Taste & Network:** Bob's evaluation summary + key findings
- **Slide 4 — Round Table Highlights:** Key turning points, core disagreements, and final consensus from the 100-round debate
- **Slide 5 — Verdict:** Final recommendation (Strong Yes / Yes / Maybe / No) + admission conditions + ideal co-founder profile

---

### Feature 2: Candidate Pool Matching

**Input:**
```
ef-agents match \
  --pool ./candidates.csv \
  --top 5
```

**Flow:**

```
Step 1: Batch Evaluation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Alisa & Bob] Evaluating 20 candidates...   ✓

Step 2: Matching Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Carol] Running matching algorithm...        ✓
[Carol] Found 5 high-potential pairs.

Step 3: Matching Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Match #1 (Score: 95/100)
  ┌─────────────────┬──────────────────┐
  │ CEO: Alice Wang  │ CTO: David Chen  │
  │ Biz + Product    │ AI/ML Engineer   │
  │ Ex-McKinsey      │ Ex-DeepMind      │
  ├─────────────────┴──────────────────┤
  │ Why: Complementary skills in AI     │
  │ healthcare. Both passionate about   │
  │ personalized medicine. Alice brings │
  │ GTM, David brings deep tech.        │
  └────────────────────────────────────┘

  Match #2 (Score: 91/100)
  ...
```

**Output:**
- Terminal displays Top N matching results
- PPT matching report `./output/matching_report.pptx`

---

## 4. Multi-Agent Collaboration Mechanism

### Round Table Protocol

This is the product's **core highlight** — a **100-round** deep debate that simulates the full discussion process of a real investment committee. Users can watch in real-time, like a live broadcast, as two AI partners move from disagreement to consensus.

**Four-Phase Structure (100 Rounds Total):**

1. **Phase 1 — Opening Statements (Rounds 1-5):** Alisa and Bob each present their independent evaluation results and state their core positions
2. **Phase 2 — Deep Dive & Challenge (Rounds 6-40):** Drill into each evaluation dimension one by one, challenge each other's scoring rationale, present counterexamples and supplementary evidence
3. **Phase 3 — Stress Test (Rounds 41-80):** Devil's advocate mode — take turns playing the opposing side to stress-test the candidate's weaknesses. Discuss risk factors, red flags, and comparisons with other candidates
4. **Phase 4 — Convergence & Verdict (Rounds 81-100):** Gradually converge on disagreements, negotiate final scores, reach consensus, and draft a joint recommendation

**Key Design Decisions:**
- **Full 100-round dialogue**, streamed in real-time to the CLI — users can watch it unfold like a debate tournament
- Each Agent has a "conviction level" (1-10) that dynamically updates after each round — they don't change their minds easily
- Each round is labeled with **round number and phase indicator**, so users can clearly track discussion progress
- **Key turning points** that emerge during discussion are highlighted (e.g., when a piece of evidence causes an Agent to shift position)
- If disagreements remain after 100 rounds, they are explicitly noted as "Unresolved Disagreements" in the Memo

**CLI Display:**
```
Round Table — Phase 2: Deep Dive (Round 23/100)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Alisa] conviction: 7/10 → LEAN YES
"Let's talk about execution speed. Their LinkedIn shows
 they spent 4 years at Google — but what did they actually
 ship? I see a lot of 'led' and 'managed' but no concrete
 product launches..."

[Bob] conviction: 8/10 → YES
"You're reading the LinkedIn wrong. Look at their GitHub —
 they committed 1,200+ times in the last 12 months. They
 built an entire ML pipeline framework that got adopted by
 3 YC companies. That's not a manager, that's a builder
 who happens to work at Google."

[Alisa] conviction: 7 → 8/10  ⚡ SHIFTED
"That's a strong data point I missed. Revising my execution
 signal from 7 to 8.5. But I still want to stress-test
 their ability to operate outside a big-company support
 structure..."

  ▸ Phase progress: ████████░░░░ 23/40
```

---

## 5. Technical Architecture

```
┌─────────────────────────────────────────┐
│              CLI Interface              │
│     (Rich/Textual for styled output)    │
├─────────────────────────────────────────┤
│           Orchestrator Agent            │
│    (manages workflow & round table)     │
├──────────┬──────────┬───────────────────┤
│  Alisa   │   Bob    │      Carol        │
│ (Claude) │ (Claude) │    (Claude)       │
├──────────┴──────────┴───────────────────┤
│           Data Collection Layer         │
│  LinkedIn API / Twitter API / GitHub API│
├─────────────────────────────────────────┤
│           Output Generation             │
│     python-pptx (PPT Memo Builder)     │
└─────────────────────────────────────────┘
```

**Tech Stack (suitable for 1-day build):**
- **Language:** Python
- **LLM:** Claude API (Anthropic SDK)
- **CLI Framework:** Rich (beautiful terminal output, progress bars, live text)
- **Data Collection:** Simplified approach — user pastes profile text or uses public APIs
- **PPT Generation:** python-pptx
- **Agent Framework:** Direct multi-turn conversation via Claude API, no heavy frameworks

---

## 6. Demo Scenario

**Hackathon Demo Flow (5 minutes):**

1. **Opening (30s):** "EF receives thousands of applications every year. We use 3 AI Agents to simulate an investment committee — making evaluation faster, more comprehensive, and more transparent."

2. **Demo: Individual Evaluation (3min):**
   - Input a real (or fictional) strong candidate profile
   - Show real-time CLI output: Data collection → Independent evaluation → 100-round debate
   - Focus on the extended Agent debate (conviction shifts, position changes, gradual convergence)
   - Open the generated PPT Memo

3. **Demo: Matching (1min):**
   - Show candidate pool matching results
   - Show Carol's matching rationale

4. **Closing (30s):** "Three minds. One decision. Zero bias."

---

## 7. MVP Scope (1-Day Build)

### Must Have
- [ ] CLI input for candidate info (text paste first, no API scraping dependency)
- [ ] Alisa independent evaluation + structured scoring
- [ ] Bob independent evaluation + structured scoring
- [ ] Alisa & Bob Round Table (100-round deep debate, 4-phase structure)
- [ ] Real-time streaming CLI display of entire process
- [ ] Auto-generate PPT Memo

### Nice to Have
- [ ] Carol matching feature
- [ ] LinkedIn/Twitter/GitHub automated data collection
- [ ] Radar chart visualization (embedded in PPT)
- [ ] Candidate pool batch processing
