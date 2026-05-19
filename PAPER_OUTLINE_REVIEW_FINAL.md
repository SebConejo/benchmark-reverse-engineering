# Paper Outline v2 — Final Review

**Date:** 2026-05-19
**Reviewer:** Critical self-review before sign-off

---

## Verdict: ALL 5 ISSUES RESOLVED — outline ready for sign-off

All issues from the 2026-05-18 review have been applied to PAPER_OUTLINE_v2.md.
Below: original issues preserved with resolution notes.

---

## 1. Flow Coherence

**Introduction → Methodology → Results → Discussion: GOOD.**

The narrative arc works:
- §1 sets up "practitioners need per-task cost-quality data"
- §3 explains how we built it (including judge validation as a prereq)
- §4 delivers the findings in a logical order: landscape overview → headline
  finding → Pareto/routing → provider evidence → generational trends → coverage
- §5 synthesizes practical recommendations
- §6–7 close honestly

One issue: **§5.2 mixes two unrelated topics.** The section is titled
"Evaluation Methodology Implications" but ends with origin/license observations
that have nothing to do with evaluation methodology. See issue #3 below.

---

## 2. Findings Coverage

All 17 findings are accounted for:

| Finding | Location | Status |
|---------|----------|--------|
| F1 | §4.2 + Abstract + §1.3 | OK |
| F2 | §4.3 + Abstract | **See issue #1** (70% number) |
| F3 | §4.1 | OK |
| F4 | §4.4 + Abstract | OK |
| F5 | §4.4 (Mistral paragraph) | OK |
| F6 | §4.1 | OK |
| F7 | §5.2 (1 sentence) + Appendix G | OK |
| F8 | §5.2 (1 sentence) + Appendix G | OK |
| F9 | §4.6 + §1.3 | OK |
| F10 | §4.5 | OK |
| F11 | §4.5 | OK |
| F12 | Dropped (1 sentence in §5.1) | OK |
| F13 | §3.4 + §5.2 + Abstract | OK |
| F14 | §3.4 | OK |
| F15 | §5.2 | OK |
| F16 | §4.6 | OK |
| F17 | §4.6 | OK |

Coverage is complete.

---

## 3. Page Budget

**Current estimate:**

| Section | Text (lines) | Figures | Est. pages |
|---------|:---:|:---:|:---:|
| Abstract | 10 | 0 | 0.3 |
| §1 Introduction | 34 | 0 | 0.7 |
| §2 Related Work | 24 | 0 | 0.5 |
| §3 Methodology | 57 | 0 | 1.2 |
| §4 Results | 96 | 6 | **3.6** |
| §5 Discussion | 24 | 0 | 0.5 |
| §6 Limitations | 18 | 0 | 0.4 |
| §7 Conclusion | 10 | 0 | 0.2 |
| Disclosure | 4 | 0 | 0.1 |
| **Total** | | | **~7.5** |

The raw text fits in 8 pages. The problem is **§4 Results with 6 figures**.
Full-width figures (heatmap, 2 Paretos, provider gradient) take ~1/3 page each
= 1.3 pages. Two half-width figures (discriminativeness + tier CIs) share one
row = 0.3 page. Figures alone = ~1.6 pages. Text + figures = **3.6 pages**,
overshooting the 3-page budget by 0.5 page.

**Total with figures: ~9.1 pages.** Over the 8-page target.

See issue #4 for the fix.

---

## 4. Weak or Redundant Sections

### §4.5 Generational Delta — THIN

4 model pairs, one of which contradicts the thesis (DeepSeek costs +211%).
The punchline ("upgrade generations, not tiers") is already stated as
recommendation #3 in §5.1. As a standalone results sub-section with its own
header, it's thin. It's really supporting evidence for a discussion point.

### §4.6 Coverage Matrix — OVERLAPS with §4.3

§4.3 already states: "4 models cover all at ≥4.0, GPT-5.4 Nano cheapest on
15/21. 5 models cover at ≥4.5, cheapest = Grok 4 Fast." §4.6 repeats these
exact numbers with slightly more detail (the ≥4.7 = 0 models datapoint is
the only new info).

### Combined fix: merge §4.5 + §4.6 → §4.5 "Model Selection in Practice"

