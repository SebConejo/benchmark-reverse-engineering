# Final Coherence Review

**Date:** 2026-05-23
**Method:** Automated cross-check of every number in main.tex against
freshly regenerated analysis_v3_final/ JSONs. Manual scan for stale
values from previous iterations.

---

## 1. Number Cross-Check (64 checks)

| Metric | Paper | Source | Source file | Status |
|--------|-------|--------|-------------|--------|
| Premium mean | 4.791 | 4.791 | stats_validation | OK |
| Premium CI | [4.729, 4.853] | [4.729, 4.853] | stats_validation | OK |
| Premium n pairs | 42 | 42 | stats_validation | OK |
| Standard mean | 4.783 | 4.783 | stats_validation | OK |
| Standard CI | [4.760, 4.805] | [4.76, 4.805] | stats_validation | OK (trailing zero) |
| Standard n pairs | 399 | 399 | stats_validation | OK |
| Economy mean | 4.741 | 4.741 | stats_validation | OK |
| Economy CI | [4.710, 4.768] | [4.71, 4.768] | stats_validation | OK (trailing zero) |
| Economy n pairs | 441 | 441 | stats_validation | OK |
| Micro mean | 4.287 | 4.287 | stats_validation | OK |
| Micro CI | [4.128, 4.449] | [4.128, 4.449] | stats_validation | OK |
| Micro n pairs | 84 | 84 | stats_validation | OK |
| Premium models | 2 | 42/21 = 2 | computed | OK |
| Standard models | 19 | 399/21 = 19 | computed | OK |
| Economy models | 21 | 441/21 = 21 | computed | OK |
| Micro models | 4 | 84/21 = 4 | computed | OK |
| Total models | 46 | 2+19+21+4 = 46 | computed | OK |
| Prem-Econ gap | 0.050 | 4.791-4.741 = 0.050 | computed | OK |
| Micro gap vs Prem | -0.50 | 4.287-4.791 = -0.504 | computed | OK (rounded) |
| CI bound | 0.14 | 4.853-4.710 = 0.143 | computed | OK (rounded) |
| MW tasks tested | 21 | 21 | stats_validation | OK |
| MW significant | 2 | 2 | stats_validation | OK |
| MW multistep p | 0.029 | 0.0286 | stats_validation | OK (rounded) |
| MW instruction p | 0.043 | 0.0427 | stats_validation | OK (rounded) |
| Intent spread | 3.20 | 3.2 | task_discriminativeness | OK |
| Intent sigma | 0.624 | 0.624 | task_discriminativeness | OK |
| RAG spread | 2.84 | 2.84 | task_discriminativeness | OK |
| RAG sigma | 0.560 | 0.56 | task_discriminativeness | OK |
| Mod spread | 2.40 | 2.4 | task_discriminativeness | OK |
| TestGen spread | 2.40 | 2.4 | task_discriminativeness | OK |
| StructOut spread | 0.29 | 0.293 | task_discriminativeness | OK (rounded) |
| Multistep spread | 0.80 | 0.8 | task_discriminativeness | OK |
| Best model | o3 | o3 | routing_savings | OK |
| Best score | 4.842 | 4.842 | routing_savings | OK |
| Best cost | $0.003332 | 0.003332 | routing_savings | OK |
| Routed cost | $0.000009 | 9e-06 | routing_savings | OK |
| Savings % | 99.7 | 99.7 | routing_savings | OK |
| Cover 4.0 | 37 | 37 | coverage_matrix | OK |
| Cover 4.5 | 5 | 5 | coverage_matrix | OK |
| Cover 4.7 | 0 | 0 | coverage_matrix | OK |
| Haiku score | 4.775 | 4.775 | provider_gradient | OK |
| Opus score | 4.753 | 4.753 | provider_gradient | OK |
| Flash score | 4.749 | 4.749 | provider_gradient | OK |
| Pro score | 4.747 | 4.747 | provider_gradient | OK |
| Nano score | 4.694 | 4.694 | provider_gradient | OK |
| GPT55Pro score | 4.828 | 4.828 | provider_gradient | OK |
| Turbo score | 4.654 | 4.654 | provider_gradient | OK |
| Max score | 4.746 | 4.746 | provider_gradient | OK |
| Ministral score | 4.441 | 4.441 | provider_gradient | OK |
| MistralLrg score | 4.800 | 4.8 | provider_gradient | OK |
| GPT4o->5.4 price% | -60 | -60 | generational_delta | OK |
| GPT4o->5.4 quality | +0.089 | 0.089 | generational_delta | OK |
| Origin KW H | 1.83 | 1.83 | origin_comparison | OK |
| Origin KW p | 0.40 | 0.4002 | origin_comparison | OK (rounded) |
| License gap | 0.183 | 0.183 | license_comparison | OK |
| License p | 0.0004 | 0.0004 | license_comparison | OK |
| Flip rate | 34.7% | 34.7 | ranking_flips | OK |
| Flips count | 5,195 | 5195 | ranking_flips | OK |
| Total pairs | 14,972 | 14972 | ranking_flips | OK |
| Verbosity r | 0.22 | 0.2174 | verbosity_correlation | OK (rounded) |
| Verbosity p | 0.13 | 0.133 | verbosity_correlation | OK (rounded) |
| Providers | 12 | 12 | manual count | OK |
| Total cases | 51,580 | CSV row count | benchmark_results.csv | OK |
| Raw files | 51,705 | file count | results/raw/ | OK |

