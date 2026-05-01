# Synthesis — Benchmark Paper Reverse Engineering

Based on analysis of: HELM, MMLU, HumanEval, Chatbot Arena, MTEB, RouterArena.

---

## Recurring Patterns

### Paper Structure

**Methodology before results.** Every benchmark studied places its methodology section before results (HELM, MMLU, HumanEval, Chatbot Arena, MTEB, RouterArena). The methodology-first ordering is universal and non-negotiable for credibility.

**Abstract frames a gap, not a contribution.** All six papers open their abstract with what's wrong or missing in current evaluation, not with "we built X." HELM: "lack of transparency." MMLU: models at "near random chance." HumanEval: BLEU is inadequate. Chatbot Arena: "evaluating alignment is hard." MTEB: "unclear whether STS embeddings generalize." RouterArena: "no comprehensive platform." The contribution is introduced as the response to the gap.

**Scale numbers in the abstract.** HELM (30 models, 42 scenarios, $38K), MMLU (57 subjects), MTEB (8 tasks, 58 datasets, 112 languages), RouterArena (8,400 queries, 42 models, 14 routers), Chatbot Arena (1.5M+ votes, 70+ LLMs). The abstract establishes authority through scope.

### Methodology Presentation

**Taxonomy before selection.** HELM and MTEB both map the full space of what could be evaluated, then justify their subset. This "map then select" pattern legitimizes the benchmark by proving awareness of exclusions. RouterArena uses "principles" (DDC, Bloom) as a lighter version of the same idea.

**Metrics justified by deployment concern, not mathematical derivation.** RouterArena maps its 5 metrics to deployment realities (accuracy=quality, cost=economics, etc). HELM motivates each metric by a real-world concern (fairness=deployment risk). Chatbot Arena is the exception — it provides full mathematical justification for BT over Elo. The stronger your metric is novel, the more justification you need.

**Reproducibility asymmetry: paper states what, repo shows how.** MMLU's paper is deliberately terse on protocol details; the code fills in. HumanEval provides the metric formula and sampling params but not seeds. HELM points to the website for exact prompts. The pattern is: enough detail in the paper for replication in principle, with the code/website as the authoritative reference.

### Results Communication