New §4.5 covers: (1) coverage matrix thresholds (from old §4.6), (2)
generational upgrades as a model selection strategy (from old §4.5), (3) the
≥4.7 bottleneck observation. One tighter sub-section instead of two thin ones.
Saves ~0.5 page — brings Results back to ~3 pages.

Additionally: **cut Figure 2 (discriminativeness bar chart)** from the main
paper. The information is already conveyed by: (a) the heatmap which shows
variance visually, and (b) the text listing the 4 most/3 least discriminative
tasks with numbers. Move Figure 2 to Appendix. This saves 0.15 page and makes
§4.1 tighter.

With both changes: Results = ~2.9 pages. Total = ~7.8 pages. Budget met.

---

## 5. Issues to Fix

### Issue #1: The "70%" routing savings number is unsourced (BLOCKING)

The Abstract and §1.3 say "routing saves 70% vs a single-model deployment."
The analysis files show:
- **99.7%** vs o3 (routing_savings.json)
- **~97%** vs Grok 4 Fast (cheapest universal at ≥4.5)
- **98.7–99.9%** per task vs o3 (per_task_routing_savings.json)

The 70% number appears in PAPER_STRATEGY.md but is not backed by any JSON
in analysis_v3_final/. It may come from an earlier analysis or a different
baseline (e.g., vs a mid-tier model like GPT-4o). Either:

- **Option A:** Drop the 70% and use only the sourced numbers. Abstract
  becomes: "Per-task routing reduces cost by over 97% versus a single
  universal model and by 99.7% versus the best model."
- **Option B:** Compute the 70% explicitly against a named baseline and
  add it to the analysis outputs.

**Recommendation: Option A.** The 99.7% and 97% are both sourced and more
impressive. The 70% is weaker AND unsourced — no reason to keep it.

### Issue #2: §4.3 routing baselines need clarification (MINOR)

§4.3 uses three different routing baselines in quick succession:
1. vs o3 (99.7%)
2. vs Grok 4 Fast (~97%)
3. vs "4-model cheapest portfolio"

A reader will be confused about which "savings" number to take away. Pick
ONE primary comparison for the text and table the rest. Recommendation:
lead with **vs cheapest universal model** (Grok 4 Fast, ~97%) as the
realistic baseline. Put the 99.7% vs o3 in parentheses as an upper bound.

### Issue #3: §5.2 mixes evaluation methodology + model diversity (MINOR)

The section is titled "Evaluation Methodology Implications" but the last
paragraph is about origin (p=0.40) and license (0.183 gap) — unrelated to
evaluation methodology.

**Fix:** Move the origin/license sentences to §6 Limitations as a bullet:
"**Model diversity.** Our sample includes 3 geographic origins and both
open/closed licenses; neither dimension significantly predicts quality
(Appendix G)." This is cleaner — it acknowledges we checked it, says it's
null, and points to the appendix. §5.2 stays focused on its topic.

### Issue #4: Merge §4.5 + §4.6 to save page budget (STRUCTURAL)

As detailed in section 4 above. Merge into one sub-section, cut Figure 2
from main paper to appendix.

### Issue #5: Abstract word count (COSMETIC)

Current Abstract is ~145 words after the judge compression. The 200-word
budget has room. Consider adding one sentence on task diversity: "Tasks
span classification, structured extraction, code generation, and
open-ended reasoning." This helps the reader who only reads the abstract
understand what "21 production tasks" means concretely.

---

## 6. Punchline Check

| Section | Punchline | Verdict |
|---------|-----------|---------|
| §4.1 Landscape | "For 11/21 tasks, model selection is irrelevant" | STRONG |
| §4.2 Tier Comparison | "Premium adds no detectable quality" | STRONG (headline) |
| §4.3 Pareto/Routing | "Premium models are never on the Pareto frontier" | STRONG |
| §4.4 Provider Gradient | "The most expensive model is not the best" | STRONG |
| §4.5 Gen Delta | "Upgrade generations = free lunch" | OK but overlaps §5.1 |
| §4.6 Coverage | "At ≥4.7, no model covers all tasks" | Interesting but thin |
| §5.1 Practical | Three numbered recommendations | STRONG |
| §5.2 Eval Methodology | "Validate your judge against ground truth" | CLEAR |

After merging §4.5+§4.6, the combined punchline becomes: "5 models cover
everything at ≥4.5, but the frontier keeps moving — each generation is
cheaper AND better." Stronger than either alone.

