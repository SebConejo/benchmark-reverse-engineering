# HELM — Reverse-Engineering Analysis

## Source

- **Paper**: "Holistic Evaluation of Language Models" — https://arxiv.org/abs/2211.09110
- **Repo**: https://github.com/stanford-crfm/helm (Apache-2.0, ~2.8k stars)
- **Published**: TMLR 2023 (Featured + Expert + Outstanding Certification). First arXiv: Nov 16, 2022; v2 Oct 1, 2023.
- **Authors**: 47 authors from Stanford CRFM (HAI). Leads: Percy Liang, Rishi Bommasani.
- **Institutional framing**: This is Stanford CRFM's flagship output — the 47-author list signals "community effort within one institution."

## Paper Structure

The paper is ~200 pages with appendices. Section order:

1. Abstract — problem (lack of transparency), contribution (taxonomy + framework), scale (7 metrics, 16 scenarios, 30 models), "living benchmark" framing
2. Introduction — "holistic" = multi-scenario + multi-metric
3. Taxonomy — maps scenario/metric space before showing any results
4. Scenarios — 16 core + 26 targeted, with selection criteria
5. Metrics — formal definitions for 7 metric families
6. Adaptation — prompting standardization
7. Models — catalog of 30 models
8. Results — 25 "top-level findings" organized thematically
9. Targeted evaluations — deeper dives on bias, toxicity
10. Limitations — dedicated section near end
11. Conclusion — ongoing infrastructure, community invitation

**Critical choice**: Methodology occupies the majority (sections 2-7). Results are compressed into a numbered-findings format. Framework > numbers.

## Methodology Presentation

Uses a "map then select" pattern: first shows the full space of possible evaluations, then justifies the subset chosen. This legitimizes the benchmark by showing awareness of exclusions.

Reproducibility: exact cost ($38K), token count (12B), evaluation count (4,900). All prompts and completions released publicly via the website. Model versions documented by API endpoint/date.

Seeds/randomness: not prominent. Deterministic evaluation (fixed prompts, fixed examples). Variance addressed through breadth, not repeated runs.

Metric justification: each metric motivated by real-world concern (fairness → deployment risk, efficiency → accessibility). Deliberately avoids combining into a single score — anti-leaderboard framing in the paper itself.

## Results Communication

Visualizations: taxonomy diagrams, coverage matrices (the "96% coverage" number), multi-metric tables, adaptation procedure diagrams. No radar charts or scatter plots.

Findings are 25 numbered declarative statements ("Instruction tuning is highly effective"). Organized thematically, not by model rank. No single model declared "the best."

Uncertainty: not shown via error bars. Scale (4,900 runs) positioned as the answer to reliability.

Tone: neutral academic with advocacy undercurrent about transparency ("we should aspire for holistic, pluralistic, and democratic benchmarks").

## Questions the Benchmark Answers

- How does model X compare to Y on a specific scenario?
- What is the accuracy-fairness tradeoff?
- Are larger models consistently better across all metrics?
- Which models are most robust to perturbations?
- Which scenarios remain unsolved?
- How much does instruction tuning improve over base?

## Limitations Handling

Dedicated section near end, standard placement. Framed as "design-intentional incompleteness" rather than weaknesses. Limitations reframed as features of a "living benchmark."

Types: scenario coverage necessarily incomplete, metrics don't capture all concerns, commercial API access constraints, temporal decay, English-centric.

Tone: invitational — "we welcome the community to highlight further gaps."

## Repo Organization

```
.github/
docs/             # MkDocs
helm-frontend/    # TypeScript leaderboard UI
scripts/
src/helm/
  benchmark/
    scenarios/    # ~235 files (one .py per scenario)
    metrics/
    adaptation/
    run_specs/    # Config-driven evaluation
    runner.py     # Main entry point
  clients/        # Model API adapters
  common/
  config/
  proxy/
```

README leads with a one-sentence identity, then bullet-point features, then "how to install and run." Functional/instructional — prioritizes usage over philosophy.

Data: downloaded on-demand during runs (code-only repo). License: Apache-2.0.

Plugin architecture: new scenarios, models, and metrics register without modifying core code.

## Communication / Launch

**Full-package launch**: paper (Nov 16, 2022), blog (Nov 17), leaderboard all simultaneous.

