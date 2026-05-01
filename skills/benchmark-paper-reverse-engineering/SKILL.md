---
name: benchmark-paper-reverse-engineering
description: Reverse engineer published LLM benchmark papers and their associated GitHub repos to extract patterns for methodology presentation, results communication, repo organization, and limitations handling. Use when the user wants to study how existing benchmarks are written and structured before publishing their own. Triggers on "reverse engineer benchmark", "study how benchmarks are published", "analyze benchmark papers", "/benchmark-reverse".
---

# Benchmark Paper Reverse Engineering

## When to use

Use this skill when the user is preparing to publish their own LLM benchmark and wants to learn from existing published benchmarks. The goal is to extract patterns: how leading benchmarks present methodology, communicate results, organize their repo, handle limitations, and respond to anticipated criticism.

The user provides the list of benchmarks to analyze in their prompt. Do not hardcode a default list.

Do NOT use this skill for performance benchmarking (Core Web Vitals, API latency) or for protocol reverse engineering (network traffic).

## Workflow

### Step 1: For each benchmark provided, analyze the following dimensions

For each benchmark URL the user provides, read the README, parse the repo structure, find the associated arxiv paper, and write an analysis covering these dimensions. Write in free-form prose, not as a fill-in-the-blank template. The dimensions are what to look at, not what to format.

- **Source** — paper URL, repo URL, year, authors / institution
- **Paper structure** — section order, where methodology sits, where results sit, how the abstract is framed (problem-first, gap-first, results-first), placement of limitations
- **Methodology presentation** — how the evaluation protocol is described, level of reproducibility detail (seeds, prompts, model versions), how metrics are justified, transparency on human vs LLM judging
- **Results communication** — types of plots and tables used, ordering of headline findings, how uncertainty / variance is shown, how surprising findings are handled, tone (academic neutral, advocacy, defensive)
- **Questions the benchmark answers** — what specific questions can a reader answer using this benchmark? What is the benchmark useful for in practice?
- **Limitations handling** — dedicated section vs scattered, what types of limitations are pre-emptively addressed, framing (defensive, transparent, future-work-ready)
- **Repo organization** — top-level structure, what the README leads with, where the data lives, evaluation scripts layout, leaderboard / viewer / website, reproducibility files, license, issue templates
- **Communication / launch** — blog post, X thread, talk; paper-first vs blog-first vs leaderboard-first; phased release vs all-at-once; community submission patterns
- **Writing style & prose patterns** — how sentences are constructed at the clause level. Look for: sentence length distribution (short declarative vs long compound), use of hedging language ("we find that" vs "this shows"), how claims are qualified, whether definitions are given inline before using a term, citation density (every claim backed vs sparse references), use of em-dashes / parentheticals / semicolons, how lists are introduced, whether the voice is active or passive, how transitions between paragraphs work (explicit connectors vs implicit), vocabulary register (formal academic vs accessible technical), how numbers and comparisons are phrased ("X outperforms Y by Z%" vs "X achieves Z%, compared to Y's W%"), whether authors use "we" or impersonal constructions, and any recurring sentence templates or rhetorical moves that appear across sections (e.g. "To address this, we...", "Notably, ...", "In contrast to prior work..."). The goal is to extract a style guide from how researchers actually write, not to describe the content.

Save each analysis to `reverse-engineering/<benchmark-name>.md`.

### Step 2: Produce the synthesis

After all benchmarks are analyzed, write `reverse-engineering/synthesis.md` with the following sections:

- **Recurring patterns** — patterns that appear across the majority of benchmarks studied. For each, name which benchmarks use it. Cover patterns in paper structure, methodology presentation, results communication, limitations handling, repo organization, and launch.
- **Divergent patterns** — where the benchmarks differ meaningfully. E.g. methodology-first vs results-first abstracts, dedicated limitations section vs scattered, leaderboard-driven vs paper-driven launches.
- **What the best benchmarks do** — pick the strongest 2-3 (by citation, adoption, or clarity) and call out what specifically makes their presentation strong.
- **What to avoid** — patterns that look weak, defensive, unclear, or that aged poorly.
- **Recommendations for our benchmark** — direct, actionable recommendations covering paper structure, repo organization, results presentation, limitations handling, launch strategy, and writing style.
- **Writing style guide** — a concrete, usable style guide extracted from the analyzed papers. Cover: sentence templates that recur (with examples), how to introduce a claim, how to hedge vs assert, citation placement conventions, punctuation patterns, definition conventions, vocabulary to use and avoid, and the register shift between abstract/intro (accessible) vs methodology (precise) vs results (declarative). This section should be directly usable by a redaction agent writing the paper.

The synthesis is the most important deliverable. The per-benchmark analyses are evidence; the synthesis is what the redaction agent will use.

### Step 3: Persist learnings

After the synthesis is written, run `/learn` to persist the key patterns and recommendations so a separate session (the redaction agent) can retrieve them later.

## Discipline

- Do not recommend a structure for the user's own benchmark until all benchmarks have been analyzed. Premature recommendations bias the analysis.
- Do not pick benchmarks that are not LLM evaluations (e.g. ImageNet, GLUE pre-LLM era) if the user's list is ambiguous. Stick to modern LLM evaluation benchmarks where the publication norms match.
- Do not summarize benchmarks for their own sake. The point is to extract presentation patterns, not to teach what each benchmark is about.