**Result: 64 checks, 0 real errors.** All "errors" from the automated
script were trailing-zero formatting differences (4.76 vs 4.760), not
value mismatches.

---

## 2. Stale Value Scan

Searched for all known old values in main.tex (excluding comments):

| Old value | Description | Found? |
|-----------|-------------|:------:|
| 4.519 | Old Micro mean | No |
| 4.787 | Old Standard mean | No |
| 4.749 (as tier mean) | Old Economy mean | No (4.749 exists as Flash model score, correct) |
| 0.042 | Old Prem-Econ gap | No |
| 21/21 | Old MW claim | No |
| 21 of 21 | Old MW claim | No |
| on any task | Old "no gap on any task" | No |
| any of the 21 | Old "any of 21 tasks" | No |
| every task tested | Old conclusion | No |
| 9 API | Old provider count | No |
| 9 providers | Old provider count | No |
| n=22 | Old Standard count | No |
| n=13 | Old Economy count | No |
| n=9 | Old Micro count | No |
| 0.27 | Old Micro gap | No |

**Result: 0 stale values found.**

---

## 3. Claim Consistency

The "19/21" claim appears in exactly 5 locations:

| Location | Text | Consistent? |
|----------|------|:-----------:|
| Abstract (L53) | "19 of 21 tasks" | OK |
| §1.2 (L90) | "19 of 21 tasks" | OK |
| §1.3 (L107) | "19 of 21 tasks" | OK |
| §4.2 (L338) | "19 of 21 individual tasks" | OK |
| §5.1 (L478) | "19 of 21 tasks" | OK |
| §7 (L574) | "19 of 21 tasks" | OK |

The n=2 caveat appears in:

| Location | Present? |
|----------|:--------:|
| Abstract (L54) | Yes ($n_{\text{Premium}} = 2$) |
| §4.2 caveat box (L348) | Yes ("$n = 2$ Premium models") |
| §6 Limitations (L519) | Yes ("$n = 2$ Premium models") |
| §7 Conclusion (L575) | Yes ($n_{\text{Premium}} = 2$) |

**All consistent.**

---

## 4. Derived Values

| Derived value | Formula | Paper says | Computed | OK? |
|--------------|---------|-----------|----------|:---:|
| Prem-Econ gap | 4.791 - 4.741 | 0.050 | 0.050 | OK |
| Gap as % of scale | 0.050/5 | 1.0% | 1.0% | OK |
| Micro gap | 4.287 - 4.791 | -0.50 | -0.504 | OK |
| CI bound | 4.853 - 4.710 | 0.14 | 0.143 | OK |
| Haiku/Opus ratio | 15/0.80 | 19x | 18.75x | OK |
| Flash/Pro ratio | 1.25/0.15 | 8x | 8.33x | OK |
| Nano/GPT55Pro ratio | 15/0.02 | 750x | 750x | OK |
| OpenAI quality delta | 4.828-4.694 | +0.134 | 0.134 | OK |
| Qwen quality delta | 4.746-4.654 | +0.092 | 0.092 | OK |
| Mistral quality delta | 4.800-4.441 | +0.359 | 0.359 | OK |

**All derived values correct.**

---

## 5. Verdict

**PASS. The paper is internally coherent.**

- 64 numbers verified against fresh JSONs: 0 real mismatches.
- 0 stale values from previous iterations.
- "19/21" claim consistent across all 6 locations.
- n=2 caveat present in all 4 required locations.
- All derived values (ratios, gaps, percentages) recompute correctly.
- Tier counts (2/19/21/4) match bootstrap n pairs (42/399/441/84) at 21 tasks each.