Blog opens with societal stakes, not results. More space on *why holistic evaluation matters* than on findings. Advocacy-scholarship.

Leaderboard as living artifact — updated over time with new models. Paper remains a snapshot. Blog directs to "Explore the latest HELM results."

Scale signaling: abstract/blog lead with impressive numbers (30 models, 42 scenarios, $38K, 12B tokens). Authority through exhaustiveness.

Ongoing cadence: periodic updates (HELM Capabilities, HELM Safety, VHELM) maintain visibility without new papers.

## Writing Style & Prose Patterns

### Sentence Structure

Medium-to-long sentences (20-40 words typical), heavily weighted toward complex/compound-complex structures with embedded clauses, parentheticals, and appositives. Simple sentences are rare and reserved for rhetorical emphasis.

> "Unlike previous AI systems, language models are general-purpose text interfaces that could be applied across a vast expanse of scenarios from question answering to summarization to toxicity detection."

> "Transparency begets trust and standards." (rare short punch)

Ratio: ~15% simple, 25% compound, 60% complex. Frequently front-loads subordinate clauses ("Given language models' vast surface...", "Unlike previous AI systems...").

### Hedging & Qualification

Moderate hedging. Empirical findings asserted with "we find that X." Predictions hedged with "could," "suggests," "remains to be seen." Never uses "perhaps" or "it seems" — hedging always tied to temporal uncertainty, not epistemic doubt about their own data.

> Hedged: "This *suggests* that better summarization datasets are desperately needed."
> Asserted: "Instruction tuning... *is* highly effective in terms of accuracy, robustness, and fairness."

### Definition Conventions

Inline, immediately upon introduction, using comma-offset appositives. Pattern: **Term, [appositive definition], [attribution], predicate.** Stacks multiple appositive phrases before reaching the main verb.

> "Instruction tuning, the practice of fine-tuning LMs with human feedback, pioneered by OpenAI and Anthropic, is highly effective..."

### Citation Placement

Inline nominal references — name-drops organization and model together. Citations are densely embedded in examples rather than appended to claims. Heavy parenthetical density (model names + parameter counts in parentheses).

> "Models such as Google's T5 (11B) and Anthropic's Anthropic-LM (52B) were not evaluated on a single dataset in common."

### Punctuation Patterns

- **Colons**: frequent, to introduce elaborations or lists
- **Parentheticals**: extremely heavy (examples, model sizes, metric lists). "e.g.," appears in nearly every paragraph.
- **Em-dashes**: absent. Commas and parentheticals used instead.
- **Semicolons**: rare, only for list items containing commas.

### Voice & Person

Consistently first-person plural "we" for actions, findings, and aspirations. Passive only for describing the state of the field (not their work). Deliberate: **passive = existing problems; active "we" = their contribution.**

> "Let us work together to provide the much needed transparency." (aspirational "we" expanding to community)

### Transitions

Mostly implicit or structural. When explicit: "But," "However," "In contrast to," "Further," "Thus." Avoid "Furthermore," "Moreover," "Additionally." "Overall" marks section summaries.

### Number Phrasing

Concrete specifics embedded in narrative: "which we improve to X" (before/after framing), "over N [unit]" (scale emphasis), "Nx the size" (relative). Never "outperforms by X%" — frames as competitive relationships.

### Recurring Templates

1. "We find that X" — canonical finding opener
2. "[Noun], the practice of [gerund], is [adj]" — stacked appositive
3. "X should Y" — normative prescriptions
4. "This [verb] the importance of X" — drawing implications
5. "[Entity] such as [parenthetical list]" — example enumeration

### Register

Three-register structure: Introduction = elevated, rhetorical, about society. Methodology = precise, definitional, "consists of." Findings = empirical, hedged, "We find." Closing = returns to elevated, aspirational.

### Vocabulary

Accessible academic. Key recurring: "transparency" (thematic keyword), "holistic," "desiderata," "ecosystem," "substrate," "foregrounds." Avoids deep ML jargon; uses evaluation/measurement vocabulary. Rhetorical sections use governance/policy discourse ("democratic," "pluralistic," "norms"). Occasional colloquial punctures ("not yet a slam dunk," "desperately needed") create authoritative-but-human voice.
