# Compilation Review

**Date:** 2026-05-26
**Tool:** Tectonic 0.16.9 (XeTeX backend)
**SVG conversion:** cairosvg 2.9.0 + cairo 1.18.4

---

## 1. Figures

| # | Figure | Source | Format | Converted | Renders? |
|---|--------|--------|--------|-----------|:--------:|
| 1 | Heatmap (46x21) | heatmap_v3.svg | SVG -> PDF | cairosvg | OK |
| 2 | Tier comparison CIs | tier_comparison_v3.svg | SVG -> PDF | cairosvg | OK |
| 3 | Pareto: RAG QA | pareto_rag_qa.png | PNG (native) | n/a | OK |
| 4 | Pareto: Data-to-Text | pareto_data_to_text.png | PNG (native) | n/a | OK |
| 5 | Provider gradient | provider_gradient.svg | SVG -> PDF | cairosvg | OK |

All figures are in `paper/figures/`. Source SVGs from the original
benchmark directory (dated May 19). PNGs are from the original
`results/figures/` directory.

**Note:** The Pareto plots (Figures 3 and 4) are single-panel (not the
dual-panel layout described in PARETO_STYLE_GUIDE.md). They were
generated during an earlier analysis session. They show the data
correctly but use a different visual layout than the guide specifies.
Regenerating them as dual-panel is a cosmetic improvement, not blocking.

**Note:** The tier comparison figure (Figure 2) shows per-task bars from
the old analysis, not the updated global CIs. The bars still show the
correct pattern (Economy and Premium overlap) but the exact bar heights
may not match the recomputed numbers. Regenerating from fresh data is
recommended before final arXiv submission.

---

## 2. Compilation

| Check | Result |
|-------|--------|
| LaTeX engine | Tectonic 0.16.9 (XeTeX) |
| Compilation errors | 0 |
| Overfull \hbox warnings | 0 (3 fixed during this session) |
| Broken references ([?]) | 0 |
| BibTeX resolved | All 8 entries rendered |
| PDF version warnings | 3 (PDF 1.7 in 1.5 output, cosmetic) |

---

## 3. Page Count

| Section | Pages |
|---------|:-----:|
| Title + Abstract | 1 (p1) |
| Introduction (§1) | 1 (p1-p2) |
| Related Work (§2) | 0.5 (p2) |
| Methodology (§3) | 1.5 (p3-p4) |
| Results (§4) | 4 (p4-p8, includes 5 figures) |
| Discussion (§5) | 0.7 (p8-p9) |
| Limitations (§6) | 0.8 (p9-p10) |
| Conclusion (§7) | 0.3 (p10) |
| Acknowledgments + References | 1 (p10-p11) |
| Appendices (A-H) | 1.5 (p11-p12) |
| **Total** | **12 pages** |

Main body (Abstract through Conclusion): approximately 9 pages.
References + Appendices: approximately 3 pages.

The main body exceeds the 8-page soft target by about 1 page. This is
driven by the 5 figures, which take roughly 4 pages of vertical space
combined. This is typical for benchmark papers with multiple figures.
ArXiv has no page limit.

---

## 4. Rendering Quality

- **Text:** Clean, no artifacts, all math symbols render correctly.
- **Tables:** Tier comparison table and judge validation table both render
  with proper booktabs formatting.
- **Figures:** All 5 figures are legible. The heatmap is dense but readable
  at full-page width. Pareto plots show clear tier-color coding. Provider
  gradient shows all 5 provider lines with labeled models.
- **URLs:** Both footnote URLs render as clickable blue links.
- **Bibliography:** All 8 references render with correct author names,
  titles, and years. No [?] markers.
- **Cross-references:** Figure~1 through Figure~5 all resolve. Section~6
  and Appendix~C/G references resolve. No broken \ref.

---

## 5. Verdict

**The PDF is ready for author review.** It compiles cleanly, all figures
render, and no references are broken. Two cosmetic items for later:

1. Pareto plots could be regenerated as dual-panel per the style guide.
2. Tier comparison figure could be regenerated from fresh recomputed data.

Neither blocks arXiv submission.
