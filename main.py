#!/usr/bin/env python3
"""EF Agents — Three AI minds. One decision. Zero bias."""

import argparse
import sys
import time
import os
from dotenv import load_dotenv

load_dotenv()

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from src.config import EF_PURPLE, EF_ORANGE, TOTAL_ROUNDS, get_phase
from src.data_collector import collect_all
from src.agents import run_alisa_evaluation, run_bob_evaluation, parse_scores
from src.round_table import run_round_table, conviction_to_bar
from src.ppt_generator import generate_memo

console = Console()
A = EF_PURPLE  # Alisa color
B = EF_ORANGE  # Bob color


def print_banner():
    banner = f"""
[bold {A}]███████╗███████╗     █████╗  ██████╗ ███████╗███╗   ██╗████████╗███████╗[/]
[bold {A}]██╔════╝██╔════╝    ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝██╔════╝[/]
[bold {B}]█████╗  █████╗      ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   ███████╗[/]
[bold {B}]██╔══╝  ██╔══╝      ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   ╚════██║[/]
[bold {A}]███████╗██║         ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   ███████║[/]
[bold {A}]╚══════╝╚═╝         ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝[/]
"""
    console.print(banner)
    console.print(f"  [bold {B}]Three AI minds. One decision. Zero bias.[/]")
    console.print(f"  [dim]Powered by Entrepreneurs First × Claude[/]")
    console.print()


def step_header(step_num: int, title: str):
    console.print()
    console.print(Rule(f"[bold {B}]Step {step_num}: {title}[/]", style=A))
    console.print()


# ======================== DEMO MODE ========================

DEMO_ALISA_EVAL = """TRACK_RECORD_SCORE: 7.5
TRACK_RECORD_ANALYSIS: CS(AI) + Business minor at Northeastern, still early in career but already shipping multiple projects. Built a YC application exporter and SEC filing tracker — shows initiative beyond coursework.

DOMAIN_EXPERTISE_SCORE: 7
DOMAIN_EXPERTISE_ANALYSIS: Broad AI/ML knowledge with hands-on experience across multiple stacks (Python, TypeScript, Rust interests). Not yet deep in one domain but breadth is impressive for age.

EXECUTION_SIGNAL_SCORE: 8.5
EXECUTION_SIGNAL_ANALYSIS: 14 public repos with real shipped products — not toy projects. Built Payless.chat (AI coding assistant), pluely (open-source Cluely alternative), Bulk Autolisting Agent, SEC Tracker. Ships fast and ships often.

FOUNDER_MARKET_FIT_SCORE: 7
FOUNDER_MARKET_FIT_ANALYSIS: Strong builder mentality with clear interest in AI tooling and developer productivity. The YC exporter suggests awareness of startup ecosystem. Good fit for AI/developer tools space.

EDGE_TYPE: Tech Edge + Catalyst Edge
EDGE_ANALYSIS: Primary edge is technical execution speed — ships full products in hackathon timeframes. Secondary catalyst edge shown by breadth of projects and community engagement. Young enough to move faster than incumbents.

OVERALL_SCORE: 7.5
INITIAL_VERDICT: Yes
SUMMARY: A high-velocity young builder with impressive shipping cadence for their age. 14 repos spanning AI assistants, browser extensions, and CLI tools show genuine builder DNA. The combination of CS(AI) depth and business minor suggests strategic thinking beyond pure engineering."""

DEMO_BOB_EVAL = """INFORMATION_DIET_SCORE: 8
INFORMATION_DIET_ANALYSIS: Starred repos reveal excellent taste — MLX (Apple's ML framework), SurrealDB, SpacetimeDB, RustQuant, Laminar (YC S24 observability). This person is tracking cutting-edge AI infra and databases, not just trending repos.

THOUGHT_LEADERSHIP_SCORE: 6
THOUGHT_LEADERSHIP_ANALYSIS: Limited original content creation visible. The get-shit-done-codex repo (16 stars) shows some thought leadership in AI dev workflows, but no major blog posts or Twitter threads yet. Potential is there but not yet realized.

NETWORK_QUALITY_SCORE: 7.5
NETWORK_QUALITY_ANALYSIS: Connected to YC ecosystem (built YC exporter), follows AI/ML community closely. The ArchMC-Development org suggests collaborative building. Twitter network shows engagement with SF tech scene.

BUILDER_SIGNAL_SCORE: 9
BUILDER_SIGNAL_ANALYSIS: This is where they shine. 14 repos, diverse tech stack (TypeScript, Python, Rust interests), real products not just tutorials. Pluely (open-source Cluely) shows ability to identify market opportunity and execute. SEC Tracker and Reddit Stocker show creative applications of AI. Strong hackathon track record.

OVERALL_SCORE: 7.5
INITIAL_VERDICT: Yes
SUMMARY: Exceptional builder signal for someone still in university. Their GitHub starred repos reveal sophisticated taste in infrastructure — they're tracking the right technologies. The gap is in thought leadership and public visibility, but the raw building capability is clearly there."""

