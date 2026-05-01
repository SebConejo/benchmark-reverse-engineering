# MMLU — Reverse-Engineering Analysis

## Source

- **Paper**: "Measuring Massive Multitask Language Understanding" — https://arxiv.org/abs/2009.03300
- **Repo**: https://github.com/hendrycks/test (MIT license)
- **Year**: Submitted Sept 7, 2020; ICLR 2021
- **Authors**: Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, Jacob Steinhardt
- **Institution**: UC Berkeley (EECS and Statistics)

## Paper Structure

Sections: Abstract → Introduction (1) → Related Work (2) → A Multitask Test (3) with subsections per discipline → Experiments (4: Setup + Results) → Discussion (5) → Conclusion (6) → Appendices (A: Additional Analysis, B: Test Details).

Methodology (Section 3 + 4.1) occupies roughly half the paper. No dedicated "Limitations" section — limitations woven into Discussion and Appendix A. Enormous appendix space shows example questions from each of 57 subjects (Figures 14-70), making the appendix a showcase of the test itself.

Abstract leads with the contribution ("we provide a test"), pivots to what models cannot do (near random chance), then names specific gaps. Frames the benchmark as a diagnostic of failure, not a celebration of progress.

## Methodology Presentation

Evaluation protocol in Section 4.1. Reproducibility is deliberately minimal in the paper:
- Prompt template given verbatim
- Few-shot count: up to 5 from fixed dev set
- Selection: highest logprob among A/B/C/D
- Temperature: 0
- No seeds (deterministic inference), no model version hashes

More detail lives in the code (`evaluate.py`) than in the paper: retry loops, context-length cropping logic.

Metric justification is implicit — accuracy is the only metric, never formally justified. Random baseline (25%) and human expert performance (~89.8%) serve as anchors.

## Results Communication

Visualizations:
- One leaderboard-style table (Table 1): accuracy by 4 discipline groups + average
- Line plots: MMLU difficulty vs existing benchmarks as f(model size) — establishing MMLU is harder
- Horizontal bar charts: per-task accuracy across 57 subjects (emphasizing variance)
- Scatter plots: calibration (accuracy vs confidence)
- Example question figures

Headline findings ordered: (1) scale matters, (2) performance lopsided across disciplines, (3) counterintuitive patterns (college math > elementary math), (4) calibration is poor.

No confidence intervals or error bars. Variance communicated visually through per-task bar chart spread.

Tone: measured and diagnostic. "Lopsided performance," "knowledge blindspots," "near random-chance accuracy." A challenge to the field.

## Questions the Benchmark Answers

- How well does model X perform on knowledge-intensive tasks vs random chance and human experts?
- Where are the most severe knowledge gaps by discipline/subject?
- Does scaling help, and is the relationship linear?
- Is a model well-calibrated?
- How does MMLU difficulty compare to saturated benchmarks?

## Limitations Handling

No dedicated section. Three locations:
1. Discussion (Section 5): text-only, potential contamination, gap between MC and real-world
2. Appendix A.3 (Format Sensitivity): prompt wording sensitivity — buried
3. Appendix B.2 (Contamination): measures rather than claims absence

Framing: defensive-pragmatic — acknowledged but contextualized as features of evaluation design.

## Repo Organization

Extremely flat:
```
LICENSE (MIT)
README.md
calib_tools.py
categories.py    # 57 subjects → subcategories → 4 macro categories
crop.py
evaluate.py      # Main OpenAI API loop
evaluate_flan.py
```

No subdirectories. Data hosted externally as tar archive. README leads with paper title, author list, one-sentence description, download link, then immediately a leaderboard table.

39 total commits (2020-2023). No CI, no tests, no contributing guidelines. Maximally minimal.

## Communication / Launch

**Paper-first, repo-simultaneous** (same day, Sept 7, 2020). No blog post. Conference amplification via ICLR 2021.

**Leaderboard-in-README pattern**: results table in the README itself. Explicit invitation: "If you want your model added, reach out or submit a PR."

Community adoption via three mechanisms:
1. Other labs self-reporting (Gopher, Chinchilla, FLAN-T5)
2. "MMLU" as catchy shorthand (despite repo named "test")
3. Becoming standard reporting metric in model cards (GPT-4, PaLM, Gemini)

