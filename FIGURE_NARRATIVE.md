# Figure Narrative

Document vivant. Pour chaque figure : ce qu'elle prouve, comment on la decrit, ses limites, et comment elle interagit avec les autres.

Derniere mise a jour : 2026-06-12 (prices reconciled to CSV as single source of truth, all figures regenerated)

**Source de verite des prix :** `benchmark_results.csv` (cout reel au moment du benchmark). Les dicts `MODEL_PRICES` dans `analyze_v3.py` et `generate_figures.py` sont synchronises sur ces prix.

---

## Figure 1 — Heatmap (46 models x 21 tasks)

**Fichier :** `paper/figures/heatmap_v3.svg` / `.png`
**Statut review :** PASS

### Ce qu'elle prouve
La qualite est remarquablement homogene en haut du tableau. Les 10 meilleurs modeles (o3 a Seed 2.0 Pro) sont a moins de 0.05 points les uns des autres (4.79-4.84). Le veritable decrochage est en bas : Llama 1B (3.26), Llama 3B (4.15), Ministral 3B (4.43). Le spread total est de 1.58 points sur une echelle de 5.

L'heterogeneite est dans les colonnes, pas les lignes : certaines taches (intent_clinc150, multistep_reasoning, rag_qa) separent les modeles avec un spread >2.5, tandis que d'autres (structured_output: 0.29, code_explanation: 0.81) ne separent presque rien.

### Comment on la decrit dans le paper
Section Results, ouverture. La heatmap est la "vue satellite" — elle pose le paysage avant qu'on zoome. On la commente en deux temps : (1) la compression du haut (les 40 meilleurs modeles tiennent dans 0.6 point), (2) les taches qui discriminent vs celles qui ne discriminent pas. On ne fait pas de claim sur le cout ici — c'est le role des figures suivantes.

### Limites / caveats
- L'echelle 1-5 avec ceiling a 5.0 compresse les hauts scores. On ne peut pas distinguer "excellent" de "parfait".
- Les couleurs (RdYlGn) rendent bien les extremes mais ecrasent les nuances entre 4.5 et 5.0 ou se trouvent 80% des donnees.
- Le classement des lignes (par score moyen) est un choix editorial — un tri par cout ou par provider raconterait une histoire differente.

### Interaction avec les autres figures
- **Vers Fig 2 :** La compression en haut du heatmap explique pourquoi les tiers Premium/Standard/Economy sont si proches dans le bar chart (4.79/4.76/4.70). La heatmap montre que c'est reel, pas un artefact d'agregation.
- **Vers Figs 3-4 :** Les colonnes "vertes partout" (data_to_text, structured_output) correspondent aux taches saturees. Les colonnes avec du rouge/orange (rag_qa, multistep_reasoning) sont celles ou le Pareto a du relief.

---

## Figure 2 — Tier Comparison (bootstrap 95% CI)

**Fichier :** `paper/figures/tier_comparison_v3.svg` / `.png`
**Statut review :** PASS

### Ce qu'elle prouve
Premium (4.791), Standard (4.756) et Economy (4.698) sont statistiquement indistinguables — leurs CIs se chevauchent (P [4.73, 4.85], S [4.72, 4.79], E [4.67, 4.73]). Seul Micro (4.104) decroche nettement, avec un CI [3.90, 4.30] qui ne touche aucun des trois autres. Le message : **payer plus ne garantit pas une meilleure qualite en moyenne**, mais les modeles les moins chers (< $0.05/M) sont nettement en dessous.

Chiffres cles : Premium vs Economy = 0.093 points d'ecart (~2% relatif). Premium vs Micro = 0.687 points (~14% relatif).

### Comment on la decrit dans le paper
Section Results, juste apres la heatmap. C'est le premier argument quantitatif du paper : "en moyenne, les trois tiers superieurs sont equivalents." On cite les CIs, on note le chevauchement, on pose la question que les figures 3-4 vont resoudre : "si les moyennes sont plates, ou est la valeur du routage ?"

