# Paper Title Challenge

**Date:** 2026-05-19
**Candidat actuel:** "TaskBench: Economy LLMs Show No Quality Gap vs. Premium Across 21 Tasks"

---

## 1. Critique sur 5 angles

### 1.1 Précision scientifique

"No Quality Gap" est un claim d'absence. Les Mann-Whitney p>0.05 disent "nous
n'avons pas détecté de différence significative" — ce n'est pas la même chose
que "il n'y a pas de gap." L'absence de preuve n'est pas la preuve d'absence.

Un reviewer attaquera sur deux fronts :
- **n=2 Premium** : le test manque de puissance. On n'a pas détecté de gap
  parce qu'on n'avait pas assez de données pour le détecter.
- **"No Gap" vs "No Significant Gap"** : en titre, "No Quality Gap" est un
  claim absolu. Le corps du paper dit "no difference detected" (correct),
  mais le titre dit "no gap" (overclaim).

"No Statistically Significant Quality Gap" est rigoureux mais lourd (6 mots
pour un qualificatif). Compromis : "No Significant Quality Gap" (4 mots).

**Verdict : attaquable. "No Quality Gap" est trop fort pour n=2.**

### 1.2 Impact / attractivité

Comparaison avec des titres à succès :

| Paper | Titre | Pourquoi ça marche |
|-------|-------|-------------------|
| HELM | "Holistic Evaluation of Language Models" | Nom propre fort, descriptif |
| MMLU | "Measuring Massive Multitask Language Understanding" | Allitération, scope dans le titre |
| BIG-bench | "Beyond the Imitation Game Benchmark" | Référence culturelle, ambition |
| Chatbot Arena | "Chatbot Arena: An Open Platform..." | Nom mémorable + description |
| FrugalGPT | "FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance" | Nom accrocheur + promesse concrète |

Le candidat actuel : informatif mais plat. Pas de nom mémorable au-delà de
"TaskBench". Pas de tension, pas de surprise. Un lecteur arXiv scrollant voit
"No Quality Gap" et pense "ok, encore un paper qui dit que les modèles cheap
sont bons." Pas assez différenciant.

**Verdict : fonctionnel mais pas mémorable.**

### 1.3 Mémorabilité / SEO

Requête probable : "LLM cost benchmark", "cheap vs expensive LLM",
"LLM model comparison cost quality."

Le titre contient "Economy LLMs", "Premium", "Quality Gap", "21 Tasks" — bons
mots-clés. "TaskBench" est un nom propre indexable. Mais "Economy" et "Premium"
sont notre jargon de tiers, pas le vocabulaire naturel d'un chercheur.

Un chercheur tapera plutôt "cheap LLM as good as expensive" ou "LLM cost
quality tradeoff." Le mot "tradeoff" ou "cost" n'apparaît pas dans le titre
actuel.

**Verdict : moyen. Manque "cost" dans le titre.**

### 1.4 Honnêteté vs marketing

Le caveat n=2 Premium est invisible dans le titre. "No Quality Gap" sur la
base de 2 Premium models est un claim que le paper lui-même qualifie
de "suggestive, not conclusive" (PAPER_STRATEGY.md). Le titre ne ment pas
mais il omet la faiblesse principale.

C'est standard en titrage académique — personne ne met les caveats dans le
titre. Mais un reviewer qui lit "No Quality Gap" puis découvre n=2 se sentira
trompé. La friction entre titre et données crée de la méfiance.

**Verdict : borderline. Acceptable si le corps est honnête, mais crée une
attente que les données ne remplissent pas entièrement.**

### 1.5 Longueur et structure

14 mots. Acceptable pour arXiv (pas de limite stricte). Mais "vs." est informel
pour un titre académique. La structure "Name: Finding Across Scope" est
classique et fonctionne.

**Verdict : OK sur la forme, "vs." à remplacer par "and" ou reformuler.**

---

## 2. Variantes proposées

### V1 — Rigoureuse

> **TaskBench: Per-Task Cost-Quality Tradeoffs Across 46 LLMs**

- **Force :** Descriptif, inattaquable. Contient "cost" (SEO). Nomme le scope.
  Ne fait aucun claim. Le lecteur sait exactement ce qu'il va lire.
