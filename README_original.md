# Benchmark Paper Reverse Engineering

Reverse engineering of 6 published LLM benchmark papers to extract presentation patterns for methodology, results communication, repo organization, and limitations handling.

## Benchmarks Analyzed

| Benchmark | Paper | Repo |
|-----------|-------|------|
| HELM | [arXiv:2211.09110](https://arxiv.org/abs/2211.09110) | [stanford-crfm/helm](https://github.com/stanford-crfm/helm) |
| MMLU | [arXiv:2009.03300](https://arxiv.org/abs/2009.03300) | [hendrycks/test](https://github.com/hendrycks/test) |
| HumanEval | [arXiv:2107.03374](https://arxiv.org/abs/2107.03374) | [openai/human-eval](https://github.com/openai/human-eval) |
| Chatbot Arena | [arXiv:2403.04132](https://arxiv.org/abs/2403.04132) | [lm-sys/FastChat](https://github.com/lm-sys/FastChat) |
| MTEB | [arXiv:2210.07316](https://arxiv.org/abs/2210.07316) | [embeddings-benchmark/mteb](https://github.com/embeddings-benchmark/mteb) |
| RouterArena | [arXiv:2510.00202](https://arxiv.org/abs/2510.00202) | [RouteWorks/RouterArena](https://github.com/RouteWorks/RouterArena) |

## Structure

```
reverse-engineering/     # Per-benchmark analyses + synthesis
  helm.md
  mmlu.md
  humaneval.md
  chatbot-arena.md
  mteb.md
  routerarena.md
  synthesis.md           # Cross-benchmark patterns & recommendations
skills/                  # Claude Code skills used
  benchmark-paper-reverse-engineering/SKILL.md
  learn/SKILL.md
learnings/               # Persisted key patterns (JSONL)
  learnings.jsonl
```

## Key Findings

See `reverse-engineering/synthesis.md` for the full synthesis. Top-line patterns:

1. Abstract structure: gap-first, then contribution, then scale numbers
2. Methodology: "map then select" pattern legitimizes scope decisions
3. Launch: leaderboard-first beats paper-first for community adoption
4. Results: never declare a single winner; frame headline as surprising
5. Limitations: dedicated section, reframe scope as design choice
6. Repo: pip-installable, data on HuggingFace, automated CI evaluation