DEMO_ROUND_TABLE_SCRIPT = [
    ("Alisa", "Looking at this candidate's profile, I'm seeing a strong execution signal — 14 repos with real shipped products, not toy projects. The CS(AI) + Business minor combination at Northeastern is solid. My main concern is the lack of deep domain expertise in any single area. They're a generalist builder right now.", 7, "Lean Yes"),
    ("Bob", "I want to push back slightly on the 'generalist' label. Look at their starred repos — MLX, SurrealDB, SpacetimeDB, RustQuant. This person is specifically tracking next-gen AI infrastructure and databases. That's not random browsing, that's someone building a mental model of where the stack is going.", 8, "Yes"),
    ("Alisa", "Fair observation about the starred repos. But starring repos and building with them are different things. I want to see evidence of depth, not just breadth. The get-shit-done-codex project with 16 stars is interesting though — it suggests they're thinking about AI development workflows at a meta level.", 7, "Lean Yes"),
    ("Bob", "Let me highlight something else — they built pluely, an open-source alternative to Cluely. That's not just building, that's identifying a market gap and moving on it fast. And the SEC Tracker and Reddit Stocker show they can apply AI to real-world domains like finance. These aren't homework assignments.", 8, "Yes"),
    ("Alisa", "The pluely project is a strong signal, I agree. Building an open-source competitor to a commercial product shows market awareness and confidence. Let me also note the YC exporter — building tools for the YC ecosystem suggests they're deeply embedded in the startup world, not just academia.", 8, "Yes"),
    ("Bob", "Let's drill into the builder signal. Their commit patterns show consistent activity across months, not just hackathon bursts. And the tech stack diversity — TypeScript, Python, Tauri (Rust) — means they're not locked into one framework. They pick the right tool for the job.", 8, "Yes"),
    ("Alisa", "I want to examine the track record dimension more carefully. They're at Northeastern '29, so likely a sophomore or junior. At this stage, having 14 repos with multiple starred projects is genuinely impressive. But I need to flag: no internship experience visible in the data. Is that a concern?", 7, "Lean Yes"),
    ("Bob", "I'd argue the absence of traditional internships is actually a positive signal here. They're building their own products instead of doing corporate rotations. That's exactly the Catalyst Edge that EF values — someone who creates momentum rather than following structured paths.", 9, "Yes"),
    ("Alisa", "That's a compelling reframe. Let me look at the Founder-Market Fit angle. The pattern I see is: AI tooling, developer productivity, and financial data. If they were to start a company in AI-powered developer tools or fintech, they'd have genuine domain familiarity from building in these spaces.", 8, "Yes"),
    ("Bob", "Exactly. And their information diet supports this — following MLX, Laminar (AI observability), system prompts collection (127K stars). They're studying how AI tools are built under the hood. That's the information diet of someone preparing to build in this space.", 9, "Yes"),
    ("Alisa", "Let me push on network quality though. 20 GitHub followers isn't massive. The Twitter presence through Jenny's profile shows SF tech scene engagement, but I'd like to see stronger evidence of connections to established founders or investors.", 7, "Lean Yes"),
    ("Bob", "The network is early-stage, I'll concede that. But being part of ArchMC-Development org and the hackathon circuit suggests they're building connections organically. For someone still in university, the network will come. The builder signal is what matters at this stage.", 8, "Yes"),
    ("Alisa", "Let's look at the execution speed dimension. The Bulk Autolisting Agent was built for a CodeRabbit hackathon — they shipped a full product with AI image analysis and eBay integration in what was likely a weekend. That's remarkable execution velocity.", 8, "Yes"),
    ("Bob", "And look at the project ambition level — it's not building simple CRUD apps. Each project involves API integrations, AI/ML components, and real user-facing functionality. Payless.chat integrates GPT-4, Claude, AND Gemini. That's someone who understands the multi-model landscape.", 9, "Yes"),
    ("Alisa", "Good point about multi-model awareness. In the current AI landscape, understanding the strengths of different models is a genuine competitive advantage. This isn't someone who just uses ChatGPT — they're building on top of multiple LLM providers.", 8, "Yes"),
    ("Bob", "I want to highlight the 'pinger' project too — 'Keep my Supabase alive.' It's tiny but telling. They're deploying real infrastructure, dealing with real production concerns. This person isn't just coding, they're operating.", 8, "Yes"),
    ("Alisa", "That's a micro-signal I would have missed. You're right — operational awareness at this stage is notable. Let me also examine the website xiao.sh — having a personal domain suggests intentionality about personal brand, even if early.", 8, "Yes"),
    ("Bob", "Looking at their tech taste through the lens of starred repos — they're interested in scalability patterns (awesome-scalability, 69K stars), security testing (AIDA), and animation (GSAP MCP server). This breadth of curiosity is what I look for in builder-founders.", 8, "Yes"),
    ("Alisa", "I want to challenge on one dimension: Thought Leadership. We don't see blog posts, technical writing, or Twitter threads. Building is great, but founders also need to attract talent, raise money, and sell. Can they communicate their vision?", 7, "Lean Yes"),
    ("Bob", "Valid concern, but I'd argue the projects themselves communicate vision. The README descriptions are clear and compelling — 'The Open Source Alternative to Cluely' is a positioning statement, not just a description. They know how to frame what they're building.", 8, "Yes"),
    ("Alisa", "That's true — the repo descriptions show marketing instinct. 'Survey-funded AI coding assistant' for Payless.chat is a creative business model description. They're thinking about GTM even in side projects.", 8, "Yes"),
    ("Bob", "Let me bring up the competitive dimension. We see the SEC Tracker and Reddit Stocker — both use AI to process financial data for retail investors. If they decided to go deep on AI-powered financial intelligence, they'd already have working prototypes.", 8, "Yes"),
    ("Alisa", "Agreed. The question is whether they'll pick one direction and go deep, or continue spreading across multiple domains. For EF, that's actually ideal — they come in with multiple potential edges and the matching process helps them focus.", 8, "Yes"),
    ("Bob", "Exactly. This is textbook Catalyst Edge material — someone who moves fast, builds across domains, and needs a co-founder to go deep with. The EF matching process would pair them with someone who has a specific Market or Tech Edge.", 9, "Yes"),
    ("Alisa", "I'm revising my Domain Expertise concern. At their career stage, breadth IS the right strategy. Depth comes from choosing the right co-founder and problem. They have enough technical foundation to go deep in AI tooling, fintech, or developer productivity.", 8, "Yes"),
    ("Bob", "Let's examine the risk factors. Main risk I see: they might be a 'serial side-project builder' who struggles to commit to one thing for 18+ months. The project graveyard in their repos (webcam-test, SideQuest with no description) suggests some pattern of starting and abandoning.", 7, "Lean Yes"),
    ("Alisa", "That's a valid red flag. But I'd counter that in early stages, rapid experimentation IS the right approach. The key question is: when they find the right co-founder and idea, can they sustain focus? The longer-running projects like Payless.chat and SEC Tracker suggest yes.", 8, "Yes"),
    ("Bob", "Fair analysis. Another risk: they're still in university. EF typically wants people who can commit full-time. Would they drop out or defer? The 'hireable: true' flag on GitHub and the lack of current company affiliation suggest they're open to it.", 8, "Yes"),
    ("Alisa", "The hiring availability signal is interesting. Combined with building tools for the YC ecosystem, this person seems oriented toward startup life rather than a traditional career path. That's the right mindset.", 8, "Yes"),
    ("Bob", "Let me score the Information Diet dimension specifically. They're starred 30 repos and the quality is exceptional — top-tier open source projects mixed with niche but important tools. This is someone who curates their learning deliberately.", 8, "Yes"),
    ("Alisa", "Looking at the full picture for Track Record: freshman year they're already shipping production-quality tools. If we project this trajectory forward, by the time they graduate they'll have more shipping experience than most people 5 years into their career.", 8, "Yes"),
    ("Bob", "One more thing on network — the Twitter profile shows SF + NYC presence, involvement in Speedrun and Founders Inc. These are legit founder communities. They're in the right rooms even if the network is still growing.", 8, "Yes"),
    ("Alisa", "Good catch on the founder communities. Speedrun and Founders Inc are selective programs. Being accepted into those validates the builder signal independently of our assessment.", 8, "Yes"),
    ("Bob", "I think we're converging. Let me state clearly: Builder Signal is 9/10, Information Diet is 8/10, Network is growing at 7.5/10, Thought Leadership is the gap at 6/10. Overall, this is a strong yes candidate for EF.", 9, "Yes"),
    ("Alisa", "Agreed with those numbers. My side: Track Record 7.5 (impressive for age), Domain Expertise 7 (broad but not yet deep), Execution Signal 8.5 (exceptional), Founder-Market Fit 7.5 (multiple viable directions). Overall 7.5, Yes.", 8, "Yes"),
    ("Bob", "For the co-founder matching note: they need someone with deep Market Edge — ideally someone with industry experience in fintech, enterprise AI, or developer tools who can bring the domain depth and business network they currently lack.", 9, "Yes"),
    ("Alisa", "Perfect complement analysis. A CEO-type with go-to-market experience in one of those verticals, paired with this candidate's technical execution speed, would be a formidable founding team.", 8, "Yes"),
    ("Bob", "Also worth noting for matching: their working style seems to be 'ship fast, iterate quickly.' They'd pair well with someone more methodical who can provide strategic direction while they execute at speed.", 9, "Yes"),
    ("Alisa", "Let me play devil's advocate now. Biggest concern: this candidate is still in school. Many student builders fail to transition from 'impressive side projects' to 'committed founder.' What evidence do we have that they'll make the leap?", 7, "Lean Yes"),
    ("Bob", "Counter: they built pluely — an open-source alternative to a funded startup (Cluely). That's not a school project, that's a competitive move. Someone who thinks about market positioning at this age is already thinking like a founder.", 8, "Yes"),
    ("Alisa", "But pluely has 0 stars. If the open-source alternative thesis was strong, shouldn't it have gained traction? Is this a case of building the right thing but failing to distribute it?", 7, "Lean Yes"),
    ("Bob", "Fair point on traction. But the get-shit-done-codex has 16 stars — for a meta-prompting framework, that's not bad. Distribution is a learnable skill, and EF provides exactly that support. The raw product instinct is what matters.", 8, "Yes"),
    ("Alisa", "Let me stress-test the depth question one more time. In AI, the field moves so fast that being a generalist can mean being perpetually behind specialists. Can this candidate compete against teams with PhDs in specific AI sub-domains?", 7, "Lean Yes"),
    ("Bob", "They wouldn't compete on research — they'd compete on product. Their edge is taking existing AI capabilities (GPT-4, Claude, open-source models) and wrapping them in useful products faster than anyone else. That's an application-layer edge, not a research edge.", 8, "Yes"),
    ("Alisa", "Good distinction. Application-layer speed vs. research-layer depth. For most AI startups today, the winning formula IS fast application development on top of foundation models. Their approach is actually well-suited to the current market.", 8, "Yes"),
    ("Bob", "Devil's advocate from my side: the 20 GitHub followers is genuinely low. Even for a student, strong builders usually accumulate more of a following. Is this person actually known in any community, or are they building in isolation?", 7, "Lean Yes"),
    ("Alisa", "That could be a marketing/visibility gap rather than a quality gap. Many exceptional builders have low GitHub followers because they don't actively promote their work. The work quality speaks for itself — the visibility can be built.", 8, "Yes"),
    ("Bob", "Agreed. And the ArchMC-Development org membership suggests they're not fully isolated — there's at least a small collaborative community. Let me raise another concern: financial risk. University students often don't have the financial runway to commit to a startup.", 7, "Lean Yes"),
    ("Alisa", "EF addresses this directly with the equity-free grant while ideating. And the $250K investment once a company forms. For a student founder, EF's financial structure is actually ideal — it removes the biggest barrier to committing.", 8, "Yes"),
    ("Bob", "Good point. Let me push harder: is there any red flag in the project selection? The 'pinger' project is literally just keeping a free Supabase instance alive. Does that suggest they're optimizing for free tiers rather than building at scale?", 7, "Lean Yes"),
    ("Alisa", "I read that differently. It shows resourcefulness — using free tools efficiently while focusing energy on building. Most successful founders start scrappy. Jeff Bezos used doors as desks. A pinger script to keep Supabase alive is the modern equivalent.", 8, "Yes"),
    ("Bob", "Ha, fair enough. Scrappy is good. Let me stress-test one more angle: the 'Portfilo' repo (misspelled 'Portfolio') — 'Links to non-code stuff.' Is the attention to detail there? Typos in portfolio branding could be a concern.", 7, "Lean Yes"),
    ("Alisa", "Minor concern. Speed over polish is actually the right priority at the ideation stage. And honestly, some of the best founders I've evaluated had terrible personal branding but exceptional products. I wouldn't weight this heavily.", 8, "Yes"),
    ("Bob", "Agreed, that's a nitpick. Let me raise a structural concern: all their projects are solo. We don't see evidence of collaborative building — no major open-source contributions to other projects, no co-authored repos. Can they work in a team?", 7, "Lean Yes"),
    ("Alisa", "The ArchMC-Development org membership and hackathon participation (CodeRabbit hackathon) suggest some collaborative experience. But you're right that solo building dominates. This is actually why EF's co-founder matching is so critical for this candidate.", 8, "Yes"),
    ("Bob", "Exactly. They've proven they can build solo. The question is whether they can build WITH someone. That's the co-founder chemistry test that happens during the EF program itself.", 8, "Yes"),
    ("Alisa", "Let me do a competitive comparison. Relative to other student builders applying to EF, how does this candidate stack up? In my experience, 14 shipped repos puts them in the top 10% of student applicants.", 8, "Yes"),
    ("Bob", "I'd agree with top 10%. The quality and diversity of projects is exceptional for a university student. Most student applicants have 2-3 course projects and maybe one hackathon win. This person has a genuine product portfolio.", 9, "Yes"),
    ("Alisa", "Risk summary from my side: (1) Commitment risk — still in school, (2) Depth risk — generalist, not yet specialist, (3) Team risk — mostly solo building. All three are addressable through the EF program.", 8, "Yes"),
    ("Bob", "Risk summary from mine: (1) Visibility gap — low public profile, (2) Traction gap — projects built but not widely adopted, (3) Revenue gap — no evidence of generating income from any project. Again, all addressable.", 8, "Yes"),
    ("Alisa", "Interesting that our risk lists are complementary, not overlapping. My concerns are about depth and commitment, yours are about distribution and monetization. Together, these map exactly to why they need a co-founder.", 8, "Yes"),
    ("Bob", "Perfect observation. A co-founder with sales/marketing experience would address my concerns, while a co-founder with deep domain expertise would address yours. The ideal match is clear.", 8, "Yes"),
    ("Alisa", "Let me stress-test the Edge classification. I said Tech Edge + Catalyst Edge. The Tech Edge is real but early — they have technical ability but not yet deep expertise. The Catalyst Edge is strong — they generate projects at impressive velocity.", 8, "Yes"),
    ("Bob", "I'd weight the Catalyst Edge higher. The ability to ship 14 projects while in university, across multiple tech stacks, with real-world applications — that's pure Catalyst energy. The Tech Edge will deepen with focus.", 8, "Yes"),
    ("Alisa", "Agreed. Primary Edge is Catalyst, secondary is Tech. This classification helps with matching — they should be paired with someone whose primary Edge is Market or Tech (deep), creating maximum complementarity.", 8, "Yes"),
    ("Bob", "One final stress test: age and maturity. Building cool projects and running a startup are very different. Startups require handling rejection, managing people, making difficult decisions under uncertainty. Any signal on emotional resilience?", 7, "Lean Yes"),
    ("Alisa", "The diversity of projects suggests they handle failure well — some projects clearly didn't take off (SideQuest, webcam-test) but they kept building new things. That's resilience in action. They don't get stuck on failures.", 8, "Yes"),
    ("Bob", "And leaving internship and school to build full-time — that's visible in the Twitter data from the co-candidate — shows willingness to make bold bets. Though we should note that data point is from the Twitter profile which may be a different person.", 8, "Yes"),
    ("Alisa", "Good catch on data attribution. Let's be careful to evaluate based on confirmed data. The GitHub data alone provides strong enough signal for a Yes recommendation.", 8, "Yes"),
    ("Bob", "Agreed. Even without LinkedIn data (blocked) and attributing Twitter conservatively, the GitHub profile alone tells a compelling story of a high-velocity builder.", 8, "Yes"),
    ("Alisa", "Let me pose the ultimate stress test question: If we had to bet $250K of EF's money on this person building a meaningful company, would we?", 8, "Yes"),
    ("Bob", "Yes, conditional on finding the right co-founder match. The raw material is clearly there — execution speed, technical breadth, market awareness, builder mentality. The co-founder is the catalyst that turns potential into trajectory.", 9, "Yes"),
    ("Alisa", "I concur. The $250K bet is on the team, not just the individual. And this individual brings enough to the table that the right co-founder pairing could produce something exceptional.", 8, "Yes"),
    ("Bob", "Agreed. I'm comfortable with my conviction. Let's move to convergence.", 9, "Yes"),
    ("Alisa", "Let me state my converged position. Overall assessment: 7.5/10. This is a Yes candidate with specific conditions — the co-founder match must address the depth and distribution gaps we identified.", 8, "Yes"),
    ("Bob", "My converged position: 8/10. Also a Yes. I'm slightly more bullish because the builder signal at this age is genuinely rare. The gaps are all addressable through the EF program and the right co-founder.", 9, "Yes"),
    ("Alisa", "Let's align on the Edge classification. Primary: Catalyst Edge. Secondary: emerging Tech Edge. The speed of execution and breadth of projects is the standout quality.", 8, "Yes"),
    ("Bob", "Agreed on Edge classification. For the matching recommendation: ideal co-founder is someone with Market Edge in AI tooling, fintech, or enterprise software. Should be 3-5 years more experienced with go-to-market capability.", 9, "Yes"),
    ("Alisa", "Good matching spec. I'd add: the co-founder should have experience taking products from prototype to paying customers, since that's the gap in this candidate's track record.", 8, "Yes"),
    ("Bob", "Perfect addition. Let me finalize the risk assessment for the memo: Primary risk is commitment (still in school), mitigated by EF's grant structure and the candidate's demonstrated bias toward building over academics.", 9, "Yes"),
    ("Alisa", "Secondary risk is the generalist trap — spreading across too many domains. Mitigated by co-founder matching and the EF advisor who can help focus their energy on the highest-potential direction.", 8, "Yes"),
    ("Bob", "For the memo highlights, I want to emphasize three things: (1) Exceptional builder velocity, (2) Sophisticated technical taste visible in starred repos, (3) Already thinking about markets and positioning, not just technology.", 9, "Yes"),
    ("Alisa", "Agreed on those three highlights. I'd add: (4) Strong Catalyst Edge — generates momentum and ships consistently, which is the hardest thing to teach.", 8, "Yes"),
    ("Bob", "Great addition. Let me draft the joint recommendation: 'We recommend admitting this candidate to the EF program with high priority on co-founder matching. Primary Edge: Catalyst. Key strength: execution velocity. Key gap: needs a co-founder with market depth and distribution experience.'", 9, "Yes"),
    ("Alisa", "I endorse that recommendation. One amendment: add 'Ideal sectors: AI developer tools, fintech intelligence, or AI-powered productivity software — areas where the candidate has demonstrated building experience.'", 8, "Yes"),
    ("Bob", "Amendment accepted. Final question: Strong Yes or Yes? I'm at Yes — impressive but not yet at the level of a candidate who would get Strong Yes (which I reserve for people with notable exits or breakthrough research).", 8, "Yes"),
    ("Alisa", "Agreed on Yes rather than Strong Yes. The potential is high but unproven at scale. A Strong Yes would require evidence of leading a team, generating revenue, or achieving significant traction. This candidate has the trajectory to get there.", 8, "Yes"),
    ("Bob", "So we're aligned: Yes, with strong conviction. Conviction levels: I'm at 8/10, reflecting high confidence tempered by the early-career uncertainty.", 8, "Yes"),
    ("Alisa", "I'm at 8/10 as well. We've reached full consensus on verdict, conviction level, Edge classification, and co-founder matching recommendation. I'm satisfied with this evaluation.", 8, "Yes"),
    ("Bob", "Consensus achieved. Let me state for the record: EF Agents Alisa and Bob jointly recommend this candidate with a verdict of YES. Conviction: 8/10 (both). The evaluation is complete.", 8, "Yes"),
    ("Alisa", "Confirmed. Three AI minds have deliberated. One decision reached. Zero bias in the process. This candidate should proceed to the next stage of the EF application process.", 8, "Yes"),
    ("Bob", "Seconded. Recording final verdict: YES. This concludes the 100-round evaluation of this candidate. Memo will be generated with our full analysis and co-founder matching recommendation.", 8, "Yes"),
    ("Alisa", "Final note for the memo: we recommend the human review committee pay special attention to the co-founder matching — this candidate's success probability increases dramatically with the right pairing.", 8, "Yes"),
    ("Bob", "Agreed. And one last observation: this candidate represents exactly the type of young, high-velocity builder that EF was designed to identify and support. The program is built for people like this.", 8, "Yes"),
]


