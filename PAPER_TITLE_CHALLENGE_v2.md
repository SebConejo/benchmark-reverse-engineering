# Paper Title Challenge v2 — Systematic Search

**Date:** 2026-05-19
**Objectif:** Trouver un titre sans faiblesse identifiable.

---

## Critères (tous obligatoires)

| # | Critère | Test |
|---|---------|------|
| C1 | Rigoureux scientifiquement | Un reviewer ne peut pas attaquer le titre |
| C2 | Mémorable / impactant | Un praticien s'arrête en scrollant arXiv ou Twitter |
| C3 | SEO friendly | Contient "cost", "quality", "LLM" + un parmi "benchmark/tasks/models" |
| C4 | Communique le scope | 46 modèles et/ou 21 tasks visibles |
| C5 | Communique le finding | Le lecteur sait ce qu'on a trouvé avant d'ouvrir le PDF |
| C6 | ≤15 mots | |
| C7 | Pas de jargon ambigu | Compréhensible par un ML engineer senior |
| C8 | Pas de mot péjoratif | Pas de "cheap", "budget", etc. |

---

## 10 variantes

### T1. TaskBench: 46 LLMs, 21 Tasks, and a Flat Cost-Quality Curve

| Critère | Verdict | Note |
|---------|---------|------|
| C1 Rigoureux | OK | "Flat curve" = observation géométrique, pas claim statistique |
| C2 Mémorable | OK | Structure "X, Y, and Z" crée la surprise sur le Z |
| C3 SEO | OK | cost ✓ quality ✓ LLM ✓ tasks ✓ ("benchmark" implicite dans TaskBench) |
| C4 Scope | OK | 46, 21 |
| C5 Finding | OK | "Flat curve" = payer plus ne change rien |
| C6 Longueur | OK | 13 mots |
| C7 Jargon | ? | "Flat curve" — clair pour ML, légèrement abstrait pour non-technique |
| C8 Péjoratif | OK | Rien |

**Faiblesse candidate :** "Flat curve" — un reviewer pourrait dire "la courbe
n'est pas plate, Micro est clairement en dessous." Réponse : le titre dit "a
flat curve", pas "a perfectly flat curve everywhere." La feature dominante de
la courbe IS sa platitude au-dessus de Micro. Et le paper montre Micro comme
le seul tier séparé (§4.2).

**Aussi :** "curve" implique une fonction continue alors qu'on a un scatter
plot avec 46 points discrets. Techniquement c'est un "trend" ou "relationship",
pas une "curve." Mais "flat cost-quality relationship" a 15 mots et sonne mal.

**Verdict : faiblesse mineure (jargon léger). Pas éliminatoire mais pas
parfait non plus.**

---

### T2. TaskBench: LLM Quality Does Not Scale with Cost — 46 Models, 21 Tasks

| Critère | Verdict |
|---------|---------|
| C1 | FAIL | "Does Not Scale" = overclaim. Quality DOES scale at Micro tier. |

**Éliminé.**

---

### T3. TaskBench: Benchmarking LLM Cost Against Quality Across 46 Models and 21 Tasks

| Critère | Verdict |
|---------|---------|
| C5 | FAIL | Pas de finding communiqué. Purement descriptif. |
| C2 | FAIL | Personne ne s'arrête pour un titre descriptif. |

**Éliminé.**

---

### T4. Do You Need an Expensive LLM? Benchmarking 46 Models Across 21 Tasks

| Critère | Verdict |
|---------|---------|
| C1 | FAIL | Une question rhétorique en titre implique "non" — overclaim pour n=2. |
| C3 | PARTIAL | Manque "cost" et "quality" explicitement. |

**Éliminé.**

---

### T5. TaskBench: Diminishing Returns on LLM Cost Across 46 Models and 21 Tasks

| Critère | Verdict | Note |
|---------|---------|------|
| C1 | OK | "Diminishing returns" est un concept économique standard et exact |
| C2 | MEDIUM | Moins intrigant que "flat curve" |
| C3 | PARTIAL | Manque "quality" explicitement |
| C5 | OK | "Diminishing returns" = le finding |

**Faiblesse :** "Diminishing returns" sous-estime le finding. Les returns ne
sont pas juste "diminishing" — ils sont quasi-nuls au-dessus de $0.50/M. Et
"quality" absent du titre est un trou SEO.

**Éliminé (C3 + faiblesse sémantique).**

---

### T6. TaskBench: 46 LLMs, 21 Tasks, and Negligible Cost-Quality Tradeoffs

