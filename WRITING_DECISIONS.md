# Writing Decisions Log

Decisions made during paper drafting where the outline was ambiguous or
a conservative choice was needed. Review these on return.

## D1: Figure paths

The outline specifies 5 main figures. I use `\includegraphics` with paths
relative to the paper directory. The actual figure files are:
- `../results/analysis_v3_final/heatmap_v3.svg` (Figure 1)
- `../results/analysis_v3_final/tier_comparison_v3.svg` (Figure 2)
- `../results/figures/pareto_rag_qa.png` (Figure 3)
- `../results/figures/pareto_data_to_text.png` (Figure 4)
- `../results/analysis_v3_final/provider_gradient.svg` (Figure 5)

SVG files may need conversion to PDF for LaTeX compilation. I add a comment
noting this. The `\includegraphics` calls will work once converted.

## D2: RAG QA V2 r value

FINAL_GO_NO_GO.md corrected 0.887 to 0.888 (r=0.8885 rounds to 0.888).
The Abstract uses "r=0.89-0.91" which covers this correctly. In Section 3.4
I write r=0.888 per the correction.

## D3: Number of models claiming "49 with 21/21 tasks"

49 models have rows for all 21 tasks, but only 46 meet the >=40 cases/task
threshold. I use 46 everywhere, consistent with FINAL_FINDINGS_v3.md and
PAPER_OUTLINE_v2.md.

## D4: Provider gradient narrative

The outline lists specific provider comparisons. For OpenAI, the cheapest
is GPT-5.4 Nano at $0.02/M and the most expensive is GPT-5.5 Pro at $15/M.
The price ratio is 750x and the quality delta is +0.134 (4.828 - 4.694).
I keep these exact numbers from provider_gradient.json.

## D5: Appendix scope

The outline calls for 8 appendices (A-H). I include all 8 as section headers
with brief content descriptions. Full tables and figures will be populated
during formatting. The appendix text is kept minimal to stay within page budget.

## D6: Bibliography

I create a minimal .bib file with the key references cited in the paper.
Full bibliographic details may need verification against the actual papers.

## D7: Abstract em-dash removal

The abstract was already fixed in the previous session. I verified no em-dashes
remain in main.tex before starting.

## D8: Translation BLEU inconclusive

Section 3.4 mentions translation BLEU correlation as inconclusive (r=0.29).
The outline says to note this is a BLEU limitation, not a judge limitation.
I follow this framing exactly.

## D9: F12 dropped

Finding 12 (Premium better on language tasks) is dropped from the main paper
per PAPER_OUTLINE_v2.md. I include one sentence in Discussion noting Premium
may add marginal value on open-ended tasks, within CI bounds.

## D10: Exact match scoring description

The methodology describes exact match as binary (correct/incorrect). The CSV
uses score=5 for correct and score=0 for incorrect. I describe this as "binary
accuracy" in the paper rather than explaining the 0/5 encoding.
