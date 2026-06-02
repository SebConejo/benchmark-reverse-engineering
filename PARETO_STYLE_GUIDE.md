# Pareto Figure Style Guide

**Validated on:** RAG QA + Data-to-Text, 2026-06-02
**Format:** Single-panel, log-scale X axis (academic convention: HELM, FrugalGPT, RouterArena)

This document defines the exact visual style for all TaskBench Pareto scatter
plots. A new session MUST follow this guide to produce consistent figures.

---

## Layout: Single Panel, Log-Scale X

One panel per figure. X-axis in log scale spans the full cost range.

```python
fig, ax = plt.subplots(figsize=(10, 6.5))
ax.set_xscale("log")

cost_min = min(costs) * 0.5
cost_max = max(costs) * 2.0
ax.set_xlim(cost_min, cost_max)
ax.set_ylim(min(scores) - 0.3, 5.2)
```

- Log scale naturally separates the dense low-cost cluster from expensive outliers.
- No need for dual panels or zoom rectangles.
- Follows the convention used by HELM, FrugalGPT, and RouterArena.

---

## Points

| Tier | Color | Marker | Hex |
|------|-------|--------|-----|
| Premium | Red | Diamond `D` | `#d62728` |
| Standard | Blue | Square `s` | `#1f77b4` |
| Economy | Green | Circle `o` | `#2ca02c` |
| Micro | Orange | Triangle `^` | `#ff7f0e` |

```python
TIER_COLOR = {'Premium': '#d62728', 'Standard': '#1f77b4', 'Economy': '#2ca02c', 'Micro': '#ff7f0e'}
TIER_MARKER = {'Premium': 'D', 'Standard': 's', 'Economy': 'o', 'Micro': '^'}
```

Point size: `s=50`. Edge: `edgecolors='#444444', linewidths=0.5`. Alpha: `0.75`.

```python
ax.scatter(x, y, c=TIER_COLOR[tier], marker=TIER_MARKER[tier],
           s=50, alpha=0.75, zorder=3, edgecolors='#444444', linewidths=0.5,
           label=f'{tier} (n={count})')
```

---

## Pareto Frontier Line

**Color: black** (`#222222`). **Solid line**, not dashed. **Width: 2.5**.

```python
ax.plot(pareto_costs, pareto_scores,
        color='#222222', linewidth=2.5, alpha=0.8, zorder=2,
        solid_capstyle='round', label='Pareto frontier')
```

The frontier is computed as: sort by cost ascending, keep only points where
score strictly increases.

```python
def compute_pareto(costs, scores):
    pareto = []
    best = -1
    for i in sorted(range(len(costs)), key=lambda i: costs[i]):
        if scores[i] > best:
            pareto.append(i)
            best = scores[i]
    return pareto
```

---

## Labels: adjustText (mandatory)

Use the `adjustText` library for automatic label placement. Manual offsets
are prohibited (they broke on every data change and caused overlaps).

### Rules

1. **4-5 labels per figure.** More creates clutter.
2. **adjustText handles placement.** No manual `xytext` offsets.
3. **Every label has an arrow** pointing to its exact data point.
4. **No label covers a data point.** adjustText's `force_points` enforces this.
5. **Cross-check each label's coordinates against the source JSON** before shipping.

### Which models to label

- **Pareto extremes:** cheapest Pareto point, highest-quality Pareto point
- **Pareto intermediate:** one Economy sweet-spot on the frontier
- **Cost extremes:** most expensive model (usually Premium)
- **Quality extremes:** lowest-quality model (usually Llama 1B)

Before labeling, list the 4-5 candidates and justify each choice. This list
goes in the spot-check table when presenting the figure.

### Label style

```python
from adjustText import adjust_text

texts = []
label_x, label_y = [], []
for model_id in label_models:
    mx = task_data[model_id]["avg_cost"] * 100
    my = task_data[model_id]["avg_score"]
    is_frontier = model_id in pareto_set
    label_x.append(mx)
    label_y.append(my)
    texts.append(ax.text(mx, my, display_name(model_id),
                         fontsize=8.5,
                         fontweight="bold" if is_frontier else "normal",
                         color="#222222", zorder=12,
                         bbox=dict(boxstyle="round,pad=0.15", fc="white",
                                   ec="#bbbbbb", lw=0.4, alpha=0.92)))

adjust_text(texts, x=label_x, y=label_y, ax=ax,
            arrowprops=dict(arrowstyle="-|>", color="#555555", lw=0.8),
            expand=(2.0, 2.0), force_text=(1.5, 1.5), force_points=(2.0, 2.0),
            ensure_inside_axes=True)
```

Bold for Pareto-frontier models. Normal weight for non-frontier.

---

## Legend

Position: `loc='lower right'`. `framealpha=0.9`, `fontsize=9`.

```python
ax.legend(fontsize=9, loc='lower right', framealpha=0.9)
```

---

## Title and Caption

**Title:**
```python
ax.set_title(f'{task_title}: Cost vs Quality', fontsize=14, fontweight='bold', pad=12)
```

**Caption** (below the figure):
```python
fig.text(0.5, 0.005,
    f'n = {n} models, {n_cases} cases each. X-axis: log scale. '
    f'Black line: Pareto frontier. {CAPTION_TIER_TEXT}',
    ha='center', fontsize=8, color='#555555', style='italic')
```

**Axes:**
```python
ax.set_xlabel('Cost per query (millicents, log scale)', fontsize=11)
ax.set_ylabel('Average quality score (1-5)', fontsize=11)
```

**Caption typography (check 15):** every `$` sign must be escaped as `\$`
in matplotlib text to avoid LaTeX math mode interpretation.

---

## Grid and Ticks

```python
ax.grid(True, alpha=0.15, which="both")  # both major and minor for log scale
ax.tick_params(labelsize=9)
```

---

## Tight Layout

```python
fig.tight_layout(rect=[0, 0.04, 1, 0.97])
```

---

## Display Names

Use human-readable model names, not API IDs:

```python
DISPLAY_NAMES = {
    'claude-opus-4-7': 'Claude Opus 4.7',
    'gpt-5.5-pro': 'GPT-5.5 Pro',
    'gpt-4o-mini': 'GPT-4o Mini',
    'qwen/qwen-turbo': 'Qwen Turbo',
    'qwen/qwen3-8b': 'Qwen3-8B',
    'meta-llama/llama-3.2-1b-instruct': 'Llama 1B',
    'meta-llama/llama-3.2-3b-instruct': 'Llama 3B',
    'bytedance-seed/seed-2.0-mini': 'Seed 2.0 Mini',
    'claude-sonnet-4-6': 'Sonnet 4.6',
    # ... see generate_figures.py for full dict
}
```

---

## Tier Boundaries

| Tier | Input price/M tokens |
|------|---------------------|
| Premium | >= $5.00 |
| Standard | $0.50 - $4.99 |
| Economy | $0.05 - $0.49 |
| Micro | < $0.05 |
