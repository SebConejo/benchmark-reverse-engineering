# RouterArena — Reverse-Engineering Analysis

## Source

- **Paper**: "RouterArena: An Open Platform for Comprehensive Comparison of LLM Routers" — https://arxiv.org/abs/2510.00202v3
- **Repo**: https://github.com/RouteWorks/RouterArena (Apache-2.0, ~74 stars)
- **Year**: October 2024
- **Authors**: Yifan Lu, Rixin Liu, Jiayi Yuan, Xingqi Cui, Shenrun Zhang, Hongyi Liu, Jiarong Xing
- **Institution**: Rice University
- **Relevance**: closest benchmark to our own work (LLM routing evaluation)

## Paper Structure

Non-standard ordering:

1. Introduction
2. Motivation (3 subsections framing the problem narratively)
3. Evaluation Dataset (construction principles)
4. Evaluation Metrics (five metrics defined)
5. Evaluation Framework (ranking mechanism + automation)
6. Experiments (settings + results + difficulty + additional dataset + leaderboard insights)
7. Related Work — placed AFTER experiments
8. Conclusion
9. Appendices A-H (model pools, dataset details, additional results, leaderboard, robustness, hyperparams, prompts, pricing)

Key decisions:
- **Motivation section** gets 3 full subsections before any technical content (unusually prominent)
- **Related Work after experiments**: readers encounter comparison table already knowing RouterArena's capabilities, making the checkmark column a victory lap
- Methodology split across 3 digestible sections (dataset, metrics, framework) instead of one monolith

## Methodology Presentation

**"Principle" framing** for dataset construction:
- Principle 1: DDC-Inspired Domain Coverage
- Principle 2: Bloom-Guided Cognitive Skills
- Principle 3: Empirically Defined Difficulty

This signals deliberate design via borrowed frameworks (DDC, Bloom) applied to a new domain.

**Five numbered metrics** (each with own subsection + math):
1. Query-answer Accuracy
2. Query-answer Cost
3. Routing Optimality
4. Routing Robustness
5. Routing Latency

Justified implicitly by mapping to deployment concerns rather than formal axiomatics.

Reproducibility: main body gives "what and why"; appendices G/H give exact prompts and pricing. Dataset uses 42 models for difficulty calibration (full list in Appendix B.4).

## Results Communication

Deliberate escalation pattern:
1. Deferral curve (Fig 6) — the expected format from routing literature
2. Normalized deferral curve (Fig 7) — novel contribution, both axes to [0,1]
3. Optimality metrics (Fig 8, grouped bars) — reveals routers fail to exploit cheap models
4. Robustness + Latency (Fig 9) — exposes weaknesses
5. Difficulty breakdown (Table 6) — sharp degradation on hard queries
6. Final leaderboard (Table 2) — multi-metric synthesis as culmination

Headline finding framed as surprise: GPT-5 highest accuracy but doesn't rank best because of cost. Validates multi-dimensional evaluation.

**Cost-quality tradeoff visualization** (central concern for routing):
- Raw deferral curve: X=cost per 1k queries, Y=accuracy (%). Oracle line shows theoretical optimum.
- Normalized scatter: both axes [0,1] via log-scaling (cost) + linear (accuracy). Each router = single point.

Scoring formula: weighted harmonic mean with beta parameter (beta=0.1 favors accuracy heavily).

No error bars or CIs. Large dataset (8,400 queries) + robustness as explicit separate metric substitutes for variance reporting.

## Questions the Benchmark Answers

- Which LLM router achieves the best accuracy-cost tradeoff?
- How far are current routers from the oracle?
- Do routers exploit cheap-but-correct model opportunities?
- Which routers are robust to query perturbations?
- How does routing overhead (latency) compare across approaches?
- How does performance degrade on hard queries?

## Limitations Handling

**No dedicated section.** Limitations scattered as observations within results:
- Low robustness across all routers (BERT-based sensitivity)
- High latency for some (external embedding APIs)
- Bloom-level agreement at 54.9% exact match
- Skewed difficulty distribution

Scattered approach softens limitations by framing them as "findings about the field" rather than benchmark weaknesses. Confident positioning.

## Repo Organization

```
router_inference/    # Configs + predictions per router
llm_inference/       # API calling
llm_evaluation/      # Metrics computation
router_evaluation/   # Orchestration
model_cost/          # Pricing data
```

New router submission via PR with `/evaluate` comment trigger for automated scoring. 10% subset for local testing before full submission.

Leaderboard at routeworks.github.io (14 routers ranked). Dataset on HuggingFace.

## Communication / Launch

**Paper-first**: arXiv preprint establishes credibility, leaderboard provides engagement. Abstract links both repo AND leaderboard as first-class artifacts.

Uses promotional language ("first open platform," "comprehensive comparison") while maintaining academic formality. Vision statement ("open community venue") positions as infrastructure.

Automated leaderboard maintenance but governance details thin — no timeline commitments, no update cadence, no funding disclosure.

## Patterns Relevant to TaskBench

1. Principle-based dataset construction signals rigor via borrowed frameworks
2. Five orthogonal metrics prevent gaming
3. Normalized visualization solves unfair cross-pool comparison
4. Point estimates work with large dataset + robustness as separate metric
5. PR-based submission with automated evaluation makes leaderboard self-sustaining
6. Related Work after results turns comparison table into a strength demonstration
7. Scattered limitations = confident positioning for a platform paper
