# Paper Outline v2 — Detailed

**Date:** 2026-05-19
**Status:** For final validation. No drafting until signed off.
**Revision:** v2.1 — applied 5 fixes from PAPER_OUTLINE_REVIEW_FINAL.md

---

## Title Candidates

| # | Title | Angle |
|---|-------|-------|
**Final title (validated 2026-05-19):**

> **TaskBench: Measuring Cost-Quality Tradeoffs Across 46 LLMs and 21 Production Tasks**

---

## Abstract (200 words)

We benchmark 46 large language models from 9 API providers across 21
production tasks — spanning sentiment classification, intent detection,
code generation, mathematical reasoning, and 17 others — measuring both
per-query cost and quality on 50 cases per task (51,580 scored cases
total). We find that Economy-tier models ($0.05–$0.50/M input tokens)
show no statistically significant quality gap versus Premium models
($5+/M) on any of the 21 tasks (Mann-Whitney p>0.05, 21/21). Within
providers, paying 750× more buys at most +0.13 quality points on a 1–5
scale. Per-task routing to the cheapest adequate model reduces cost by
99.7% versus the best single model while matching its quality. Quality
scores are produced by an LLM judge validated against ground truth on
3 task types (r=0.89–0.91). We release the full dataset, raw model
responses, and evaluation prompts.

**Findings referenced:** F1, F2, F4, F13
**Key numbers:** 46 models, 21 tasks, 51,580 rows, 9 providers, p>0.05 21/21, 750×, +0.13, 99.7%, r=0.89–0.91
**Sources:** stats_validation.json, provider_gradient.json, routing_savings.json, judge_v2_validation.json

---

## 1. Introduction (1 page)

### 1.1 The Problem

Practitioners choose LLMs by reputation or leaderboard rank. Existing benchmarks
(MMLU, Chatbot Arena, HELM) measure capability but not per-task cost-efficiency.
A model ranked #1 on Arena may cost 100× more than the #5 model for identical
quality on sentiment classification. No public dataset lets a practitioner answer:
"For this specific task, which model gives me 4.5/5 quality at the lowest cost?"

**Findings:** none (motivation)
**Figures:** none
**Key numbers:** none
**Length:** ~10 lines

### 1.2 Our Contributions

Three contributions:
1. **TaskBench** — the first benchmark measuring per-task cost-quality Pareto
   frontiers across 46 models, 21 production tasks, 9 providers, 4 price tiers
   (51,580 scored cases).
2. **Empirical findings** — Economy-tier models show no significant quality gap
   versus Premium on any task; per-task routing saves 99.7% vs the best model;
   within-provider price gradients are nearly flat.
3. **Judge validation** — we show that standard LLM-as-judge with generic rubrics
   has format bias (r=0.39), fix it with correctness rubrics (r=0.91), and
   release both V1 and V2 scores for reproducibility.

We release all raw responses, scores, and evaluation code.

**Findings:** F1, F2, F4, F13
**Figures:** none
**Key numbers:** 46 models, 21 tasks, 9 providers, 51,580 cases, r=0.39→0.91
**Sources:** stats_validation.json, judge_v2_validation.json
**Length:** ~12 lines

### 1.3 Key Findings Preview

Bulleted preview of the 4 headline findings:
- No Economy–Premium gap detected (F1): Mann-Whitney p>0.05 on 21/21 tasks.
  Premium avg 4.791 vs Economy 4.749 — gap of 0.042 on a 1–5 scale.
- Flat provider gradients (F4): Anthropic Haiku ($0.80/M) ≥ Opus ($15/M).
  Google Flash ($0.15/M) ≈ Pro ($1.25/M). OpenAI: 750× price = +0.13 quality.
- Per-task routing saves 99.7% vs o3 while matching its quality on every task (F2).
- 5 Economy models cover all 21 tasks at ≥4.5 quality. Cheapest: Grok 4 Fast
  at $0.000435/query average (F9).

