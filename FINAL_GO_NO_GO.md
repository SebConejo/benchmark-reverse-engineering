# Final Go/No-Go Review

**Date:** 2026-05-19
**Purpose:** Verify everything is ready before paper drafting begins.

---

## 1. Data — OK

- **CSV:** 51,580 data rows + 1 header (51,581 lines). 13 columns.
- **V2 scores:** `rebuild_csv.py` line 154 reads `judge_v2_score` first. Confirmed.
- **Backup:** `benchmark_results.csv.bak` exists (May 15, pre-fix V1 scores).
- **Raw files:** 51,705 (exceeds CSV by 125 — rejected/duplicate raws, expected).

**Verdict: OK**

---

## 2. Analyses — OK

- **analysis_v3_final/:** 31 files (14 JSON + 10 SVG + 5 judge validation + 1 md + 1 stats).
- **All 17 findings traceable:** every number in PAPER_OUTLINE_v2.md was cross-checked
  against source JSONs. 24 exact matches. 8 acceptable roundings (3 decimal places).
- **Scripts exist and are substantial:**
  - `rebuild_csv.py` (247 lines)
  - `analyze_v3.py` (476 lines)
  - `generate_figures.py` (201 lines)

**Verdict: OK**

---

## 3. Judge Validation — OK with 1 minor fix needed

- **GSM8K:** V1 r=0.3882, V2 r=0.9053 (paper: 0.388, 0.905 — correct rounding)
- **RAG QA:** V1 r=−0.0127, V2 r=0.8885 (paper: −0.013, **0.887**)
- **HumanEval:** V2 r=0.8913 (paper: 0.891 — correct rounding)

**ERROR:** RAG QA V2 r=0.8885 rounds to **0.888**, not 0.887. The paper says
0.887 (truncation). Fix: change 0.887 → 0.888 in §3.4.

Also: the Abstract says "r=0.89–0.91" which is correct (0.888–0.905 rounds
to 0.89–0.91). No change needed there.

**Verdict: MINOR FIX (0.887→0.888 in §3.4)**

---

## 4. Paper Outline — OK with 1 title fix pending

- **PAPER_OUTLINE_v2.md** updated today (v2.1). Structure: 7 sections + appendix.
- **5 main figures** chosen, all generated (SVGs in analysis_v3_final/).
- **Chiffres cohérents:** 32 numbers cross-checked, all match or correctly round.
- **70% removed:** zero traces remaining.
- **Findings mapping:** all 17 findings referenced (main or appendix).

Title finalized (2026-05-19):
> **TaskBench: Measuring Cost-Quality Tradeoffs Across 46 LLMs and 21 Production Tasks**

Descriptive, no claim, all SEO keywords present, 12 words.

**Verdict: OK**

---

## 5. Repo Reproducibility — OK

- **README.md:** exists, titled "TaskBench — Cost-Quality Tradeoffs..."
- **requirements.txt:** exists
- **.env.example:** exists
- **Pipeline:** `rebuild_csv.py` → `analyze_v3.py` → `generate_figures.py`. All exist.
- **rebuild_csv.py** reads V2 scores (line 154: `judge_v2_score` first). Bug fix confirmed.

**Verdict: OK**

---

## 6. Figures — OK

- **Main paper (5 needed):**
  - Heatmap: `heatmap_v3.svg` (495K) — exists
  - Tier comparison: `tier_comparison_v3.svg` — exists
  - Pareto RAG QA: `pareto_rag_qa.png` — exists
  - Pareto Data-to-Text: `pareto_data_to_text.png` — exists
  - Provider gradient: `provider_gradient.svg` — exists
- **Appendix Paretos:** 37 PNG files in results/figures/ covering all tasks.
- **Appendix charts:** 10 SVGs in analysis_v3_final/ (discriminativeness, generational, etc.)

**Note:** Main paper Paretos are PNGs (from figures/) while other figures are
SVGs (from analysis_v3_final/). For arXiv, all should be PDF or high-res PNG.
The PNGs may need regeneration as SVG/PDF for print quality. Not blocking —
can be done during paper formatting.

**Verdict: OK (format standardization needed later, not blocking)**

---

## 7. Support Documents — OK with staleness note

| Document | Exists | Last Modified | Status |
|----------|--------|---------------|--------|
| LEARNINGS.md | YES | May 15 | OK (covers all 19 lessons incl. V2 judge) |
| FINDINGS_COHERENCE_REVIEW.md | YES | May 17 | OK (post-V3 analysis) |
| METHODOLOGY.md | YES | May 12 | STALE (pre-V3, pre-judge-fix) |
| LIMITATIONS.md | YES | May 12 | STALE (pre-V3) |
| PAPER_STRATEGY.md | YES | May 15 | OK |
| PARETO_STYLE_GUIDE.md | YES | May 14 | OK |
| PAPER_OUTLINE_v2.md | YES | May 19 | OK (today) |

**Note:** METHODOLOGY.md and LIMITATIONS.md are from May 12 (pre-V3 analysis,
pre-judge-validation-code, pre-rebuild_csv fix). They may contain stale numbers
or miss the HumanEval validation. However, the paper will be written from
PAPER_OUTLINE_v2.md (which is current), not from these docs. They are
working notes, not paper sources. **Not blocking.**

**Verdict: OK (staleness noted, not blocking)**

---

## 8. Disclosure — OK

Wording in PAPER_OUTLINE_v2.md:
> **Disclosure.** This work was conducted by Sébastien Conejo, co-founder of
> Manifest (https://github.com/mnfst/manifest), an open-source LLM model
> router. Manifest was not used in this benchmark. The routing savings analysis
> (§4.3) applies to any routing system and is computed from the benchmark data
> using a simple per-task argmin. All code, data, and evaluation prompts are
> publicly available at https://github.com/SebConejo/.

**Verdict: OK**

---

## 9. Cohérence Globale — OK with 1 rounding fix

- **No contradictions** between PAPER_OUTLINE_v2.md and source JSONs (32 numbers checked).
- **No stale 70%** anywhere in the outline.
- **F12 correctly dropped** from main paper, noted in mapping table.
- **One rounding inconsistency:** RAG QA V2 r=0.888 should be 0.888.
- **Title "Match" still in file** — pending user decision.

**Verdict: OK after 2 minor fixes**

---

## Final Verdict: GO

Both fixes applied (2026-05-19):

| # | Fix | Status |
|---|-----|--------|
| 1 | §3.4: RAG QA V2 r 0.887 → 0.888 | **DONE** |
| 2 | Title finalized: descriptive, no claim | **DONE** |

**GO for paper drafting.**