- **Faiblesse :** Pas de hook. Ne dit pas ce qu'on a trouvé. Personne ne clique
  sur un titre purement descriptif sur Twitter.
- **Style :** HELM / MMLU (descriptif pur).

### V2 — Accrocheuse grand public

> **Do You Need an Expensive LLM? A 46-Model Benchmark Says Probably Not**

- **Force :** Question directe, réponse dans le titre. Provoque la curiosité.
  "Probably Not" est honnête (pas "No"). Fonctionne sur Twitter/HN.
- **Faiblesse :** Trop informel pour certains reviewers. "Says Probably Not"
  est vague. Pas de nom de benchmark en position forte.
- **Style :** FrugalGPT / blog-post.

### V3 — Scope-first avec finding

> **TaskBench: 46 Models, 21 Tasks, and a Flat Cost-Quality Curve**

- **Force :** Les chiffres (46, 21) donnent l'échelle. "Flat Cost-Quality Curve"
  est le finding structurel sans overclaim — une courbe plate n'est pas "no gap",
  c'est une observation géométrique. Contient "cost" et "quality."
- **Faiblesse :** "Flat curve" est abstrait. Moins immédiatement compréhensible
  que "no gap." Ne dit pas explicitement "cheap = good."
- **Style :** Hybride MMLU (chiffres) + finding.

### V4 — Finding rigoureux avec scope

> **TaskBench: Cheap LLMs Score Within 1% of Expensive Ones Across 21 Production Tasks**

- **Force :** Le "1%" est exact (gap 0.042 = 0.84% de l'échelle 1–5, arrondi
  à 1%). Chiffre concret, vérifiable, pas un claim statistique. "Cheap" et
  "Expensive" sont le vocabulaire naturel. "Production Tasks" signale la
  pertinence pratique.
- **Faiblesse :** "Within 1%" semble petit mais un lecteur pourrait se demander
  "1% de quoi ?" Le gap est 0.042 sur 5 points, soit 0.84% de l'échelle
  totale mais 4.2% si on mesure par rapport au gap 0–1. Le "1%" est correct
  mais ambigu. Et "Cheap" peut paraître péjoratif.
- **Style :** Finding-first concret.

### V5 — Question + nom fort

> **How Much Does LLM Quality Cost? Benchmarking 46 Models Across 21 Tasks**

- **Force :** La question est LE problème du paper. Tout praticien se la pose.
  La deuxième moitié donne le scope. Pas de claim dans le titre — le paper
  répond à la question.
- **Faiblesse :** Pas de finding. Le lecteur ne sait pas la réponse avant de
  lire. Moins de click-bait. Pas de "TaskBench" en position de nom propre.
- **Style :** Question framing (courant en économie, rare en ML).

---

## 3. Recommandation finale

**V3 : "TaskBench: 46 Models, 21 Tasks, and a Flat Cost-Quality Curve"**

Justification :

1. **Inattaquable.** "Flat curve" est une observation géométrique des données,
   pas un claim statistique. Un reviewer ne peut pas dire "votre courbe n'est
   pas plate" — il suffit de regarder Figure 3. Ce n'est pas "no gap" (claim
   d'absence) ni "Match" (claim d'équivalence).

2. **Contient "cost" et "quality."** Les deux mots-clés SEO critiques pour
   la découvrabilité.

3. **Les chiffres (46, 21) vendent le scope.** C'est ce qui différencie
   TaskBench de FrugalGPT (1 task, 3 models) ou des leaderboards à score
   unique. Le lecteur voit immédiatement "c'est gros."

4. **"Flat curve" intrigue.** Un praticien qui paie $15/M pour GPT-5.5 Pro
   voit "flat cost-quality curve" et pense "attends, je paie pour rien ?"
   C'est un hook subtil sans être click-bait.

5. **Compatible n=2.** Même avec plus de Premium models, la courbe resterait
   relativement plate (le gap max possible est <0.12 d'après les CIs).
   Le titre ne surpromet pas.

Backup : V1 pour sécurité maximale, V5 si on veut une question.