No separate website or hosted leaderboard. Adoption driven by benchmark properties (hard, broad, easy to run) not by marketing or tooling.

The generic repo name "test" suggests authors didn't anticipate canonical status.

## Writing Style & Prose Patterns

### Sentence Structure

Medium-length sentences (20-30 words), strong preference for compound sentences with "but" pivots. Simple declaratives for topic-openers, complex sentences for qualifying results. Very few exceed 40 words or go under 10. Structurally controlled — reads like a textbook.

> "Natural Language Processing (NLP) models have achieved superhuman performance on a number of recently proposed benchmarks."
> "However, these models are still well below human level performance for language understanding as a whole, suggesting a disconnect between our benchmarks and the actual capabilities of these models."

Dominant rhythm: short declarative claim → longer "However" sentence that complicates it.

### Hedging & Qualification

Two-tier system. Hard findings get "we find that" (workhorse epistemic verb). Interpretive claims get "suggest" or "speculate." The distinction is consistent.

> Asserted: "We find that while most recent models have near random-chance accuracy, the very largest GPT-3 model improves over random chance by almost 20 percentage points."
> Hedged: "We speculate that this is in part because GPT-3 acquires declarative knowledge more readily than procedural knowledge."
> Evaluative (rare): "Worryingly, we also find that GPT-3 does not have an accurate sense of what it does or does not know."

Only two explicitly emotional words in the entire paper: "Worryingly" and "concerning."

### Definition Conventions

Always inline, never in separate blocks. Pattern: name the thing, then appositive or relative clause in the same sentence.

> "The General Language Understanding Evaluation benchmark (GLUE) (Wang et al., 2018) was introduced in 2018 to evaluate performance on a wide range of NLP tasks"

Parenthetical-acronym pattern used consistently: full name (ABBREVIATION).

### Citation Placement

Almost exclusively parenthetical, at end of clause. Narrative citations only when the cited work is itself the topic. Multiple citations stacked semicolon-separated.

> "(Zellers et al., 2019; Huang et al., 2019; Bisk et al., 2019)"
> "Brown et al. (2020) also observe that larger GPT-3 models perform better" (rare narrative)

Density: 2-4 per paragraph in Introduction/Related Work, 0-1 in Results.

### Punctuation Patterns

- **Commas** dominate (Oxford comma consistent)
- **Parentheses** heavy: acronyms, citations, clarifying asides "(around 25%)"
- **Semicolons**: absent
- **Em-dashes**: absent
- **Colons**: very rare, only in captions

Extremely conservative punctuation — commas and parentheses do all the work.

### Voice & Person

"We" as dominant subject (~80% of methodology/results sentences). Three modes: methodological "we" (what we did), epistemic "we" (what we found), inclusive "we" (community). Never uses "I," "one," or "it is shown that."

### Transitions

Heavy reliance on "However," (most frequent connector, appears in every section). Also: "In contrast," "Instead," "Consequently," "Additionally," "Overall." "Claim + However" is the signature rhetorical move. Implicit transitions almost nonexistent — always signals logical turns explicitly.

### Number Phrasing

Template: model name/size + metric as percentage + comparison anchor (random chance, another model, expert-level).

> "GPT-3 does better on College Medicine (47.4%) and College Mathematics (35.0%) than calculation-heavy Elementary Mathematics (29.9%)"
> "improves over random chance by almost 20 percentage points on average"

Numbers always percentages. Absolute counts only for dataset sizes and parameter counts.

### Recurring Templates

1. "We find that [claim]." — at least 8 times
2. "[Prior claim]. However, [complication]." — signature move
3. "This [verb] that [interpretation]." — drawing conclusions
4. "To [purpose], we [action]." — methodological choices
5. "[Topic]. [Enumerative expansion with 'and so on']."

### Register

Remarkably stable. Introduction slightly more rhetorical. Results more mechanical and report-like. Discussion shifts to speculative/conditional. Conclusion restates with mild evaluative language. Never informal, never humorous.

### Vocabulary

Technical but accessible. Recurring evaluative words: "lopsided" (distinctive, used twice for vivid image), "blindspots," "shortcomings," "challenging," "concerning." Avoids jargon-heavy constructions. Defines every term inline on first use. Written for broad ML audience, not NLP specialists. Never uses "SOTA" — only "state-of-the-art" as compound adjective.