def run_demo_round_table(total_rounds: int) -> dict:
    """Run a demo round table with scripted dialogue."""
    script = DEMO_ROUND_TABLE_SCRIPT
    rounds_data = []
    transcript_lines = []
    prev_convictions = {"Alisa": 5, "Bob": 5}

    console.print()
    console.print(Rule(f"[bold {B}]ROUND TABLE — {total_rounds}-ROUND DEBATE[/]", style=A))
    console.print()

    prev_phase = ""
    for i in range(min(total_rounds, len(script))):
        agent_name, text, conviction, verdict = script[i]
        round_num = i + 1
        phase_name, _ = get_phase(round_num)
        ac = A if agent_name == "Alisa" else B  # Agent color

        if phase_name != prev_phase:
            console.print()
            console.print(Rule(f"[bold {B}]{phase_name}[/]", style=A))
            console.print()
            prev_phase = phase_name

        # Round label
        console.print(f"  [bold {ac}][{agent_name}][/] [dim]Round {round_num}/{total_rounds}[/]")

        # Simulate streaming
        console.print(f"  [dim]\"[/]", end="")
        words = text.split()
        for j, word in enumerate(words):
            console.print(word, end="", highlight=False)
            if j < len(words) - 1:
                console.print(" ", end="")
            time.sleep(0.02)
        console.print(f"\"")

        # Conviction display
        prev_conv = prev_convictions[agent_name]
        shifted = conviction != prev_conv
        shift_indicator = ""
        if shifted:
            direction = "↑" if conviction > prev_conv else "↓"
            shift_indicator = f" [bold {ac}]⚡ {prev_conv}→{conviction}{direction}[/]"

        bar = conviction_to_bar(conviction)
        console.print(
            f"  [dim]conviction:[/] [{ac}]{bar}[/] "
            f"[bold {ac}]{conviction}/10[/] → [bold]{verdict}[/]{shift_indicator}"
        )
        console.print()

        prev_convictions[agent_name] = conviction
        rounds_data.append({
            "round": round_num, "agent": agent_name, "phase": phase_name,
            "text": text, "conviction": conviction, "verdict": verdict, "shifted": shifted,
        })
        transcript_lines.append(f"[Round {round_num}] {agent_name}: {text}")

    # Final summary
    console.print()
    console.print(Rule(f"[bold {B}]DEBATE CONCLUDED[/]", style=A))
    console.print(f"  [bold {A}]Alisa[/] final: 8/10 → Yes")
    console.print(f"  [bold {B}]Bob[/]   final: 8/10 → Yes")
    console.print(f"\n  [bold {B}]✓ Consensus: Yes[/]")
    console.print()

    return {
        "rounds": rounds_data, "transcript": transcript_lines,
        "alisa_final_conviction": 8, "alisa_final_verdict": "Yes",
        "bob_final_conviction": 8, "bob_final_verdict": "Yes",
        "consensus": True, "final_verdict": "Yes",
    }


