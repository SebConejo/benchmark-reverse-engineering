# Paper Title — Final

**Date:** 2026-05-19

---

## Specs

1. Format "TaskBench: [...]"
2. Verbe descriptif après le deux-points
3. Mots-clés : "cost-quality" (ou equiv) + "LLM"/"Language Models"
4. Scope visible : 46 models, 21 tasks (ou equiv)
5. 8–12 mots
6. Pas de claim finding
7. Pas de jargon

---

## Variantes

### T1. TaskBench: Measuring LLM Cost-Quality Tradeoffs Across 46 Models and 21 Tasks

| Spec | OK? |
|------|-----|
| S1 "TaskBench: [...]" | OK |
| S2 Verbe descriptif | OK — "Measuring" |
| S3 Mots-clés | OK — "cost-quality" + "LLM" |
| S4 Scope | OK — "46 Models and 21 Tasks" |
| S5 8–12 mots | OK — 11 mots |
| S6 Pas de claim | OK |
| S7 Pas de jargon | OK |

---

### T2. TaskBench: Evaluating LLM Cost and Quality Across 46 Models and 21 Tasks

| Spec | OK? |
|------|-----|
| S1 | OK |
| S2 | OK — "Evaluating" |
| S3 | OK — "Cost and Quality" + "LLM" |
| S4 | OK — "46 Models and 21 Tasks" |
| S5 | OK — 12 mots |
| S6 | OK |
| S7 | OK |

---

### T3. TaskBench: Benchmarking Cost-Quality Tradeoffs for 46 LLMs on 21 Tasks

| Spec | OK? |
|------|-----|
| S1 | OK |
| S2 | OK — "Benchmarking" |
| S3 | OK — "Cost-Quality" + "LLMs" |
| S4 | OK — "46 LLMs" + "21 Tasks" |
| S5 | OK — 10 mots |
| S6 | OK |
| S7 | OK |

---

### T4. TaskBench: Comparing LLM Cost and Quality Across 46 Models and 21 Tasks

| Spec | OK? |
|------|-----|
| S1 | OK |
| S2 | OK — "Comparing" |
| S3 | OK — "Cost and Quality" + "LLM" |
| S4 | OK — "46 Models and 21 Tasks" |
| S5 | OK — 12 mots |
| S6 | OK |
| S7 | OK |

---

### T5. TaskBench: Measuring Cost-Quality Tradeoffs Across 46 LLMs and 21 Production Tasks

| Spec | OK? |
|------|-----|
| S1 | OK |
| S2 | OK — "Measuring" |
| S3 | OK — "Cost-Quality" + "LLMs" |
| S4 | OK — "46 LLMs and 21 Production Tasks" |
| S5 | BORDERLINE — 11 mots (12 si on compte "Production") |
| S6 | OK |
| S7 | OK |

Note : "Production Tasks" ajoute un signal utile — on benchmark des tâches
de production, pas des exams académiques (MMLU) ni du chat (Arena). Distingue
TaskBench du reste du champ. 12 mots, à la limite haute de la spec.

---

## Recommandation

**T3 : TaskBench: Benchmarking Cost-Quality Tradeoffs for 46 LLMs on 21 Tasks**

- 10 mots, compact
- "Benchmarking" est le verbe le plus précis (c'est ce qu'on fait)
- "Cost-Quality Tradeoffs" en un seul composé hyphenné, efficace
- "for 46 LLMs on 21 Tasks" — prépositions courtes, scope immédiat
- Zéro claim, zéro jargon, zéro ambiguïté

Alternative si on veut "Production Tasks" : T5 (12 mots, ajoute la
différenciation vs benchmarks académiques).

Alternative si on préfère "Measuring" à "Benchmarking" : T1 (11 mots,
évite la redondance TaskBench + Benchmarking).

Note sur la redondance T3 : "TaskBench: Benchmarking..." — "Bench" +
"Benchmarking" est une légère redondance. T1 ("Measuring") l'évite.
Si ça gêne : T1. Si ça ne gêne pas : T3.
