# HumanEval — Reverse-Engineering Analysis

## Source

- **Paper**: "Evaluating Large Language Models Trained on Code" — https://arxiv.org/abs/2107.03374
- **Repo**: https://github.com/openai/human-eval (MIT, 3,220 stars)
- **Year**: July 7, 2021 (repo created July 6)
- **Authors**: 58 authors, OpenAI. Four leads with equal contribution (Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan).
- **Dual nature**: simultaneously a benchmark paper and a model-capability disclosure (Codex → GitHub Copilot)

## Paper Structure

31 pages (15 main body + appendices). Sections:

1. Abstract
2. Introduction
3. Evaluation Framework (2.1 Functional Correctness, 2.2 HumanEval, 2.3 Sandbox)
4. Code Fine-Tuning (data, methods, results, comparisons)
5. Supervised Fine-Tuning
6. Docstring Generation
7. **Limitations** — dedicated section
8. **Broader Impacts** — 8 subsections, ~4 pages
9. Related Work (placed AFTER limitations and impacts)
10. Conclusion
11. Appendices A-H

Key structural decisions: benchmark introduced in Section 2 titled "Evaluation Framework" (not "Benchmark" or "Dataset"). Limitations gets its own section before Related Work. Broader Impacts is massive (8 subsections) — reflecting responsible-disclosure framing for a product capability.

## Methodology Presentation

Precision in some dimensions, deliberate vagueness in others:

**Specified exactly:**
- pass@k metric: formal definition (Equation 1) + unbiasedness proof (Appendix A) + reference numpy implementation (Figure 3)
- Sampling: n=200 per task, nucleus top_p=0.95, T=0.8. Optimal temperatures stated per metric.
- Stop sequences enumerated
- Dataset: 164 problems, avg 7.7 unit tests
- Sandbox: gVisor + eBPF firewall on Kubernetes

**Left unspecified:**
- No random seeds
- No checkpoint hashes — models by parameter count only
- No separate prompt template doc (prompts = docstrings)

Metric justification by contrast: two paragraphs arguing BLEU is inadequate (with later empirical proof in Figure 8 showing BLEU distributions for correct/incorrect overlap). Then functional correctness as the natural alternative.

Statistical rigor: Appendix A proves naive estimator is biased, Figure 13 shows bias/variance curves with confidence bands. Unusual care for a systems paper.

## Results Communication

12 figures in main body. Types:
- **Scaling curves** (signature visual): pass rate vs model size on log-x axis
- **Hyperparameter sweeps**: pass@k vs samples, temperature as parameter
- **Sample ranking heuristics**: oracle vs logp vs random
- **Distribution histograms**: BLEU for correct vs wrong (proving BLEU inadequate)
- **Code examples**: actual prompt/completion with color highlighting
- **Degradation curve**: pass rate vs chained complexity (exponential decay)

Tables: pass@k for k=1,10,100 across models. Models grouped by family, sizes ascending.

Headline ordering: own result first (28.8%), baselines second (GPT-3=0%, GPT-J=11.4%), best-case third (70.2% with 100 samples).

No error bars in main tables. Variance discussion entirely about estimator properties, not run-to-run variation.

Tone: measured, technical. No superlatives. "A surprisingly effective strategy," "this result suggests."

## Questions the Benchmark Answers

- What fraction of simple programming problems can a code LLM solve in one attempt?
- How does that change with repeated sampling?
- How does code generation scale with parameters?
- What's the optimal temperature for pass@1 vs pass@100?
- Can heuristic ranking substitute for oracle selection?
- Is BLEU reliable for code?
- How does performance degrade with docstring complexity?

Explicitly does NOT answer: multi-file, real codebases, debugging, non-Python.

## Limitations Handling

Dedicated Section 6, ~1 page. After all results, before Broader Impacts.

Types:
- Sample efficiency (training on millions of lines vs student needing far less)
- Counter-intuitive failures (syntactically incorrect, undefined variables)
- Complexity scaling (exponential degradation — backed by synthetic experiment)
- Variable binding errors (concrete code example shown)

Framing: honest, evidence-backed observations. The synthetic chaining experiment is notable — they built a controlled experiment specifically to characterize a limitation. Goes beyond "here are things we noticed."

Broader Impacts (Section 7, 4 pages): over-reliance, misalignment, bias, economic impacts, security, environment, legal, risk mitigation. More like a responsible-deployment document than a paper appendix.

## Repo Organization

```
LICENSE (MIT)
README.md
requirements.txt
setup.py
data/
  HumanEval.jsonl.gz       # 164 problems
  example_problem.jsonl
  example_samples.jsonl
human_eval/
  __init__.py
  data.py
  evaluate_functional_correctness.py
  evaluation.py
  execution.py
```

Installable Python package (pip install -e). Data = single gzipped JSONL. No train/test split. Security warning on execution prominently in README. Console entry point for CLI evaluation.

No leaderboard, no results, no badges, no CI, no contributing guidelines. Maximally minimal.

## Communication / Launch

**Paper-first, code-simultaneous** (repo July 6, paper July 7). Repo description: "Code for the paper..."

Blog post about Codex (the product), not about HumanEval (the benchmark). Benchmark positioned as evidence for Codex capabilities, not as independent contribution — despite HumanEval becoming arguably more influential than any Codex model.

"Fire and forget" release: MIT license, one JSONL file, one command. No registration, no submission server, no leaderboard. This became the greatest distribution advantage.

No versioning, no v2, no expansion. Static dataset, 164 problems forever.
