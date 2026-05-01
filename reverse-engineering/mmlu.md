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