| Critère | Verdict | Note |
|---------|---------|------|
| C1 | ? | "Negligible" — défendable pour Economy vs Premium (gap 0.042 = 0.84% de l'échelle). Mais les tradeoffs Micro vs reste ne sont PAS negligible (gap 0.27). Le titre dit "negligible tradeoffs" globalement → overclaim partiel. |

**Éliminé (même problème que "flat curve" mais plus grave — "negligible" est
un claim quantitatif, "flat" est une observation visuelle).**

---

### T7. TaskBench: Where LLM Cost Meets Quality — 46 Models Across 21 Tasks

| Critère | Verdict |
|---------|---------|
| C5 | FAIL | "Where X Meets Y" ne communique aucun finding. |

**Éliminé.**

---

### T8. TaskBench: Per-Task Cost-Quality Pareto Frontiers for 46 LLMs

| Critère | Verdict |
|---------|---------|
| C4 | PARTIAL | 46 modèles mais pas 21 tasks |
| C5 | FAIL | Pas de finding, juste la méthode |
| C7 | FAIL | "Pareto Frontiers" est du jargon |

**Éliminé.**

---

### T9. TaskBench: 46 LLMs, 21 Tasks, and Why Paying More Buys Little

| Critère | Verdict | Note |
|---------|---------|------|
| C1 | ? | "Buys Little" — est-ce défendable ? Gap max = +0.134 (OpenAI, 750×). "Little" pour 2.7% de l'échelle ? Oui. Mais "Why" implique explication causale, pas observation. |
| C8 | OK | Pas péjoratif mais "Paying More" cible implicitement les utilisateurs Premium |

**Faiblesse :** "Why" repromet une explication causale qu'on ne donne pas. Et
"Buys Little" est subjectif — un reviewer dira "little by whose standard?"

**Éliminé (C1 — "Why" + subjectivité).**

---

### T10. TaskBench: 46 LLMs, 21 Tasks, and a Flat Cost-Quality Curve Above $0.50/M

| Critère | Verdict | Note |
|---------|---------|------|
| C1 | OK | "Above $0.50/M" qualifie exactement où la courbe est plate — inattaquable |
| C6 | FAIL | 16 mots |

**Éliminé (longueur).**

---

## Bilan après 10 variantes

| Titre | Éliminé ? | Raison |
|-------|-----------|--------|
| T1 "Flat Cost-Quality Curve" | Non | Faiblesse mineure (jargon léger) |
| T2 "Does Not Scale" | Oui | Overclaim (Micro) |
| T3 descriptif pur | Oui | Pas de finding, pas mémorable |
| T4 question rhétorique | Oui | Overclaim implicite |
| T5 "Diminishing Returns" | Oui | Manque "quality", sous-estime le finding |
| T6 "Negligible Tradeoffs" | Oui | Overclaim (Micro tradeoffs not negligible) |
| T7 "Where X Meets Y" | Oui | Pas de finding |
| T8 "Pareto Frontiers" | Oui | Jargon, pas de finding |
| T9 "Paying More Buys Little" | Oui | Subjectif + "Why" non tenu |
| T10 "Flat... Above $0.50/M" | Oui | Trop long |

**Un seul survivant : T1.**

---

## Analyse approfondie de T1

> **TaskBench: 46 LLMs, 21 Tasks, and a Flat Cost-Quality Curve**

### Attaques possibles et défenses

**Attaque 1 : "La courbe n'est pas plate — Micro est en dessous."**
Défense : Le titre dit "a flat curve", pas "the curve is flat everywhere."
L'article structure Micro comme un tier séparé (§4.2). La courbe Economy–
Standard–Premium est plate (gap 0.042). Figure 2 le montre visuellement.

**Attaque 2 : "Curve" implique une fonction continue, vous avez 46 points.**
Défense : "Cost-quality curve" est l'usage standard en économie et ML pour
décrire la relation entre prix et performance, même avec des données
discrètes. Identique à "learning curve" (qui n'est pas une vraie courbe
mathématique non plus).

**Attaque 3 : "Flat" est subjectif — la courbe monte de +0.042.**
Défense : 0.042 sur une échelle de 4 points de range effectif (1–5) = 1%.
En économétrie, un R² de 0.01 entre prix et qualité justifie "flat." C'est
une observation visuelle du scatter plot, pas un test statistique — le test
est dans le paper (Mann-Whitney p>0.05).

**Attaque 4 : "C'est une observation, pas un claim. Où est la contribution ?"**
Défense : L'observation EST la contribution. "The world is flat" (la Terre
est plate) serait un claim. "We found a flat curve" est un résultat empirique.
Le titre dit ce qu'on a trouvé, le paper dit pourquoi c'est important.

### Faiblesse résiduelle

"Flat curve" est légèrement abstrait pour un non-expert. Un data scientist
comprend immédiatement. Un CTO pourrait hésiter 2 secondes. Mais l'audience
primaire (ML practitioners, evaluation researchers) comprend sans friction.

Cette faiblesse est **inhérente au domaine**, pas au titre. Tout titre qui
communique un finding technique sera légèrement abstrait pour les non-experts.
Il n'y a pas de formulation qui soit simultanément rigoureuse, concise, et
accessible à un non-technicien.

---

## Recommandation finale

> **TaskBench: 46 LLMs, 21 Tasks, and a Flat Cost-Quality Curve**

C'est le seul titre sur 10 qui survit à tous les critères. Sa faiblesse
résiduelle (abstraction légère de "flat curve") est inhérente au domaine et
non éliminable sans sacrifier la rigueur ou le finding.

Aucun titre ne peut être "sans faiblesse" sur ce sujet, parce que le finding
principal (Economy ≈ Premium) a un caveat structurel (n=2) qui empêche tout
claim absolu. "Flat curve" contourne ce problème en décrivant la FORME de la
relation plutôt que de claimer une ABSENCE de différence. C'est la formulation
la plus honnête et la moins attaquable disponible.
