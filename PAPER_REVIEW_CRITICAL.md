# Critical Review of TaskBench Paper Draft

**Date:** 2026-05-22
**Perspective:** Hostile arXiv reviewer. No charity given.

---

## P1-P5 from PAPER_SELF_REVIEW.md (with recommendations)

**P1: Economy tier boundary in Abstract.**
Abstract says "$0.05-$0.50/M". Table says Economy $0.05-$0.49, Standard starts at $0.50.
**Reco:** Change Abstract to "$0.05-$0.49/M" for consistency with the table. Minor but sloppy if left.

**P2: Rejudge cost "approximately $54".**
JUDGE_PROMPTS_V2.md estimates ~$62. The paper says ~$54.
**Reco:** Change to "approximately $60" to be safe. Cannot verify exact spend without billing data.

**P3: Figure format conversion.**
SVGs need PDF conversion for pdflatex.
**Reco:** Run `inkscape --export-type=pdf` on 3 SVG files before submission. Mechanical step, not blocking review.

**P4: Bibliography completeness.**
Two corrections needed (see Section 5 below). Berkeley Function Calling Leaderboard needs a citation or must drop "Leaderboard" phrasing.
**Reco:** Fix the two bib entries and either cite or rephrase the Berkeley reference.

**P5: Appendix tables.**
Appendices B, E, F are placeholders pointing to JSON files.
**Reco:** Acceptable for arXiv if the companion repo is live. Add a note: "All supplementary tables are available in machine-readable format in the companion repository."

---

## Critical Review

### Issue 1: Tier counts are WRONG (BLOCKING)

The paper (§3.2, line 199-208) states:

| Tier | n |
|------|---|
| Premium | 2 |
| Standard | 22 |
| Economy | 13 |
| Micro | 9 |

I computed the actual counts from the CSV for the 46 complete models using the paper's stated boundaries ($5.00 / $0.50 / $0.05):

| Tier | Actual n |
|------|----------|
| Premium | 2 |
| Standard | 18 |
| Economy | 23 |
| Micro | 3 |

The discrepancy is large: Standard is 18 not 22, Economy is 23 not 13, Micro is 3 not 9. The root cause: the CSV records query-time prices, while the analysis (stats_validation.json, provider_gradient.json) used corrected provider-published prices. For example, GPT-5.4 Nano is $0.10/M in the CSV but $0.02/M in the analysis; Qwen Turbo is $0.033/M in the CSV but $0.05/M in the analysis.

Additionally, the STATS_VALIDATION.md reveals the analysis used different boundaries: "$5 / $0.50 / $0.08" (Economy starts at $0.08, not $0.05). The n pairs in stats_validation.json (42/451/313/210) suggest approximately 2/21/15/10 models, matching the PAPER_OUTLINE's "n=2/22/15/9" more closely but still not exactly.

The paper states boundaries of $0.05 but the actual analysis used $0.08. The n counts of 22/13/9 match neither the $0.05 boundary computation nor the $0.08 one.

**Fix required:** Either (a) rerun the analysis with $0.05 boundaries and update all tier numbers, or (b) change the paper's boundaries to match the analysis ($0.08) and use the correct n counts. Option (b) is safer since it preserves the validated CIs and p-values in stats_validation.json.

The tier means and CIs (4.791/4.787/4.749/4.519) come from the analysis and are internally consistent with whatever boundaries the analysis used. The FINDINGS are not wrong, but the stated tier definitions and model counts are inconsistent with the analysis.

### Issue 2: "Matching its quality on every task" is overclaimed (MODERATE)

The Abstract (line 56-57) says routing "reduces cost by 99.7% versus the best single model while matching its quality on every task."

The actual data: the routed portfolio uses the cheapest model scoring >= 4.0 per task. These models score 4.50-5.00 per task, while o3 scores 4.60-5.00. The average gap is 0.024 points (small), but the max gap is 0.20 (moderation_toxigen: routed model 4.50 vs o3 4.70). On 10 of 21 tasks, the routed model scores lower than o3.

"Matching its quality" means zero quality loss. The actual gap is small (within CI) but nonzero on 10 tasks. The honest phrasing is "while maintaining comparable quality" or "with at most 0.2 points quality difference."

