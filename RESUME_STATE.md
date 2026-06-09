# Project Resume State

**Read this file FIRST at the start of every new session on this project.**
**This is the canonical state of the TaskBench paper as of 2026-06-02.**
**If the work has moved past what's described here, update this file at the end of the session.**

---

## What this project is

TaskBench: a benchmark paper comparing 46 LLMs across 21 production tasks on cost vs quality. The paper is in `paper/main.tex`, the data and analysis are in `results/analysis_v3_final/` and `scripts/analyze_v3.py`. The repo is `github.com/SebConejo/benchmark-reverse-engineering`, the working clone is `/tmp/benchmark-fresh`.

The paper title is: **"TaskBench: Measuring Cost-Quality Tradeoffs Across 46 LLMs and 21 Production Tasks"**

## Working with Sébastien

- All answers and prompts to Sébastien are in French. Code, file content, and commit messages are in English.
- Sébastien is co-founder and CTO of Manifest. He is technical. He pastes Claude Code outputs into a separate Claude session that coaches him on the next prompt to send. That coaching Claude does NOT do the work directly.
- Sébastien wants you to challenge your first diagnosis. Almost every time his first instinct ("are you sure?") has revealed a real error. Do not be eager to please. If you check and the data is fine, say so plainly. A clean verdict is a valid verdict.
- No em-dashes anywhere. Ever. Use commas, parentheses, or two sentences.
- Avoid AI words: delve, crucial, robust, nuanced, moreover, furthermore.
- Short subject-verb sentences (15-30 words).
- When showing a figure, always include a spot-check table (4-6 model values cross-checked against the source JSON).

## State of the paper

- All 7 sections written, coherent, internally consistent (64-number coherence review passed).
- 12-page PDF compiles cleanly. Zero broken refs, zero overfull boxes.
- Latest commit before the session interruption: `3324090c` (single-panel log-scale Paretos).
- Tier counts: Premium 2, Standard 19, Economy 21, Micro 4. Tier boundaries: Premium ≥ \$5/M, Standard \$0.50-4.99/M, Economy \$0.05-0.49/M, Micro < \$0.05/M.
- 12 providers (not 9), 46 complete models (c == 21 tasks).
- Main finding: Mann-Whitney p > 0.05 on 19/21 tasks (Economy vs Premium). The two significant tasks favor opposite tiers. Gap Premium-Economy = 0.050.
- Caveat present throughout: n=2 Premium models, low statistical power, "no difference detected" not "tiers are equal".
- Judge V2 validated on 3 tasks (GSM8K r=0.905, RAG QA r=0.888, HumanEval r=0.891). 14 LLM-judged tasks validated by mechanism consistency only. This is a documented limitation, not a flaw.

## State of the figures (the current open thread)

**Figure 1 (heatmap_v3): VALIDATED by Sébastien.** 46 models, 0 white cells, fontsize 11 in cells, full DISPLAY_NAMES labels, tier color code in caption with $ signs and proper spacing. Do not re-touch this figure.

**Figures 2, 3, 4, 5: NOT YET VALIDATED VISUALLY by Sébastien.**

- Figure 2 (tier_comparison_v3): regenerated from current V3 data. Bars should show Premium 4.791, Standard 4.783, Economy 4.741, Micro 4.287. Needs visual validation by Sébastien.
- Figure 3 (pareto_rag_qa): switched from dual-panel to single-panel log-scale (academic convention: HELM, FrugalGPT, RouterArena). Labels placed via `adjustText`. 5 labeled points: Llama 1B, Qwen Turbo, Seed 2.0 Mini, Sonnet 4.6, GPT-5.5 Pro. Needs visual validation.
- Figure 4 (pareto_data_to_text): same format as figure 3. 4 labeled points: Llama 1B, Qwen Turbo, Llama 3B, GPT-5.5 Pro. Needs visual validation.
- Figure 5 (provider_gradient): HAS KNOWN PROBLEMS, not yet fixed. Caption says "5 providers shown (29 models)" but the paper claims 12 providers. Labels overlap heavily ("Sonnet 4 (05/14)" and "Sonnet 4.6", "GPT-5.4 Mini" and "GPT-4o Mini" and "Gemini 2.5 Flash" all touching, "o3" and "o4-mini" collide, "Mistral Large" "GPT-5.5" "Sonnet 4 (05/14)" superpose). Title is a rhetorical question, not academic style.