### Limites / caveats
- **Axe Y tronque a 3.8** — exagere visuellement le decrochage Micro. Defensible (les CIs sont montrees) mais un reviewer peut le signaler.
- La moyenne masque l'heterogeneite par tache. Un modele Economy peut etre meilleur qu'un Premium sur une tache specifique. La heatmap (Fig 1) le montre, mais pas cette figure.
- n par tier tres desequilibre : Premium n=42 (2 modeles x 21 taches), Economy n=483 (23 modeles x 21 taches). Les CIs refletent ca (CI Premium ~10x plus large que Standard), mais ca vaut une mention.
- Micro n=3 modeles seulement. Le CI est large [3.90, 4.30] — tire par la variance entre Llama 1B (3.26) et Qwen Turbo (4.63). Robuste sur la direction (Micro < Economy) mais pas sur la magnitude.

### Interaction avec les autres figures
- **Depuis Fig 1 :** La compression du heatmap explique les barres plates. Ce n'est pas un artefact de l'agregation — les modeles individuels sont reellement proches.
- **Vers Figs 3-4 :** "Si les moyennes sont plates, pourquoi router ?" Reponse : parce que les moyennes cachent la variation par tache. Sur RAG QA, l'ecart cout-qualite est reel. Sur data_to_text, il n'y en a pas. Le routage cree de la valeur sur les taches difficiles, pas en moyenne.
- **Vers Fig 5 :** Le provider gradient montre la meme platitude intra-provider : Anthropic couvre 19x de prix pour ~0.05 points. Coherent avec les barres plates du tier chart.

---

## Figure 3 — Pareto RAG QA

**Fichier :** `paper/figures/pareto_rag_qa.svg` / `.png`
**Statut review :** PASS WITH NOTES (caption "50 cases each" minor inaccuracy)

### Ce qu'elle prouve
Sur une tache difficile (spread 2.84, 0% a 5.0), il y a un vrai gradient cout-qualite. La frontiere Pareto monte de Llama 1B (2.0, 0.6 mc) a Sonnet 4.6 (4.84, 140 mc) en passant par 5 modeles intermediaires. Au-dela de Sonnet 4.6, on ne gagne plus rien — GPT-5.5 Pro a 954 mc est domine (score inferieur, cout superieur).

**Le chiffre cle :** Qwen Turbo atteint 95% de la qualite max a 0.6% du cout. C'est l'argument concret pour le routage.

### Comment on la decrit dans le paper
Section Results, sous-section "Task-level Pareto analysis." On la presente comme le premier des deux exemples opposes (hard task vs easy task). On cite le ratio Qwen Turbo (95% qualite, 180x moins cher que le meilleur), on nomme le point d'inflexion (Sonnet 4.6), on note que le modele le plus cher est domine.

### Limites / caveats
- C'est UN exemple de tache difficile. On ne peut pas generaliser a toutes les taches a partir d'un seul Pareto. Le choix de RAG QA est editorial — on l'a choisi parce que le spread est le plus grand des taches jugees par LLM.
- Caption dit "50 cases each" mais Llama 4 Maverick a n=45. Mineur.

### Interaction avec les autres figures
- **Avec Fig 4 :** Le contraste delibere. Ensemble, les deux figures prouvent que "la valeur du routage depend de la tache." C'est le resultat central que le paper doit nommer explicitement.
- **Depuis Fig 2 :** Les barres plates du tier chart cachent ce gradient. Fig 3 montre qu'en zoomant sur une tache, le gradient apparait.
- **Depuis Fig 1 :** La colonne rag_qa dans le heatmap est une des plus heterogenes (rouge en bas, vert en haut). Fig 3 est le zoom sur cette colonne.

---

## Figure 4 — Pareto Data-to-Text

**Fichier :** `paper/figures/pareto_data_to_text.svg` / `.png`
**Statut review :** PASS WITH NOTES (ceiling effect delibere, pas un defaut)

### Ce qu'elle prouve
Sur une tache facile (72% des modeles a 5.0, spread 1.56), le Pareto est trivial : 2 points seulement (Llama 1B a 3.44, puis Qwen Turbo a 5.0). Tous les autres modeles — y compris GPT-5.5 Pro a 1422 mc — font aussi bien que Qwen Turbo a 0.68 mc. **Payer plus n'achete rien.**

Le chiffre cle : GPT-5.5 Pro est 2092x plus cher pour le meme score.