def main():
    parser = argparse.ArgumentParser(
        description="EF Agents — AI-powered candidate evaluation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example:\n  python3 main.py --linkedin URL --twitter URL --github URL\n  python3 main.py --demo  (run with mock data)"
    )
    parser.add_argument("--linkedin", default="", help="LinkedIn profile URL")
    parser.add_argument("--twitter", default="", help="Twitter/X profile URL")
    parser.add_argument("--github", default="", help="GitHub profile URL")
    parser.add_argument("--rounds", type=int, default=TOTAL_ROUNDS, help=f"Debate rounds (default: {TOTAL_ROUNDS})")
    parser.add_argument("--output", default="./output", help="Output directory for PPT memo")
    parser.add_argument("--demo", action="store_true", help="Run in demo mode (no API key needed)")

    args = parser.parse_args()

    if not args.demo and not (args.linkedin and args.twitter and args.github):
        parser.error("Either --demo or all three URLs (--linkedin, --twitter, --github) are required")

    print_banner()

    # Step 1: Data Collection
    step_header(1, "Data Collection")

    if args.demo:
        console.print(f"  [bold {B}]⚡ DEMO MODE[/]")
        console.print()

    with Progress(
        SpinnerColumn(style=A),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"[{A}]Collecting candidate data...", total=None)
        if args.demo:
            candidate_data = collect_all(
                "https://www.linkedin.com/in/arthurna/",
                "https://x.com/imjennywen",
                "https://github.com/undeemed",
            )
        else:
            candidate_data = collect_all(args.linkedin, args.twitter, args.github)
        progress.update(task, description=f"[{B}]✓ Data collection complete[/]")

    candidate_name = candidate_data["candidate_name"]
    console.print(f"  [bold]Candidate:[/] {candidate_name}")

    data_table = Table(show_header=False, box=None, padding=(0, 2))
    data_table.add_column(style=f"bold {A}")
    data_table.add_column()
    linkedin_status = f"[{B}]✓ Collected[/]" if candidate_data["linkedin_raw"] else "[dim]⚠ Unavailable (LinkedIn blocked)[/]"
    twitter_status = f"[{B}]✓ Collected[/]" if candidate_data["twitter_raw"] else "[dim]⚠ Unavailable[/]"
    github_repos = len(candidate_data["github"].get("repos", []))
    github_status = f"[{B}]✓ {github_repos} repos, {candidate_data['github'].get('followers', 0)} followers[/]"
    data_table.add_row("LinkedIn", linkedin_status)
    data_table.add_row("Twitter/X", twitter_status)
    data_table.add_row("GitHub", github_status)
    console.print(data_table)

    # Step 2: Independent Evaluation
    step_header(2, "Independent Evaluation")

    if args.demo:
        alisa_eval = DEMO_ALISA_EVAL
        bob_eval = DEMO_BOB_EVAL
    else:
        console.print(f"  [bold {A}][Alisa][/] Analyzing founder edge...")
        alisa_eval = run_alisa_evaluation(candidate_data["combined_text"])
        console.print(f"  [{A}]✓[/] Alisa complete")
        console.print()
        console.print(f"  [bold {B}][Bob][/] Analyzing taste & network...")
        bob_eval = run_bob_evaluation(candidate_data["combined_text"])
        console.print(f"  [{B}]✓[/] Bob complete")

    alisa_scores = parse_scores(alisa_eval)
    bob_scores = parse_scores(bob_eval)

    console.print(f"  [bold {A}][Alisa][/] Founder Edge")
    for key, label in [
        ("TRACK_RECORD_SCORE", "Track Record"), ("DOMAIN_EXPERTISE_SCORE", "Domain Expertise"),
        ("EXECUTION_SIGNAL_SCORE", "Execution Signal"), ("FOUNDER_MARKET_FIT_SCORE", "Founder-Market Fit"),
    ]:
        console.print(f"    → {label}: [bold {A}]{alisa_scores.get(key, '?')}/10[/]")
    console.print(f"    → Edge: [bold {A}]{alisa_scores.get('EDGE_TYPE', 'N/A')}[/]")
    console.print(f"    → Verdict: [bold]{alisa_scores.get('INITIAL_VERDICT', 'N/A')}[/]")
    console.print()

    console.print(f"  [bold {B}][Bob][/] Taste & Network")
    for key, label in [
        ("INFORMATION_DIET_SCORE", "Information Diet"), ("THOUGHT_LEADERSHIP_SCORE", "Thought Leadership"),
        ("NETWORK_QUALITY_SCORE", "Network Quality"), ("BUILDER_SIGNAL_SCORE", "Builder Signal"),
    ]:
        console.print(f"    → {label}: [bold {B}]{bob_scores.get(key, '?')}/10[/]")
    console.print(f"    → Verdict: [bold]{bob_scores.get('INITIAL_VERDICT', 'N/A')}[/]")

    # Step 3: Round Table
    step_header(3, f"Round Table ({args.rounds}-Round Debate)")

    if args.demo:
        round_table_result = run_demo_round_table(args.rounds)
    else:
        round_table_result = run_round_table(
            alisa_eval=alisa_eval, bob_eval=bob_eval,
            candidate_data=candidate_data["combined_text"], total_rounds=args.rounds,
        )

    # Step 4: Generate Memo
    step_header(4, "Generate Memo")

    with Progress(
        SpinnerColumn(style=A),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"[{A}]Generating EF-style PPT Memo...", total=None)
        filepath = generate_memo(
            candidate_name=candidate_name, alisa_eval=alisa_eval, bob_eval=bob_eval,
            alisa_scores=alisa_scores, bob_scores=bob_scores,
            round_table_result=round_table_result, output_dir=args.output,
        )
        progress.update(task, description=f"[{B}]✓ Memo saved[/]")

    console.print(f"  [{B}]✓[/] Saved to: [bold]{filepath}[/]")

    # Final Summary
    console.print()
    console.print(Rule(f"[bold {B}]EVALUATION COMPLETE[/]", style=A))
    console.print()
    summary_panel = Panel(
        f"[bold]Candidate:[/] {candidate_name}\n"
        f"[bold {A}]Alisa (Founder Edge):[/] {alisa_scores.get('OVERALL_SCORE', '?')}/10 → {round_table_result['alisa_final_verdict']}\n"
        f"[bold {B}]Bob (Taste & Network):[/] {bob_scores.get('OVERALL_SCORE', '?')}/10 → {round_table_result['bob_final_verdict']}\n"
        f"[bold]Final Verdict:[/] [bold {B}]{round_table_result['final_verdict']}[/]\n"
        f"[bold]Memo:[/] {filepath}",
        title=f"[bold {B}]EF AGENTS[/]",
        border_style=A,
        padding=(1, 2),
    )
    console.print(summary_panel)
    console.print()
    console.print(f"  [{B}]Three AI minds. One decision. Zero bias.[/]")
    console.print()


if __name__ == "__main__":
    main()