**Fix required:** Change "matching its quality on every task" to "while maintaining quality above 4.5 on every task" or "with negligible quality loss (average gap 0.02 points)." This applies to:
- Abstract line 56-57
- §1.3 line 115 ("while matching o3 quality on every task")
- §4.3 is already fine (it quotes the cost numbers without the "matching" claim)

### Issue 3: §3.4 Judge Validation may take too much space relative to scope (MINOR)

§3.4 is the longest methodology sub-section (~35 lines). It covers V1 failures, V2 fixes, three validation tasks, the harness fix, ranking flips, and 14 unvalidated tasks. The paper's scope is "benchmark cost-quality" not "judge methodology."

This is borderline. The validation is necessary to justify the scoring, and 35 lines is not excessive. But the harness fix detail (four extraction strategies, 91.4% formatting failures) is implementation detail that could move to Appendix C. The code_generation paragraph reads like a standalone methods contribution.

**Reco:** Cut the harness detail from §3.4 to two sentences: "Judge scores versus pass@1 execution rate. V2: $r = 0.891$." Move the multi-strategy harness description to Appendix C. Saves ~5 lines.

### Issue 4: Missing n=2 caveat in three locations (MODERATE)

The n=2 caveat appears in §4.2 and §6 but is missing from:

1. **Abstract** (line 51-53): "Economy-tier models show no statistically significant quality gap versus Premium models on any of the 21 tasks." This is a strong claim without the caveat. A reader who only reads the Abstract will not know n=2.

2. **§1.3** (line 106-108): "No Economy-Premium gap detected. Mann-Whitney p>0.05 on 21 of 21 tasks." Again no caveat.

3. **§7 Conclusion** (line 568-571): "Economy models are statistically indistinguishable from Premium on every task tested." Strongest version of the claim, no caveat.

A hostile reviewer will say: "Your headline claim is in the Abstract and Conclusion without the n=2 qualification. This reads as a proven fact when it's really a low-power null result."

**Fix required:** Add parenthetical in the Abstract: "(Mann-Whitney $p > 0.05$, 21/21; $n_{\text{Premium}} = 2$)". Add "with the caveat that n=2 Premium models limits detection power" to the Conclusion.

### Issue 5: Two bibliography entries need correction (MODERATE)

**saito2023verbosity:** Title is wrong. Actual title: "Verbosity Bias in Preference Labeling by Large Language Models" (arXiv:2310.10076). The paper cites "Verbosity Bias in LLM-as-a-Judge" which is a fabricated title.

**lu2024routerarena:** Year is wrong. Paper was submitted September 2025, not 2024. Cite key should be lu2025routerarena. The arXiv ID 2510.00202 is correct.

**Fix required:** Correct both entries in references.bib.

### Issue 6: Transition from §4.4 to §4.5 is abrupt (MINOR)

§4.4 ends with the provider gradient observation. §4.5 switches to coverage thresholds and generational upgrades without connecting to the previous section. A one-sentence bridge would help: "Having established that within-provider price increases yield minimal returns, we examine which models a practitioner should actually choose."

### Issue 7: "The first benchmark" claim (MINOR)

§1.2 (line 86) and §7 (line 567) both claim "the first benchmark measuring per-task cost-quality Pareto frontiers." This is hard to verify. Artificial Analysis, CEBench, and FrugalGPT all touch cost-quality in some form. The claim should be narrower: "the first public benchmark providing per-task cost-quality Pareto frontiers across this many models and tasks."

**Reco:** Add "public" and qualify the scope. A reviewer will challenge "first" claims.

### Issue 8: No system prompt mentioned (MINOR)

§3.1 says "Each case has a fixed prompt" and §3.3 mentions GPT-4o as judge. But the paper never explicitly states whether a system prompt was used. The runner uses no system prompt (user-turn only). This should be stated, since system prompts can affect model behavior and a reader trying to reproduce needs this information.

**Reco:** Add one sentence in §3.1: "All prompts are single-turn user messages with no system prompt."

### Issue 9: Provider count inconsistency (MINOR)