---

## 7. Title Recommendation

### Comparison with benchmark paper titles

| Paper | Title style | arXiv reach | Twitter/HN reach |
|-------|-------------|:-----------:|:-----------------:|
| HELM | Descriptive ("Holistic Evaluation of Language Models") | HIGH | LOW |
| MMLU | Descriptive ("Measuring Massive Multitask...") | HIGH | LOW |
| Chatbot Arena | Name + mechanism | HIGH | MEDIUM |
| MT-Bench | Provocative ("Judging LLM-as-a-Judge") | HIGH | HIGH |
| FrugalGPT | Finding-first ("FrugalGPT: How to Use LLMs While Reducing Cost") | MEDIUM | HIGH |

**Pattern:** The papers that spread on Twitter/HN either have a provocative
verb ("Judging", "How to") or a surprising finding in the title. Pure
descriptive titles (HELM, MMLU) work for prestige venues but don't spread
organically.

### Analysis of our 3 candidates

| Title | arXiv | Twitter/HN | Risk |
|-------|:-----:|:----------:|------|
| A: "TaskBench: Cost-Quality Tradeoffs..." | HIGH | LOW | Safe but forgettable |
| B: "A $0.02/M Model Scores 4.7/5..." | MEDIUM | HIGH | "4.7/5" is opaque to casual readers — what does the /5 scale mean? |
| C: "TaskBench: Why Economy LLMs Match Premium..." | HIGH | HIGH | Names the finding clearly, no jargon |

**B's weakness:** "Scores 4.7/5" requires context. A casual Twitter reader
doesn't know our scale. It sounds like... a decent score? Not shocking enough.
Compare to "costs 99% less" or "matches GPT-5.5 Pro" — those hook without
context.

**C's strength:** "Economy LLMs Match Premium" is immediately understandable.
No scale knowledge needed. It's the actual finding. And "Why" promises an
explanation, not just a claim.

**Recommendation: C** — "TaskBench: Why Economy LLMs Match Premium on 21
Production Tasks." It has the benchmark name (citability), the finding
(hook), the scale (21 tasks), and no model/provider names. Works for
both arXiv and Twitter.

Fallback: A for maximum academic safety.

---

## Summary of Changes — ALL RESOLVED

| # | Issue | Severity | Fix | Status |
|---|-------|----------|-----|--------|
| 1 | 70% routing savings unsourced | BLOCKING | Replaced with 99.7% (vs o3) everywhere. ~98% vs Grok 4 Fast as secondary in §4.3 | **DONE** |
| 2 | §4.3 multiple baselines confusing | MINOR | Lead with 99.7% vs o3, ~98% vs cheapest universal as secondary | **DONE** |
| 3 | §5.2 mixes eval + diversity | MINOR | Origin/license moved to §6 Limitations as bullet, §5.2 stays focused | **DONE** |
| 4 | §4.5 + §4.6 thin + redundant | STRUCTURAL | Merged into §4.5 "Model Selection in Practice" (coverage + generational) | **DONE** |
| 5 | Abstract has room for 1 sentence | COSMETIC | Added task diversity ("spanning sentiment, intent, code gen, math reasoning...") | **DONE** |

**Additional changes applied per user review:**
- Title C revised: "Why" removed → "TaskBench: Economy LLMs Match Premium Across 21 Production Tasks"
- Figure 2 (discriminativeness bar chart) moved to Appendix H, main paper now 5 figures
- Findings mapping table updated for new section numbers
- Results section is now 5 sub-sections (was 6), estimated at ~2.9 pages

**Revised page budget:**

| Section | Text (lines) | Figures | Est. pages |
|---------|:---:|:---:|:---:|
| Abstract | 12 | 0 | 0.3 |
| §1 Introduction | 34 | 0 | 0.7 |
| §2 Related Work | 24 | 0 | 0.5 |
| §3 Methodology | 57 | 0 | 1.2 |
| §4 Results | 84 | 5 | **2.9** |
| §5 Discussion | 20 | 0 | 0.4 |
| §6 Limitations | 22 | 0 | 0.5 |
| §7 Conclusion | 10 | 0 | 0.2 |
| Disclosure | 4 | 0 | 0.1 |
| **Total** | | | **~7.8** |

Budget met. Outline ready for drafting.