**Findings:** F1, F2, F4, F9
**Figures:** none
**Key numbers:** p>0.05 21/21, 4.791 vs 4.749, 0.042, $0.80 vs $15, 750×, +0.13, 99.7%, 5 models, $0.000435/query
**Sources:** stats_validation.json, provider_gradient.json, routing_savings.json, coverage_matrix.json
**Length:** ~12 lines

---

## 2. Related Work (0.5 page)

### 2.1 General LLM Benchmarks

Position against HELM (multi-metric but no cost axis), Chatbot Arena (human pref
but one aggregate Elo, no per-task), MMLU/MMLU-Pro (academic knowledge, not
production tasks), Berkeley Function Calling (single task). TaskBench adds cost as
a first-class axis and provides per-task granularity across 21 diverse tasks.

**Findings:** none
**Figures:** none
**Length:** ~8 lines

### 2.2 Cost-Aware LLM Evaluation and Routing

FrugalGPT (Chen et al. 2023) introduced LLM cascading for cost reduction but
evaluated on 1 task with 3 models. RouterBench and RouteLLM benchmark router
systems, not models. Artificial Analysis tracks speed and aggregate price but not
per-task quality. We produce the underlying per-task cost-quality data that any
router can consume.

**Findings:** none
**Figures:** none
**Length:** ~8 lines

### 2.3 LLM-as-Judge

MT-Bench (Zheng et al. 2023) introduced LLM judges. Known biases: position bias,
verbosity bias (Saito et al. 2023), self-enhancement (Panickssery et al. 2024).
We identify a specific format bias that distorts cost-quality comparisons: generic
rubrics reward concise formatting over correctness, systematically favoring
Economy models. We quantify this (r=0.39→0.91) and release both V1/V2 scores.

**Findings:** F13
**Figures:** none
**Key numbers:** r=0.39→0.91
**Sources:** judge_v2_validation.json
**Length:** ~8 lines

---

## 3. Methodology (1.5 pages)

### 3.1 Benchmark Design

21 production tasks in 4 categories, 50 cases each from standard datasets:
- **Classification** (4 tasks, exact-match): sentiment (SST-2), intent (CLINC-150),
  moderation (ToxiGen), multistep reasoning (ARC-Challenge).
- **Structured output** (5 tasks, LLM-judge): extraction, JSON transform, NER,
  function calling, structured output.
- **Generation** (8 tasks, LLM-judge): code gen (HumanEval), code review, test gen,
  summarization ×2, email, data-to-text, code explanation.
- **Reasoning & language** (4 tasks, LLM-judge): math (GSM8K), RAG QA (SQuAD v2),
  translation EN→FR (OPUS-100), instruction following.

Each case has a fixed prompt. Models receive identical inputs with temperature=0
(or 1 for models rejecting 0). Two tasks have <50 cases due to dataset size:
code_explanation (48), structured_output (41).

**Findings:** F3
**Figures:** none
**Key numbers:** 21 tasks, 4 categories, 50 cases, 4 exact-match + 17 LLM-judged
**Length:** ~15 lines (includes compact task table)

### 3.2 Model Selection

46 complete models (21/21 tasks, ≥40 valid cases each) across 9 API providers
and 4 price tiers. Tier boundaries: Premium ≥$5/M, Standard $0.50–$4.99/M,
Economy $0.05–$0.49/M, Micro <$0.05/M input tokens.

Tier distribution: Premium n=2 (Claude Opus, GPT-5.5 Pro), Standard n=22,
Economy n=15, Micro n=9. Providers: OpenAI (10 models), Qwen (7), Mistral (5),
Anthropic (4), Google (3), ByteDance (3), Meta/Llama (3), others.

Cost measured as per-query cost from token counts × provider-published prices
at benchmark time (April–May 2026). Reasoning model costs verified against
provider billing (reasoning tokens included in completion_tokens for o3, o4-mini;
see Limitations for GPT-5.5 Pro cost discrepancy).