§3.2 line 213-214 lists providers: "OpenAI (10), Qwen (7), Mistral (5), Anthropic (4), Google (3), ByteDance (3), xAI (3), Meta/Llama (3), and others." That's 8 named providers + "others" = at least 9. But the actual provider count depends on whether Microsoft, MiniMax, DeepSeek, Nvidia, and Kimi are separate providers or grouped under "others."

The 46 models come from: OpenAI, Anthropic, Google, Mistral, Qwen, ByteDance, xAI, Meta, Microsoft, MiniMax, DeepSeek, Kimi, Nvidia, Seed (ByteDance sub-brand). That's more than 9.

**Reco:** Count the actual distinct providers and update the "9 providers" claim throughout the paper, or define what counts as a "provider" (e.g., by API endpoint).

---

## Style Check

### IA word scan

| Banned word | Occurrences |
|-------------|:-----------:|
| delve | 0 |
| crucial | 0 |
| robust (as empty intensifier) | 0 |
| nuanced | 0 |
| moreover | 0 |
| furthermore | 0 |
| additionally | 0 |
| groundbreaking | 0 |
| comprehensive | 0 |
| leverage | 0 |

**PASS.** No banned words found.

### List-of-three check

- §1.2: Three contributions. Acceptable (this is a contributions list, not a rhythmic triplet).
- §2: Three subsections. Acceptable (topical).
- §5.1: Three recommendations. Acceptable (explicit numbered list).
- §5.2: Three practices recommended. This one borders on rhythmic triplet. Consider whether two would suffice or rephrasing as prose.

**PASS with note.** The threes are all functional (numbered lists), not stylistic.

### Em-dash check

Zero em-dashes in prose. All `--` are LaTeX en-dashes for numeric ranges. **PASS.**

### Narrative flow

Abstract → §1 (problem, contributions, preview) → §2 (related work) → §3 (method) → §4 (results) → §5 (discussion) → §6 (limitations) → §7 (conclusion).

The flow is standard and clean. One issue: **§1.3 Key Findings Preview** gives away all results before the methodology is presented. This is standard in benchmark papers (HELM does it, MMLU does it) but a purist reviewer may want to see methods first. Given that all 6 reverse-engineered papers place findings in or near the abstract, this is fine.

Transition quality:
- §1 → §2: implicit (standard). OK.
- §2 → §3: implicit. OK.
- §3 → §4: implicit. OK.
- §4.4 → §4.5: abrupt (see Issue 6).
- §4 → §5: implicit. OK.
- §5 → §6: implicit. OK.
- §6 → §7: implicit. OK.

### Overclaim scan

| Claim | Location | Verdict |
|-------|----------|---------|
| "No quality gap" | Abstract, §1.3 | OVERCLAIM without n=2 caveat (Issue 4) |
| "matching its quality" | Abstract, §1.3 | OVERCLAIM (Issue 2) |
| "the first benchmark" | §1.2, §7 | Needs qualifier (Issue 7) |
| "statistically indistinguishable" | §7 | OVERCLAIM without n=2 caveat (Issue 4) |
| "any routing system can consume" | §2.2 | OK (trivially true) |
| "near-zero return" | §5.1 | OK (supported by gradient data) |

---

## Summary: Issues by severity

### BLOCKING (fix before submission)

| # | Issue | Fix |
|---|-------|-----|
| 1 | Tier counts wrong (22/13/9 vs actual) | Verify analysis boundaries, update table |
| 2 | "Matching quality" overclaim | Rephrase in Abstract, §1.3 |
| 4 | n=2 caveat missing in Abstract + Conclusion | Add parenthetical |
| 5 | Two bib entries incorrect | Fix title + year |

### MODERATE (should fix)

| # | Issue | Fix |
|---|-------|-----|
| 7 | "First benchmark" unqualified | Add "public" + scope qualifier |
| 9 | Provider count may be wrong | Verify and update |

### MINOR (nice to fix)

| # | Issue | Fix |
|---|-------|-----|
| 3 | §3.4 harness detail too long | Move to appendix |
| 6 | §4.4→§4.5 transition abrupt | Add one bridge sentence |
| 8 | No system prompt stated | Add one sentence in §3.1 |
| P1 | Abstract $0.50 vs table $0.49 | Align |
| P2 | Rejudge cost $54 vs $62 | Change to ~$60 |