### Comment on la decrit dans le paper
Juste apres Fig 3, comme le contraste delibere. On la presente comme "le regime oppose" : une tache ou le routage est trivial parce que le modele le moins cher suffit. On nomme le pattern : "sur les taches faciles, le cout optimal est le cout plancher."

Puis on fait la synthese des deux figures : **"La valeur du routage est proportionnelle a la difficulte de la tache."** C'est l'argument que la section routage va formaliser.

### Limites / caveats
- **Ceiling effect :** 33/46 modeles a 5.0 signifie que le judge ne distingue pas les nuances au sommet. On ne sait pas si tous ces "5.0" sont reellement equivalents ou si une echelle plus fine revelerait des differences. On le formule prudemment : "nous ne pouvons pas distinguer une saturation reelle d'une echelle trop grossiere pour detecter des differences residuelles."
- On pourrait argumenter qu'un Pareto plat n'apporte rien visuellement. Mais c'est sa platitude qui EST l'information — il faut qu'il soit la pour que le lecteur voie le contraste avec Fig 3.

### Interaction avec les autres figures
- **Avec Fig 3 :** Couple indissociable. Ne presente jamais l'un sans l'autre. L'argument est dans le contraste.
- **Vers Limitations :** La saturation de data_to_text (+ 3 autres taches : structured_output 67%, code_review 65%, sentiment 50%) doit etre discutee. 4/21 taches saturees, 14.5% de toutes les paires a 5.0. A mentionner dans Methodology ou Limitations.
- **Depuis Fig 1 :** La colonne data_to_text dans le heatmap est un mur vert. Le Pareto plat est la traduction quantitative de ce mur.

---

## Figure 5 — Provider Quality Gradient

**Fichier :** `paper/figures/provider_gradient.svg` / `.png`
**Statut review :** PASS (labels reduits aux endpoints + adjustText, prix mis a jour)

### Ce qu'elle prouve
Au sein d'un meme fournisseur, payer plus achete tres peu de qualite :
- **OpenAI :** 150x le prix (Nano $0.10 -> Pro $15), +0.13 score
- **Anthropic :** 19x le prix (Haiku $0.80 -> Opus $15), +0.05 score
- **Qwen :** 39x le prix (Turbo $0.033 -> Max $1.30), +0.12 score
- **Google :** 17x le prix (Flash $0.15 -> Pro $2.50), +0.02 score
- **Mistral** est l'exception : 50x le prix, +0.34 score (mais c'est tire par Ministral 3B a 4.43 qui est un outlier bas)

Le gradient est quasi-plat pour 4/5 providers. La conclusion : **le rendement marginal du prix est quasi-nul au-dessus du tier Economy**, meme au sein d'un provider.

### Comment on la decrit dans le paper
Section Results, apres les Pareto. C'est le troisieme angle d'attaque du meme argument : (1) les tiers sont plats (Fig 2), (2) sur une tache difficile le Pareto a une inflexion precoce (Fig 3), (3) meme au sein d'un provider, la pente prix-qualite est plate (Fig 5). Trois perspectives independantes qui convergent.

On ne cite pas les 5 providers en detail — on donne le range (17x-150x le prix, +0.02 a +0.13 de score pour 4 providers) et on note l'exception Mistral.

### Limites / caveats
- **Axe Y tronque a 4.2** — amplifie visuellement les variations. La plage reelle est 4.43-4.84, soit 0.41 points. Defensible mais a noter.
- **5 providers seulement** — les modeles de providers avec <2 modeles (ByteDance/Seed, xAI/Grok, Meta/Llama, etc.) ne sont pas montres. Ca pourrait biaiser la conclusion si ces providers ont des gradients plus raides.
- **GPT-4o est un outlier** — il dip a ~4.70 alors que GPT-5.4 a $1 fait 4.81. Un reviewer pourrait demander pourquoi un modele plus cher fait moins bien. Reponse : GPT-4o est une generation precedente, le prix ne reflete pas seulement la qualite mais aussi l'anciennete.