**Findings:** none (descriptive)
**Figures:** none (full model table in Appendix B)
**Key numbers:** 46 models, 9 providers, 4 tiers, n per tier = 2/22/15/9
**Sources:** task_model_aggregates.json (model list)
**Length:** ~12 lines

### 3.3 Scoring

Two evaluation methods:
- **Exact match** (4 classification tasks): model output compared to gold label
  after normalization. Score: 1 (correct) or 0 (incorrect), averaged to accuracy.
- **LLM-as-judge** (17 generative tasks): GPT-4o with task-specific correctness
  rubrics, 1–5 scale. Each rubric defines what 1, 3, and 5 mean for that
  specific task (e.g., GSM8K: "5 = numerical answer matches expected, reasoning
  steps are sound"). Anti-format instruction: "Ignore formatting, verbosity,
  and style. Evaluate only correctness and completeness."

Statistical methods: bootstrap 95% CIs (1,000 iterations), Mann-Whitney U for
tier comparisons, Kruskal-Wallis for multi-group comparisons.

**Findings:** none (method)
**Figures:** none (judge prompts in Appendix D)
**Key numbers:** 4 exact-match tasks, 17 LLM-judged tasks, GPT-4o judge, 1–5 scale
**Length:** ~12 lines

### 3.4 Judge Validation

We validate the LLM judge against ground truth on 3 task types:
- **Math (GSM8K):** judge score vs numerical accuracy. V1 (generic rubrics,
  GPT-4o-mini): r=0.388. V2 (correctness rubrics, GPT-4o): r=0.905.
- **RAG QA (SQuAD v2):** judge score vs exact-match accuracy. V1: r=−0.013.
  V2: r=0.888.
- **Code generation (HumanEval):** judge score vs pass@1 execution rate.
  V2: r=0.891 (V1 not available — code execution added post-V1).

The V1→V2 improvement is driven by rubric specificity, not judge model upgrade:
V1 evaluated "quality" (rewarding concise formatting), V2 evaluates correctness
(penalizing wrong answers regardless of style). The bias changed 34.7% of
pairwise model rankings across all tasks (5,195 of 14,972 pairs flipped).

We applied V2 rubrics to all 17 LLM-judged tasks (40,350 cases re-scored at
~$54). The 15 tasks without ground truth are validated by mechanism consistency
(same rubric structure) and V1→V2 directional consistency, not by direct
ground-truth correlation. This is a limitation.

**Findings:** F13, F14
**Figures:** none in main text (V1-vs-V2 scatter in Appendix C)
**Key numbers:** r=0.388→0.905 (GSM8K), r=−0.013→0.888 (RAG QA), r=0.891 (code), 34.7% ranking flips, 5,195/14,972 pairs, 40,350 re-scored, ~$54
**Sources:** judge_v2_validation.json (V1/V2 r values), judge_v2_validation_code_v4.json (code r), ranking_flips.json (flip rate)
**Length:** ~18 lines. This is the longest methodology sub-section but stays under 0.5 page.

---

## 4. Results (3 pages)

### 4.1 Cost-Quality Landscape

Overview of the 46×21 benchmark matrix. The dominant pattern: most of the
landscape is green (≥4.5/5). Quality variance comes from 10 high-discrimination
tasks (score spread >1.5 across models) where model choice matters, versus 11
low/medium-discrimination tasks where any model above Micro tier works.

Most discriminative tasks: intent_clinc150 (spread 3.2, std 0.624), rag_qa
(spread 2.84, std 0.560), moderation_toxigen (spread 2.4), test_generation_v2
(spread 2.4). Least discriminative: structured_output (spread 0.29),
code_explanation (spread 0.81), multistep_reasoning (spread 0.80).

Practical implication: for 11 of 21 tasks, model selection is irrelevant — pick
the cheapest. The remaining 10 tasks drive all the cost-quality decisions.

**Findings:** F3, F6
**Figures:**
- **Figure 1** — Heatmap (46 models × 21 tasks, color = avg score). Rows sorted
  by avg score, columns grouped by category. Inserted here.
  (Task discriminativeness bar chart moved to Appendix H.)
**Key numbers:** 10 high-discrimination tasks (spread >1.5), 11 medium/low, spread range 0.29–3.2
**Sources:** task_discriminativeness.json
**Length:** ~15 lines + 1 figure

### 4.2 Tier Comparison: Economy Matches Premium

The headline finding. Bootstrap 95% CIs per tier:
- Premium: 4.791 [4.729, 4.853], n=2 (42 task-model pairs)
- Standard: 4.787 [4.765, 4.808], n=22 (451 pairs)
- Economy: 4.749 [4.715, 4.777], n=15 (313 pairs)
- Micro: 4.519 [4.435, 4.599], n=9 (210 pairs)

Premium–Economy gap: 0.042 points (0.9% of the 1–5 scale). CIs overlap heavily.
Mann-Whitney p>0.05 on all 21 tasks individually. The finding holds at task level:
on no single task does Premium significantly outperform Economy.

Micro is the only tier with a meaningful gap (−0.27 vs Premium). The three-tier
world (Standard/Economy/Micro) is the practical reality — Premium adds no
detectable quality.

Caveat: n=2 Premium models limits statistical power. The finding is "no
difference detected," not "tiers are equal." A future benchmark with 5+ Premium
models could detect a small gap. But even if a gap exists, it is bounded at
<0.12 (upper CI of Premium minus lower CI of Economy).

**Findings:** F1
**Figures:**
- **Figure 3** — Tier comparison bar chart with bootstrap CIs. 4 groups
  (Premium/Standard/Economy/Micro), error bars = 95% CI. Inserted here.
**Key numbers:** 4.791 vs 4.749, gap 0.042, CIs [4.729–4.853] vs [4.715–4.777], p>0.05 21/21, n=2 Premium
**Sources:** stats_validation.json
**Length:** ~18 lines + 1 figure

### 4.3 Per-Task Pareto Frontiers and Routing Savings

For each task, we compute the cost-quality Pareto frontier: the set of models
where no other model is both cheaper AND higher quality. The key observation:
Premium models are almost never on the frontier. The frontier is dominated by
Economy and Micro models.

Per-task routing to the cheapest model matching o3 quality on each task saves
99.7% ($0.003332/query → $0.000009/query). Even against the cheapest universal
model (Grok 4 Fast at $0.000435/query, the cheapest single model covering all
21 tasks at ≥4.5), routing saves ~98%.

**Findings:** F2, F9, F16, F17
**Figures:**
- **Figure 4** — Pareto dual-panel: RAG QA (high-discrimination task). Shows
  dense cheap cluster + Premium outliers off the frontier. Style per
  PARETO_STYLE_GUIDE.md.
- **Figure 5** — Pareto dual-panel: Data-to-Text (commodity task). Everything
  clustered at 4.8+, illustrating "any model works."
**Key numbers:** 99.7% savings vs o3, $0.003332 → $0.000009, 4 models cover all at ≥4.0, 5 at ≥4.5, GPT-5.4 Nano cheapest on 15/21
**Sources:** routing_savings.json, per_task_routing_savings.json, coverage_matrix.json
**Length:** ~18 lines + 2 figures

### 4.4 Provider Gradient: Paying More Buys Nothing

Within each major provider, the most expensive model is not the best.

- **Anthropic:** Haiku $0.80/M scores 4.775. Opus $15/M scores 4.753. Paying
  19× more gets −0.022 quality.
- **Google:** Flash $0.15/M scores 4.749. Pro $1.25/M scores 4.747. 8× more
  for −0.002.
- **OpenAI:** Nano $0.02/M scores 4.694. GPT-5.5 Pro $15/M scores 4.828. 750×
  more for +0.134 — the largest intra-provider gain, and still only 2.7% of
  the scale.
- **Qwen:** Turbo $0.05/M scores 4.654. Max $2.00/M scores 4.746. 40× more
  for +0.092.
- **Mistral:** Ministral 3B $0.04/M scores 4.441. Large $2.00/M scores 4.800.
  50× more for +0.359 — the only provider where paying more substantially helps,
  driven by the sub-3B model floor.

The gradient is flat at the Standard/Economy boundary. The only steep segment
is Micro→Economy (sub-3B models pulling Micro down).

**Findings:** F4, F5
**Figures:**
- **Figure 6** — Provider gradient: scatter plot (x=input price/M, y=avg score)
  with lines connecting models within each provider family. One line per
  provider (Anthropic, OpenAI, Google, Qwen, Mistral).
**Key numbers:** Haiku 4.775 vs Opus 4.753 (−0.022), Flash 4.749 vs Pro 4.747 (−0.002), Nano 4.694 vs GPT-5.5 Pro 4.828 (+0.134, 750×), Turbo 4.654 vs Max 4.746 (+0.092, 40×)
**Sources:** provider_gradient.json
**Length:** ~18 lines + 1 figure

### 4.5 Model Selection in Practice

**Coverage thresholds.** At quality threshold ≥4.0, 37 of 46 models cover all
21 tasks — model choice barely matters. A 4-model portfolio (GPT-5.4 Nano on
15 tasks, Phi-4 on 3, Qwen Turbo on 2, Gemma 26B on 1) is the cheapest
combination. At ≥4.5, only 5 models qualify as universal (Grok 4 Fast, Seed
2.0 Mini, GPT-5.4, Seed 2.0 Lite, o3); the cheapest is Grok 4 Fast at
$0.000435/query. At ≥4.7, no model covers all 21 tasks — RAG QA,
intent_clinc150, and moderation_toxigen are the bottleneck tasks.

**Generational upgrades.** The coverage frontier keeps moving. GPT-4o → GPT-5.4:
−60% price ($2.50→$1.00/M), +0.089 avg quality. GPT-4o Mini → GPT-5.4 Mini:
−33% price, quality flat (already near ceiling). Sonnet 4 → Sonnet 4.6: same
price, +0.003 quality. The exception is DeepSeek V3.2 → V4 Pro: +211% price
for +0.061 quality. In 3 of 4 provider families, the new generation is cheaper
AND better — upgrading generations is a free lunch.

**Findings:** F9, F10, F11, F16, F17
**Figures:** none (compact threshold table + generational pairs table inline)
**Key numbers:** 37/46 at ≥4.0, 5/46 at ≥4.5, 0/46 at ≥4.7, GPT-4o→5.4 −60% price +0.089 quality, cheapest universal = Grok 4 Fast $0.000435/query
**Sources:** coverage_matrix.json, generational_delta.json
**Length:** ~18 lines + 2 compact inline tables

---

## 5. Discussion (1 page)

### 5.1 Practical Implications

Three recommendations for practitioners:
1. **Default to Economy tier.** On 21/21 tasks, Economy models showed no
   significant quality loss versus Premium. The safest default is the cheapest
   model scoring ≥4.5 on your task.
2. **Route per task for maximum savings.** A 4-model portfolio covers all 21
   tasks at ≥4.0 quality and costs $0.000009/query average (vs $0.003332 for o3).
   The savings come from commodity tasks where Micro-tier models suffice.
3. **Upgrade generations, not tiers.** GPT-5.4 is 60% cheaper than GPT-4o at
   higher quality. The cost-quality frontier moves down-left with each
   generation. Paying for a premium tier within the same generation has near-zero
   ROI.

**Findings:** F1, F2, F4, F10
**Figures:** none
**Length:** ~12 lines

### 5.2 Evaluation Methodology Implications

The format bias finding (§3.4) generalizes beyond this benchmark. Any
LLM-as-judge evaluation using generic "rate quality 1–5" rubrics likely has
this bias. We recommend: (1) always validate against ground truth on ≥2 task
types, (2) use task-specific correctness anchors, (3) report both judge scores
and native metrics where available.

Verbosity is not the primary driver of the bias (r=0.22, p=0.13 between
verbosity and score delta). The mechanism is rubric ambiguity, not output length.

**Findings:** F13, F14, F15
**Figures:** none
**Key numbers:** r=0.22, p=0.13 (verbosity)
**Sources:** verbosity_correlation.json
**Length:** ~8 lines

---

## 6. Limitations (0.5 page)

Bulleted list:
- **n=2 Premium models.** The Economy≈Premium finding is "no difference
  detected," not "equal." Future work: 5+ Premium models.
- **Judge validated on 3/17 LLM-judged tasks.** The remaining 14 are validated by
  mechanism consistency, not ground-truth correlation.
- **50 cases per task.** CIs are ±0.2. Differences <0.3 are not distinguishable
  from noise. Standard for benchmark papers (HELM uses similar sample sizes).
- **Single-turn only.** Multi-turn, vision, and audio are out of scope.
- **Prices snapshot (April–May 2026).** LLM prices drop monthly. Tier-level
  findings are more durable than absolute prices. Raw data released for
  re-computation with current prices.
- **Potential data contamination.** Models may have seen GSM8K, SQuAD, HumanEval
  during training. This affects absolute scores, not relative comparisons
  (all models have the same contamination risk on standard datasets).
- **Reasoning model cost tracking.** GPT-5.5 Pro and o3 reasoning tokens are
  partially invisible. Tracked cost ($143.81) underestimates real spend (~$180+)
  for these models specifically.
- **Model diversity.** Our sample spans 3 geographic origins and both open/closed
  licenses. Neither dimension significantly predicts quality: origin has no
  effect (Kruskal-Wallis p=0.40), and the open-vs-closed gap (0.183, p=0.0004)
  is driven by sub-3B open models (Appendix G).
- **English-only** (except EN→FR translation).

**Findings:** F1 (n=2 caveat), F7, F8, F13 (3/17 validation)
**Figures:** none
**Length:** ~18 lines

---

## 7. Conclusion (0.5 page)

TaskBench provides the first systematic per-task cost-quality benchmark for
production LLM use. Across 46 models and 21 tasks, we find that the
cost-quality curve is remarkably flat: Economy models are statistically
indistinguishable from Premium on every task tested. The practical implication
is clear — practitioners should default to Economy models and use per-task
routing for maximum savings.

We also demonstrate that standard LLM-as-judge evaluation has a format bias
that specifically distorts cost-quality comparisons. Correctness-focused rubrics
fix this with minimal effort.

We release all 51,580 scored cases, 51,705 raw model responses, evaluation
prompts, and analysis code. We encourage the community to extend TaskBench
with more Premium models, multi-turn tasks, and longitudinal price tracking.

**Findings:** F1, F2, F13
**Figures:** none
**Length:** ~10 lines

---

## Acknowledgments + Disclosure

> **Disclosure.** This work was conducted by Sébastien Conejo, co-founder of
> Manifest (https://github.com/mnfst/manifest), an open-source LLM model
> router. Manifest was not used in this benchmark. The routing savings analysis
> (§4.3) applies to any routing system and is computed from the benchmark data
> using a simple per-task argmin. All code, data, and evaluation prompts are
> publicly available at https://github.com/SebConejo/.

**Length:** ~4 lines

---

## Appendix (4–6 pages)

### Appendix A: Full Pareto Frontiers (21 tasks)

One dual-panel Pareto figure per task, following PARETO_STYLE_GUIDE.md.
21 figures, each 1/4 page. ~5.5 pages total.

### Appendix B: Complete Model Table

Table with all 46 models: provider, model name, price tier, input price/M,
output price/M, avg score, rank, number of valid cases.

### Appendix C: Judge Validation Details

- V1 vs V2 scatter plots (GSM8K, RAG QA, HumanEval)
- Score distribution shift V1→V2 per task (small multiples or table)
- Full ranking flip table per task (flip rate and Kendall tau)
  - Most stable: code_review_v2 (20.2% flips, tau=0.596)
  - Least stable: rag_qa (50.3% flips, tau=−0.006)

### Appendix D: Judge Prompts

Full text of V1 and V2 judge prompts for all 17 LLM-judged tasks.

### Appendix E: Statistical Tables

- Bootstrap 95% CI per (task, tier) — full matrix
- Mann-Whitney U p-values per task (Economy vs Premium, Economy vs Standard)
- Coverage matrix: per-model threshold coverage (≥4.0, ≥4.5, ≥4.7)
- Routing savings per task (cheapest model, cost, savings %)

### Appendix F: Top-5 Models Per Task

Table: for each of the 21 tasks, top-5 models ranked by quality (ties broken
by lowest cost). Shows that different tasks have different winners.

### Appendix G: Model Diversity Analysis

- Provider origin comparison (Chinese/American/European): Kruskal-Wallis
  H=1.83, p=0.40. Full table with per-origin means and CIs.
- License comparison (open-weight vs closed): Mann-Whitney p=0.0004, gap 0.183.
  Breakdown showing sub-3B models drive the gap. Excluding sub-3B: gap ~0.066.

### Appendix H: Task Discriminativeness Bar Chart

Horizontal bar chart showing score spread (max − min) per task across all 46
models, color-coded by task category. Companion to §4.1 text.

---

## Figures Summary

| # | Figure | Section | Type |
|---|--------|---------|------|
| 1 | Heatmap (46×21) | §4.1 | Full-width |
| 2 | Tier comparison with CIs | §4.2 | Half-width |
| 3 | Pareto: RAG QA (dual-panel) | §4.3 | Full-width |
| 4 | Pareto: Data-to-Text (dual-panel) | §4.3 | Full-width |
| 5 | Provider gradient scatter | §4.4 | Full-width |

5 figures in the main paper. Task discriminativeness bar chart moved to
Appendix H. 21 Pareto figures + scatter plots in appendix.

---

## Findings → Section Mapping

| Finding | Section | Role |
|---------|---------|------|
| F1 (Economy ≈ Premium) | §4.2, Abstract, §1.3 | Headline finding |
| F2 (Routing saves 99.7%) | §4.3, Abstract | Practical implication |
| F3 (Task discriminativeness) | §4.1 | Landscape description |
| F4 (Provider gradient flat) | §4.4, Abstract | Supporting evidence for F1 |
| F5 (Sub-3B floor) | §4.4 (Mistral paragraph) | Observation |
| F6 (RAQ QA / test gen most discriminative) | §4.1 | Landscape |
| F7 (Origin doesn't predict quality) | §6 Limitations + Appendix G | Observation, null result |
| F8 (Closed > open, marginal) | §6 Limitations + Appendix G | Observation, sub-3B driven |
| F9 (5 models cover all at ≥4.5) | §4.5, §1.3 | Coverage result |
| F10 (Generational delta) | §4.5 | Cross-gen analysis |
| F11 (RAG QA biggest gen leap) | §4.5 | Detail within F10 |
| F12 (Premium better on language, worse on code) | Dropped | Marginal deltas in noise, not defensible at n=2 |
| F13 (Judge format bias) | §3.4, §5.2, Abstract | Methodology contribution |
| F14 (34.7% ranking flips) | §3.4 | Supports F13 |
| F15 (Verbosity ≠ primary bias) | §5.2 | Nuance on F13 |
| F16 (Qwen Turbo cheapest at 4.0) | §4.5 | Coverage detail |
| F17 (GPT-5.4 Nano cheapest at 4.5) | §4.5 | Coverage detail |

**F12 is dropped** from the main paper. The Premium-better-on-language finding
has marginal deltas (<0.2) within noise at n=2 Premium. Including it would invite
attacks on the most vulnerable part of our data. It can be mentioned in one
sentence in §5.1 as a nuance ("Premium models may add marginal value on
open-ended language tasks, but the effect is within our CI").