## Immediate next step

Show Sébastien the high-resolution PNGs of figures 2, 3, 4 one at a time for visual validation. Use the checklist in `FIGURE_QUALITY_CHECKLIST.md`. For each figure, provide:
- The PNG
- A spot-check table (4-6 model values vs JSON)
- A summary of what changed and what was verified

Once 2, 3, 4 are validated, tackle figure 5's known problems (provider count, overlapping labels, title).

After all 5 figures are validated, recompile the PDF and present it to Sébastien for the final end-to-end read.

## Mandatory files to read at the start of EVERY figure work session

These exist in the repo. Read them. Do not skip.

- `FIGURE_QUALITY_CHECKLIST.md` (root): full checklist to run before showing any figure.
- `PARETO_STYLE_GUIDE.md` (root): single-panel log-scale Pareto spec. Replaced the old dual-panel spec on 2026-06-02.
- `PAPER_OUTLINE_v2.md`: signed paper structure. Do not deviate.
- `WRITING_DECISIONS.md`: log of conservative decisions made during drafting.
- `LEARNINGS.md`: cumulative project lessons.

## What NOT to do (errors we already corrected, must not return)

1. Do not write figure code that includes partial models. Always filter `c == 21` (46 complete models).
2. Do not invent bibliography entries. Verify every citation against the actual paper (saito2023 title was previously fabricated, RouterArena year was wrong).
3. Do not claim "21/21 non-significant". The current finding is "19/21 non-significant, 2 significant in opposite directions, neither survives Bonferroni".
4. Do not claim Economy "matches" Premium. Claim "no significant difference detected" and add n_Premium=2.
5. Do not use dual-panel Paretos. Use single-panel log-scale (per the current style guide).
6. Do not place labels with manual `xytext` offsets on Paretos. Use `adjustText`.
7. Do not generate figures with text touching the grid. Add padding.
8. Do not say "tu as 100% raison" or other validation phrases. Just do the work.
9. Do not propose a prompt to Sébastien mid-discussion. Wait for him to ask. (This is for the coaching Claude only; for Claude Code, it does not apply.)
10. Do not work in the monorepo. The dedicated repo `github.com/SebConejo/benchmark-reverse-engineering` is the only source of truth. The working clone is `/tmp/benchmark-fresh`.

## Key data and paths

- Data CSV: `results/benchmark_results.csv` (51,580 rows, V2 judge scores).
- Analysis JSONs: `results/analysis_v3_final/` (single source of truth, regenerated by `scripts/analyze_v3.py`).
- Figure script: `scripts/generate_figures.py`.
- Figure files: `paper/figures/*.pdf` (for LaTeX) and `paper/figures/*.png` (for visual review).
- Compiled PDF: `paper/main.pdf`.
- Compilation tool: `tectonic` (installed at `/opt/homebrew/bin/tectonic`).
- SVG to PDF conversion: `cairosvg` with `DYLD_LIBRARY_PATH=/opt/homebrew/lib`.

## Reproducibility check

`python3 scripts/analyze_v3.py` should produce 31 JSON files in `results/analysis_v3_final/`. Tier means should be Premium 4.791, Standard 4.783, Economy 4.741, Micro 4.287. If different, the source data or the tier definitions drifted. Stop and investigate before doing anything else.

## End of session housekeeping

At the end of every session that meaningfully changed the project state:
1. Update this `RESUME_STATE.md` to reflect the new state.
2. Commit and push.
3. The next session will read this updated file first.