**No single winner declared.** HELM: no model declared "the best" (findings are structural patterns). MMLU: frames as diagnostic of failure. MTEB: "no method dominates." RouterArena: GPT-5 highest accuracy but not best ranked. Only Chatbot Arena produces an explicit ranking (that's its purpose), and even it frames the contribution as "credible rankings exist" not "model X wins."

**Tables over figures for leaderboard papers.** MTEB (14 tables, 6 figures), MMLU (dominated by tables), RouterArena (tables as culminating artifact). The scatter/Pareto plot appears when cost-quality tradeoff matters (MTEB quality-vs-speed, RouterArena deferral curves).

**Headline finding is surprising, not confirmatory.** MMLU: college math > elementary math. RouterArena: best accuracy ≠ best rank. HumanEval: 100 samples reach 70% where 1 sample reaches 28%. The surprising finding is what gets cited.

### Limitations Handling

**Two valid strategies exist.**
1. Dedicated section (HELM, HumanEval, Chatbot Arena) — standard placement after results, before conclusion. Works for benchmarks that want to signal thoroughness.
2. Scattered as observations (RouterArena, MMLU) — limitations emerge as findings about the field. Works for benchmarks that position as platforms rather than static contributions.

**Limitations reframed as design choices.** HELM: "design-intentional incompleteness." MMLU: format acknowledged as deliberately chosen for evaluation simplicity. HumanEval: scope explicitly stated (simple functions, Python only). Never apologetic.

**Contamination addressed head-on.** MMLU measures contamination rather than claiming absence (Appendix B.2). This is the gold standard for static benchmarks.

### Repo Organization

**Two archetypes: minimal vs platform.**
- Minimal (MMLU, HumanEval): flat structure, single eval script, data external, no CI, no docs. Works when the benchmark is dead-simple to run.
- Platform (HELM, MTEB, Chatbot Arena): full package with CLI, docs, leaderboard code, model wrappers, contributing guides. Works when the benchmark needs ongoing community participation.

RouterArena sits between — organized as a platform but without the polish of HELM/MTEB.

**README leads with identity + scale, then installation.** HELM: one sentence + features. MTEB: tagline + badges + nav. Chatbot Arena: definition + achievement numbers. MMLU is the outlier (paper title + leaderboard table). Tool-first READMEs win for adoption.

**Data never in the repo for large benchmarks.** HELM downloads on-demand. MTEB pulls from HF Hub. Chatbot Arena on HF. Only the minimal benchmarks (HumanEval's 164-problem JSONL, MMLU's tar) bundle data directly.

### Communication / Launch

**Three launch strategies, ranked by adoption:**
1. **Leaderboard-first** (Chatbot Arena, MTEB): ship the interactive artifact, paper follows months later. Highest community engagement. Self-reinforcing: utility → citations → more submissions → more utility.
2. **Full-package simultaneous** (HELM): paper + blog + leaderboard on the same day. Requires institutional resources.
3. **Paper-first minimal** (MMLU, HumanEval): paper + flat repo, no leaderboard, no blog. Works when the benchmark is so simple it spreads by properties alone.

RouterArena uses paper-first with leaderboard attached — the Rice University approach (less institutional weight, needs the paper for credibility first).

**Blog ≠ paper.** When a blog exists (HELM, Chatbot Arena, MTEB), it leads with the *why* and provides accessible entry. The paper provides *rigor*. They serve different audiences and must not duplicate.

---

## Divergent Patterns

| Dimension | Pattern A | Pattern B |
|-----------|-----------|-----------|
| Abstract framing | Gap-first (HELM, MMLU, MTEB) | Results-first social proof (Chatbot Arena) |
| Limitations | Dedicated section (HELM, HumanEval, Arena) | Scattered/absent (RouterArena, MMLU) |
| Launch | Leaderboard-first (Arena, MTEB) | Paper-first (MMLU, HumanEval, RouterArena) |
| Repo style | Platform (HELM, MTEB) | Minimal fire-and-forget (MMLU, HumanEval) |
| Related Work | After intro (MMLU, Arena) | After results (RouterArena, HumanEval) |
| Variance | Scale substitutes for stats (HELM, MMLU) | Explicit estimator analysis (HumanEval) |
| Metric count | Single metric (MMLU: accuracy) | Multi-metric (HELM: 7, RouterArena: 5) |
| Data location | External (HELM, MTEB, Arena) | Bundled (HumanEval, MMLU) |

---

## What the Best Benchmarks Do

### Chatbot Arena — strongest community adoption

- **Phased launch builds compounding credibility.** Blog → weekly updates → dataset → paper → institutional site. Each phase adds a legitimacy layer.
- **The leaderboard IS the contribution.** The paper formalizes what already exists and works. This means the paper can be confident rather than aspirational.
- **Statistical rigor on the ranking mechanism.** BT justified over Elo with proofs, sandwich covariance, nonparametric validity. The methodology is unassailable because they invested in proving the statistical backbone.

### HELM — strongest methodology presentation

- **"Map then select" legitimizes scope decisions.** By showing the full space and then justifying the subset, HELM pre-empts "why didn't you include X?" criticism.
- **Numbered findings are quotable.** 25 declarative statements that researchers can cite individually. This is better than "see Table 3" for academic impact.
- **Living benchmark framing turns limitations into features.** "This is v1 of an ongoing effort" neutralizes criticism about coverage gaps.

### HumanEval — strongest minimalism

- **One JSONL file, one pip command.** Zero friction = maximum adoption. HumanEval became canonical not despite its simplicity but because of it.
- **Novel metric with full mathematical rigor.** pass@k gets a definition, an unbiasedness proof, a numpy implementation, and an empirical comparison to the metric it replaces (BLEU). When you introduce a new metric, this is the standard.
- **Synthetic experiments to characterize limitations.** Building controlled experiments to prove where your benchmark breaks is more credible than listing limitations you observed.

---

## What to Avoid

1. **Generic repo names.** MMLU's "test" repo lost discoverability. The community had to invent the name "MMLU" itself. Name your repo after your benchmark.

2. **Variance hand-waving.** HELM and MMLU report no uncertainty. This works at their scale (4,900+ evaluations / 57 subjects) but looks weak for smaller benchmarks. If you have fewer than ~1,000 data points, you need explicit variance reporting.

3. **Scattered limitations without a platform defense.** RouterArena gets away with no limitations section because it positions as a living platform. If you're publishing a static benchmark, scattered limitations look like you're hiding something. Pick one strategy and commit.

4. **Blog post that duplicates the paper.** None of the successful launches did this. The blog is for "why this matters and how to use it." The paper is for "this is rigorous." Duplication wastes both audiences' time.

5. **Leaderboard without governance.** RouterArena's leaderboard has no update cadence, no funding disclosure. Chatbot Arena's phased updates and MTEB's HF Space discussions show how to build trust. A leaderboard that might go stale erodes credibility.

6. **Massive author lists for small teams.** HELM's 47 authors signals institutional effort. If your actual team is 3-5 people, a long author list looks padded. HumanEval's 58 authors works because it's OpenAI releasing a product capability; a university group of 7 (RouterArena) is more credible.

7. **Defending metric choices that are standard.** MTEB uses accuracy, F1, NDCG, Spearman — never justifies them because they're community-standard. Only defend metrics that are novel or controversial.

---

## Recommendations for Our Benchmark (TaskBench)

### Paper Structure

1. **Open the abstract with the gap**: "Current routing evaluations use synthetic prompts and single-metric comparisons, making it unclear whether routers generalize to production workloads." Then introduce TaskBench as the response.
2. **Include scale numbers in the abstract**: total tasks, total models, total routing decisions evaluated, total API spend.
3. **Use the HELM "map then select" pattern** for methodology: show the full space of possible production tasks, then justify which subset you included and why.
4. **Place Related Work after experiments** (RouterArena pattern). This lets your comparison table (vs RouterArena, vs synthetic benchmarks) function as a strength demonstration rather than a positioning exercise.
5. **End with numbered findings** (HELM pattern). 5-10 declarative, quotable conclusions. Not "Table 3 shows..." but "Production routing saves 40-60% cost with <3% quality loss on simple tasks."

### Metrics & Methodology

6. **Justify your metrics by deployment concern**: cost savings → economics, quality retention → reliability, routing latency → system overhead. Don't derive axiomatically unless you invent a novel metric.
7. **If you introduce a novel metric (e.g. "routing efficiency score")**: give it the HumanEval treatment — formal definition, proof of desired properties, reference implementation, empirical comparison to the metric it replaces.
8. **Address contamination explicitly** if using public prompts. Measure it (MMLU pattern), don't claim absence.
9. **Report variance** since TaskBench won't have HELM-scale breadth. Bootstrap CIs on quality metrics, or run each router N times with temperature>0 and report std.

### Repo Organization

10. **Name the repo "taskbench"** — not a generic name. Make it findable.
11. **Choose the platform archetype** (HELM/MTEB), not the minimal one (MMLU/HumanEval). TaskBench needs community submissions to stay relevant, so invest in: pip-installable package, CLI entry point, contributing guide, leaderboard code.
12. **Data on HuggingFace** (MTEB pattern). Keep the repo code-only. This separates evaluation infrastructure from dataset versioning.
13. **README: identity sentence → scale number → installation → usage → leaderboard link → citation.** Tool-first.

### Results Presentation

14. **Lead with the Pareto plot** (RouterArena's deferral curve / MTEB's quality-vs-speed scatter). This is what routing benchmarks are expected to show. Make it the Figure 1.
15. **Use a normalized visualization** (RouterArena pattern) so that readers can compare across different model pools fairly.
16. **Frame the headline finding as surprising**: e.g., "Simple keyword-based routing matches neural routers on 70% of production tasks at 1/100th the latency." The surprising finding is what gets shared on X.
17. **Declare no single winner** unless one genuinely dominates. "No routing approach dominates across all task types and cost constraints" is a stronger finding than crowning a champion.

### Limitations Handling

18. **Use a dedicated section** — we're a small team publishing a static benchmark (not a platform yet), so scattered limitations would look evasive.
19. **Reframe scope as design choice** (HELM pattern): "TaskBench evaluates routing on personal-agent workloads by design. Enterprise batch workloads are a distinct evaluation target."
20. **Build a synthetic experiment** to characterize one limitation (HumanEval pattern): e.g., show how routing accuracy degrades as prompt complexity increases, using controlled synthetic prompts of varying difficulty.

### Launch Strategy

21. **Paper-first, leaderboard-simultaneous** (like RouterArena but with more polish). We don't have Chatbot Arena's pre-existing community or MTEB's HuggingFace platform, so the paper provides initial credibility.
22. **Ship a blog post on the same day** (HELM pattern). Blog leads with "why routing evaluation is broken" + one surprising finding + a link to the interactive leaderboard. Keep it to 800 words.
23. **Automated submission via PR** (RouterArena pattern). `/evaluate` comment trigger for CI-based scoring. Provide a 10% local test subset.
24. **Announce with the surprising finding**, not with "we release TaskBench." The finding is the hook; the benchmark is the mechanism.

---

## Writing Style Guide

Extracted from the prose patterns of all 6 benchmarks. Directly usable by a redaction agent writing the TaskBench paper.

### Universal Patterns (present in all 6 papers)

**"We find that [X]"** is the universal sentence template for introducing findings. Every paper uses it as the canonical way to present empirical results. It is direct, unhedged, and attributes the observation to the authors without implying causation.

**First-person plural "we"** is the only acceptable authorial voice. No paper uses "I," "one," or "it is argued that." The split is functional: "we" for what the authors chose to do; passive for what is necessarily true or for describing systems. This is non-negotiable.

**Hedging is two-tiered everywhere.** Empirical observations ("We find that X") are unhedged. Predictions, implications, and causal explanations are hedged with "may," "could," "suggests." Never hedge on your own numbers. Never use "perhaps" or "it seems."

**Terms are defined inline, on first use, in the same sentence that uses them.** Never in standalone "Definition:" blocks. The two sub-patterns:
- Appositive: "Term, [definition clause], [attribution], predicate" (HELM, MMLU)
- Operational: "We define X: [procedure]" or "Term—[noun-phrase definition]" (RouterArena, HumanEval)

**Em-dashes are absent or rare** in 5 of 6 papers. RouterArena is the exception (uses them for definitions). The norm: commas and parentheticals carry all parenthetical content. Do not over-use em-dashes.

**Citations are parenthetical, end-of-clause.** Never "Smith (2022) showed that..." unless the cited work is itself the topic of the sentence. Multiple citations semicolon-separated. Density drops in Results — cite to establish precedent in intro/methods, let your own numbers speak in results.

### Sentence Templates to Use

These templates recur across multiple papers. Use them as the backbone of TaskBench prose:

| Template | Function | Example source |
|----------|----------|---------------|
| "We find that [observation]." | Introduce any empirical finding | All 6 |
| "To [purpose], we [action]." | Justify a methodological choice | MMLU, HumanEval, Arena |
| "[Prior claim]. However, [complication]." | Pivot from prior work to your gap | MMLU (signature), HELM |
| "This [verb] that [implication]." | Draw a conclusion from evidence | MMLU, MTEB |
| "No single X is universally Y." | State a key negative finding | RouterArena, MTEB |
| "In contrast to [prior work], [our work] Y." | Position against baselines | RouterArena, HELM |
| "Our [noun] features [3-4 items]." | Summarize contributions | RouterArena, HELM |
| "We define X: [operational procedure]." | Introduce a new metric | RouterArena, HumanEval |
| "[Model/System] achieves [N]%, while [baseline] achieves [M]%." | Report comparative results | HumanEval, MMLU |
| "Although [strength], [limitation/qualification]." | Concede limitations gracefully | Arena |

### How to Hedge vs Assert

**Assert (use "We find that", "X is", "X shows")** when:
- Reporting your own measured numbers
- Stating what your benchmark includes/excludes (scope is a design choice)
- Describing your methodology

**Hedge (use "may," "could," "suggests," "we anticipate")** when:
- Explaining WHY a result occurred (causal claims)
- Discussing future implications or generalizability
- Describing limitations of other systems

**Never hedge** with "perhaps," "it seems," "arguably," "it could be argued." These are weak. Use "may" for genuine uncertainty, nothing for confidence.

### Punctuation Conventions

| Mark | Use | Avoid |
|------|-----|-------|
| Colons | Introduce lists, expansions, elaborations | |
| Parentheses | Citations, abbreviations, quick examples "(e.g., ...)" | Long asides (>15 words) |
| Semicolons | Join balanced independent clauses (optional — 3/6 papers avoid them entirely) | |
| Em-dashes | Sparingly, for definitions only (RouterArena pattern). Most papers avoid. | Casual interjections |
| Oxford comma | Always | |
| "e.g.," | For inline examples | "for example" in running prose (too wordy) |

### Register Map (How to Write Each Section)

| Section | Register | Characteristics |
|---------|----------|----------------|
| Abstract | Accessible + assertive | Gap statement, then contribution, then scale numbers. Short sentences. No jargon. |
| Introduction | Motivational + rhetorical | Broader stakes, evaluative language ("concerning," "unclear"), "However" pivots |
| Methodology | Precise + procedural | Definitions, "consists of" structures, "We define X" templates, shorter clauses |
| Results | Declarative + empirical | "We find that" sentences, numbers without hedging, comparative templates |
| Limitations | Honest + confident | Concessive "Although X, Y" structures, "design choice" framing, no apology |
| Conclusion | Elevated + forward-looking | Returns to intro register, "should" prescriptions, community invitation |

### Vocabulary to Use

From the analyzed papers, these words are safe (proven academic register, never flagged as AI-ish):

- **For findings**: "we find," "we observe," "we show," "reveals," "indicates"
- **For comparisons**: "outperforms," "on par with," "competitive with," "Nx smaller/larger"
- **For importance**: "suggests," "highlights," "underscores" (use sparingly)
- **For scope**: "spans," "covers," "encompasses," "consists of"
- **For gaps**: "remains unclear," "has not been addressed," "is lacking"
- **For contribution**: "we introduce," "we propose," "we release," "we present"
- **One vivid word** per paper is acceptable for memorability (MMLU's "lopsided," HELM's "desperately needed," HumanEval's "surprisingly effective"). Pick one — don't over-do.

### Vocabulary to Avoid

These words are either too informal, too AI-sounding, or absent from all 6 papers:

- "delve," "crucial," "robust" (as empty intensifier), "comprehensive" (unless it's your literal differentiator like RouterArena), "nuanced," "multifaceted," "furthermore," "moreover," "additionally" (prefer "Further," or nothing)
- "groundbreaking," "revolutionary," "state-of-the-art" as standalone noun ("the SOTA")
- "it should be noted that," "it is worth mentioning," "interestingly" (used once by RouterArena, otherwise absent)
- "leverage" (overused in 2024 AI papers — use "use" or a specific verb instead)
- All superlatives unless backed by a measurement ("best" only if literally ranked #1)

### Sentence Length & Rhythm

Target: 15-30 words per sentence. 60% complex (one subordinate clause), 25% compound, 15% simple (for emphasis).

Pattern: substantive claim (short) → qualification or expansion (medium-long) → next claim. The short sentence carries the finding; the longer sentence provides context. Never more than 2 long sentences in a row without a short one to reset rhythm.

### The Researcher Voice (Summary)

The voice across all 6 papers is: **authoritative but measured, precise but accessible, confident about data but humble about implications.** It is NOT: promotional, defensive, casual, or uncertain. Write as a senior researcher presenting findings to peers — frank about what you found, clear about what it means, transparent about what it doesn't cover.