### Interaction avec les autres figures
- **Depuis Fig 2 :** Le tier chart montre la platitude entre tiers ; Fig 5 montre la platitude intra-provider. Meme conclusion, angle different.
- **Depuis Figs 3-4 :** Le gradient plat de Fig 5 est coherent avec le plateau post-inflexion de Fig 3 (au-dela de ~140 mc, on ne gagne plus rien) et la platitude totale de Fig 4.
- **Attention couleurs :** Vert = Mistral dans Fig 5 vs Vert = Economy dans Figs 1-4. Semantique differente, meme couleur. Pas de confusion probable (figure types differents, legendes presentes) mais a garder en tete.

---

## Synthese : l'argument du paper en 5 figures

| # | Figure | Role dans l'argument |
|---|--------|---------------------|
| 1 | Heatmap | Pose le paysage : qualite comprimee en haut, heterogeneite dans les taches |
| 2 | Tier bars | Premiere surprise : les tiers de prix ne separent pas la qualite (sauf Micro) |
| 3 | Pareto RAG QA | Zoom sur une tache difficile : le gradient cout-qualite existe, avec inflexion |
| 4 | Pareto Data-to-Text | Zoom sur une tache facile : le gradient n'existe pas, tout le monde sature |
| 5 | Provider gradient | Troisieme angle : meme intra-provider, payer plus n'achete presque rien |

**L'arc narratif :** Les 5 figures convergent vers une seule conclusion : **la qualite LLM est commoditisee au-dessus du tier Micro, et la valeur du routage vient de l'identification des taches ou l'ecart existe encore** (les taches difficiles). Le paper n'est pas "quel modele est le meilleur" — c'est "pourquoi la question n'a plus de sens sans specifier la tache."

---

## Chiffres cles a propager dans le paper

Ces chiffres doivent etre coherents partout (texte, captions, figures) :
- 46 modeles, 21 taches, ~50 cases chacun, 966 paires modele-tache
- Tier counts : Premium 2, Standard 18, Economy 23, Micro 3 (total 46)
- Tier means : Premium 4.791, Standard 4.756, Economy 4.698, Micro 4.104
- Tier CIs : P [4.73, 4.85], S [4.72, 4.79], E [4.67, 4.73], M [3.90, 4.30]
- Premium vs Economy = 0.093 pts (~2%). Premium vs Micro = 0.687 pts (~14%)
- 4/21 taches saturees (>=50% a 5.0) : data_to_text, structured_output, code_review, sentiment
- 14.5% de toutes les 966 paires scorent exactement 5.0
- RAG QA : Qwen Turbo = 95% qualite a 0.6% du cout du meilleur
- Data-to-Text : GPT-5.5 Pro est 2092x plus cher que Qwen Turbo pour le meme score
- Source de verite des prix : benchmark_results.csv

---

## Corrections appliquees (journal)

1. **Bug scorer multistep_reasoning** — eval_type="exact" faisait un substring match de lettres simples (A/B/C/D), scorant 5 si la lettre attendue apparaissait n'importe ou dans la reponse. Corrige : extraction du choix final du modele (patterns: "answer is X", **X**, lettre finale). 2756 raw results re-scores, multistep passe de la tache la plus saturee (56.5% a 5.0) a la plus discriminative (spread 3.68, 0% a 5.0).

2. **Prix reconcilies** — 20 divergences entre le dict hardcode et le CSV. Resolution : CSV = source de verite. Impact : gpt-5.4-nano et phi-4 passent de Micro a Economy, qwen-turbo passe d'Economy a Micro. Micro passe de 4 a 3 modeles, mean de 4.228 a 4.104.

3. **Millicents fix** — avg_cost * 100 -> avg_cost * 100_000 dans les Pareto (Figs 3-4).

4. **Fig 5 labels** — 29 labels -> 12 (endpoints + outliers) avec adjustText.

---

## Actions restantes

- [x] /figure-review formelle sur Fig 2
- [x] Verifier propagation du fix multistep dans Figs 1, 2, 5
- [x] Reconcilier les prix (CSV = source de verite)
- [ ] Ecrire les sections du paper en suivant l'arc narratif ci-dessus
- [ ] Ajouter le paragraphe Limitations sur la saturation (4/21, 14.5%, formulation prudente)
- [ ] Ajouter une mention du bug scorer multistep dans une note ou dans les limitations (transparence)
