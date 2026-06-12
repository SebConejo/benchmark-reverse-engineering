#!/usr/bin/env python3
"""
TaskBench Figure Generator — all 5 paper figures.

Reads JSON analysis files from results/analysis_v3_final/ and generates
publication-quality SVG + PNG figures. Follows PARETO_STYLE_GUIDE.md and
FIGURE_QUALITY_CHECKLIST.

Usage:
    python3 scripts/generate_figures.py

Requires: numpy, matplotlib, cairosvg
"""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from collections import defaultdict

OUT_DIR = "results/analysis_v3_final"
FIG_DIR = os.path.join("paper", "figures")

V2_TASKS = [
    "sentiment_sst2", "intent_clinc150", "moderation_toxigen", "multistep_reasoning",
    "reasoning_gsm8k", "rag_qa", "code_generation", "code_review_v2", "code_explanation",
    "test_generation_v2", "function_calling", "sql_spider", "translation_enfr",
    "instruction_following", "structured_output", "extraction_hard_v2", "json_transform_v2",
    "email_summary_v2", "long_summarization", "data_to_text", "ner_extraction",
]

TASK_SHORT = {
    "sentiment_sst2": "Sentiment", "intent_clinc150": "Intent-150",
    "moderation_toxigen": "ToxiGen", "multistep_reasoning": "Multistep",
    "reasoning_gsm8k": "GSM8K", "rag_qa": "RAG QA", "code_generation": "Code Gen",
    "code_review_v2": "Code Review", "code_explanation": "Code Expl",
    "test_generation_v2": "Test Gen", "function_calling": "Func Call",
    "sql_spider": "SQL", "translation_enfr": "Translation",
    "instruction_following": "Instruct", "structured_output": "Struct Out",
    "extraction_hard_v2": "Extraction", "json_transform_v2": "JSON Trans",
    "email_summary_v2": "Email Sum", "long_summarization": "Long Sum",
    "data_to_text": "Data-Text", "ner_extraction": "NER",
}

TIER_COLOR = {"Premium": "#d62728", "Standard": "#1f77b4", "Economy": "#2ca02c", "Micro": "#ff7f0e"}
TIER_MARKER = {"Premium": "D", "Standard": "s", "Economy": "o", "Micro": "^"}

# Prices sourced from benchmark_results.csv (actual API costs at benchmark time).
# This is the single source of truth — must match analyze_v3.py exactly.
MODEL_PRICES = {
    # Premium (>= $5.00)
    "gpt-5.5-pro": 15.0, "claude-opus-4-7": 15.0,
    # Standard ($0.50 - $4.99)
    "kimi-k2.6": 0.6, "seed-2-0-pro-260328": 0.6,
    "claude-haiku-4-5-20251001": 0.8, "gpt-5.1-chat": 0.8,
    "gpt-5.4": 1.0, "qwen/qwen-max": 1.04, "o4-mini": 1.1, "MiniMax-M2.7": 1.1,
    "x-ai/grok-4.20": 1.25, "gemini-2.5-pro": 1.25, "qwen/qwen3.6-max-preview": 1.3,
    "o3": 2.0, "mistral-large-latest": 2.0,
    "gemini-3.1-pro-preview": 2.5, "gpt-4o": 2.5,
    "gpt-5.5": 3.0, "claude-sonnet-4-6": 3.0, "claude-sonnet-4-20250514": 3.0,
    # Economy ($0.05 - $0.49)
    "qwen/qwen3-8b": 0.05, "meta-llama/llama-3.2-3b-instruct": 0.051,
    "google/gemma-4-26b-a4b-it": 0.06, "microsoft/phi-4": 0.065,
    "bytedance-seed/seed-1.6-flash": 0.075,
    "gpt-5.4-nano": 0.1, "bytedance-seed/seed-2.0-mini": 0.1,
    "mistral-small-latest": 0.1, "devstral-latest": 0.1,
    "gemini-2.5-flash": 0.15, "meta-llama/llama-4-maverick": 0.15, "gpt-4o-mini": 0.15,
    "x-ai/grok-4-fast": 0.2, "x-ai/grok-code-fast-1": 0.2, "qwen/qwen3-coder": 0.22,
    "bytedance-seed/seed-2.0-lite": 0.25, "deepseek/deepseek-v3.2": 0.25,
    "qwen/qwen3.6-flash": 0.25, "seed-2-0-code-preview-260328": 0.3, "gpt-5.4-mini": 0.3,
    "qwen/qwen3.6-plus": 0.325, "mistral-medium-latest": 0.4, "deepseek/deepseek-v4-pro": 0.435,
    # Micro (< $0.05)
    "meta-llama/llama-3.2-1b-instruct": 0.027, "qwen/qwen-turbo": 0.033,
    "ministral-3b-latest": 0.04,
    # Non-complete models (included for cost lookups)
    "nvidia/nemotron-3-super-120b-a12b": 0.09,
}

DISPLAY_NAMES = {
    "claude-opus-4-7": "Claude Opus 4.7",
    "gpt-5.5-pro": "GPT-5.5 Pro",
    "gpt-5.5": "GPT-5.5",
    "gpt-5.4": "GPT-5.4",
    "gpt-5.4-mini": "GPT-5.4 Mini",
    "gpt-5.4-nano": "GPT-5.4 Nano",
    "gpt-5.1-chat": "GPT-5.1 Chat",
    "gpt-4o": "GPT-4o",
    "gpt-4o-mini": "GPT-4o Mini",
    "o3": "o3",
    "o4-mini": "o4-mini",
    "claude-sonnet-4-20250514": "Sonnet 4 (05/14)",
    "claude-sonnet-4-6": "Sonnet 4.6",
    "claude-haiku-4-5-20251001": "Haiku 4.5",
    "gemini-2.5-pro": "Gemini 2.5 Pro",
    "gemini-2.5-flash": "Gemini 2.5 Flash",
    "gemini-3.1-pro-preview": "Gemini 3.1 Pro",
    "MiniMax-M2.7": "MiniMax M2.7",
    "mistral-large-latest": "Mistral Large",
    "mistral-medium-latest": "Mistral Medium",
    "mistral-small-latest": "Mistral Small",
    "devstral-latest": "Devstral",
    "ministral-3b-latest": "Ministral 3B",
    "qwen/qwen-max": "Qwen Max",
    "qwen/qwen-turbo": "Qwen Turbo",
    "qwen/qwen3-8b": "Qwen3-8B",
    "qwen/qwen3-coder": "Qwen3 Coder",
    "qwen/qwen3.6-flash": "Qwen3.6 Flash",
    "qwen/qwen3.6-plus": "Qwen3.6 Plus",
    "qwen/qwen3.6-max-preview": "Qwen3.6 Max",
    "meta-llama/llama-3.2-1b-instruct": "Llama 1B",
    "meta-llama/llama-3.2-3b-instruct": "Llama 3B",
    "meta-llama/llama-4-maverick": "Llama 4 Maverick",
    "microsoft/phi-4": "Phi-4",
    "google/gemma-4-26b-a4b-it": "Gemma 4 26B",
    "deepseek/deepseek-v3.2": "DeepSeek V3.2",
    "deepseek/deepseek-v4-pro": "DeepSeek V4 Pro",
    "bytedance-seed/seed-2.0-mini": "Seed 2.0 Mini",
    "bytedance-seed/seed-2.0-lite": "Seed 2.0 Lite",
    "bytedance-seed/seed-1.6-flash": "Seed 1.6 Flash",
    "seed-2-0-pro-260328": "Seed 2.0 Pro",
    "seed-2-0-code-preview-260328": "Seed 2.0 Code",
    "x-ai/grok-4.20": "Grok 4.20",
    "x-ai/grok-4-fast": "Grok 4 Fast",
    "x-ai/grok-code-fast-1": "Grok Code Fast",
    "kimi-k2.6": "Kimi K2.6",
    "nvidia/nemotron-3-super-120b-a12b": "Nemotron 120B",
}


def get_tier(m):
    """Tier boundaries — must match analyze_v3.py exactly."""
    p = MODEL_PRICES.get(m, 0.5)
    if p >= 5: return "Premium"
    if p >= 0.5: return "Standard"
    if p >= 0.05: return "Economy"
    return "Micro"


def display_name(m):
    return DISPLAY_NAMES.get(m, m.split("/")[-1])


def load_json(name):
    with open(os.path.join(OUT_DIR, name)) as f:
        return json.load(f)


def get_complete_models(agg):
    """Return list of models with c==21 tasks."""
    model_task_count = defaultdict(int)
    for task in V2_TASKS:
        for model in agg.get(task, {}):
            model_task_count[model] += 1
    return [m for m, c in model_task_count.items() if c == 21]


def save_all(fig, name):
    """Save SVG to both OUT_DIR and paper/figures/, plus high-res PNG."""
    os.makedirs(FIG_DIR, exist_ok=True)
    svg_out = os.path.join(OUT_DIR, name)
    svg_paper = os.path.join(FIG_DIR, name)
    png_paper = os.path.join(FIG_DIR, name.replace(".svg", ".png"))
    pdf_paper = os.path.join(FIG_DIR, name.replace(".svg", ".pdf"))
    fig.savefig(svg_out, format="svg", dpi=150, bbox_inches="tight")
    fig.savefig(svg_paper, format="svg", dpi=150, bbox_inches="tight")
    fig.savefig(png_paper, format="png", dpi=250, bbox_inches="tight")
    fig.savefig(pdf_paper, format="pdf", bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {name} (SVG + PNG + PDF)")


def compute_pareto(costs, scores):
    """Return indices on the Pareto frontier (lower cost, higher score)."""
    pareto = []
    best = -1
    for i in sorted(range(len(costs)), key=lambda i: costs[i]):
        if scores[i] > best:
            pareto.append(i)
            best = scores[i]
    return pareto


CAPTION_TIER_TEXT = (
    "Tier colors: red = Premium (\\$5+/M), blue = Standard (\\$0.50 - \\$4.99), "
    "green = Economy (\\$0.05 - \\$0.49), orange = Micro (< \\$0.05)."
)


# =====================================================================
# Figure 1: Heatmap — 46 models x 21 tasks
# =====================================================================
def fig_heatmap(agg):
    complete = get_complete_models(agg)
    assert len(complete) == 46, f"Expected 46 complete models, got {len(complete)}"
    models = sorted(complete,
                    key=lambda m: -np.mean([agg[t][m]["avg_score"] for t in V2_TASKS]))
    matrix = np.full((len(models), len(V2_TASKS)), np.nan)
    for i, model in enumerate(models):
        for j, task in enumerate(V2_TASKS):
            matrix[i, j] = agg[task][model]["avg_score"]
    assert not np.isnan(matrix).any(), "White cells detected — data incomplete"

    tiers = [get_tier(m) for m in models]
    short_names = [display_name(m) for m in models]

    fig, ax = plt.subplots(figsize=(26, 18))
    im = ax.imshow(matrix, cmap="RdYlGn", vmin=1, vmax=5, aspect="auto")

    ax.set_xticks(range(len(V2_TASKS)))
    ax.set_xticklabels([TASK_SHORT[t] for t in V2_TASKS], rotation=45, ha="right", fontsize=10)
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels([""] * len(models))

    for i, (label, tier) in enumerate(zip(short_names, tiers)):
        ax.text(-0.7, i, label, ha="right", va="center", fontsize=9,
                color=TIER_COLOR[tier], fontweight="bold", transform=ax.transData)

    for i in range(len(models)):
        for j in range(len(V2_TASKS)):
            color = "white" if matrix[i, j] < 3 else "black"
            ax.text(j, i, f"{matrix[i,j]:.1f}", ha="center", va="center",
                    fontsize=11, color=color)

    plt.colorbar(im, ax=ax, label="Average Score (1-5)", shrink=0.4, pad=0.02)
    ax.set_title("TaskBench: Model Quality Across 21 Production Tasks",
                 fontsize=16, fontweight="bold", pad=15)
    fig.text(0.5, 0.005,
             f"46 models, 21 tasks. V2 judge (GPT-4o, correctness-focused). "
             f"Label colors indicate price tier: red = Premium (\\$5+/M), "
             f"blue = Standard (\\$0.50 - \\$4.99), green = Economy (\\$0.05 - \\$0.49), "
             f"orange = Micro (< \\$0.05).",
             ha="center", fontsize=9, color="#555555", style="italic",
             wrap=True)
    fig.tight_layout(rect=[0.10, 0.03, 1, 0.97])
    save_all(fig, "heatmap_v3.svg")


# =====================================================================
# Figure 2: Tier Comparison — bootstrap means + CIs
# =====================================================================
def fig_tier_comparison(stats):
    boot = stats["bootstrap"]
    tiers_order = ["Premium", "Standard", "Economy", "Micro"]
    colors = [TIER_COLOR[t] for t in tiers_order]
    means = [boot[t]["mean"] for t in tiers_order]
    ci_lo = [boot[t]["ci_lo"] for t in tiers_order]
    ci_hi = [boot[t]["ci_hi"] for t in tiers_order]
    ns = [boot[t]["n"] for t in tiers_order]
    yerr_lo = [means[i] - ci_lo[i] for i in range(4)]
    yerr_hi = [ci_hi[i] - means[i] for i in range(4)]

    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(range(4), means, color=colors, alpha=0.85,
                  yerr=[yerr_lo, yerr_hi], capsize=8, error_kw={"lw": 1.5})
    ax.set_xticks(range(4))
    ax.set_xticklabels([f"{t}\n(n={ns[i]})" for i, t in enumerate(tiers_order)], fontsize=11)
    ax.set_ylabel("Mean V2 Quality Score", fontsize=12)
    ax.set_title("Average Quality by Price Tier (Bootstrap 95% CI)",
                 fontsize=14, fontweight="bold")

    for i, (m, lo, hi) in enumerate(zip(means, ci_lo, ci_hi)):
        ax.text(i, m + (ci_hi[i] - m) + 0.02, f"{m:.3f}", ha="center",
                va="bottom", fontsize=10, fontweight="bold")

    ax.set_ylim(3.8, 5.1)
    ax.grid(axis="y", alpha=0.2)
    fig.text(0.5, 0.005,
             f"Bootstrap 95% CIs (1000 iterations, seed 42). n = model-task pairs per tier. "
             f"{CAPTION_TIER_TEXT}",
             ha="center", fontsize=8, color="#555555", style="italic", wrap=True)
    fig.tight_layout(rect=[0, 0.04, 1, 0.97])
    save_all(fig, "tier_comparison_v3.svg")


# =====================================================================
# Figures 3 & 4: Dual-panel Pareto (per PARETO_STYLE_GUIDE.md)
# =====================================================================
def fig_pareto(agg, task_key, task_title, out_name, label_models):
    """
    Single-panel Pareto scatter with log-scale X axis.
    Follows academic convention (HELM, FrugalGPT, RouterArena).
    label_models: list of model IDs to label (4-5 key points).
    """
    from adjustText import adjust_text

    complete = get_complete_models(agg)
    task_data = agg[task_key]
    models = [m for m in complete if m in task_data]
    assert len(models) == 46, f"Expected 46 models for {task_key}, got {len(models)}"

    costs = [task_data[m]["avg_cost"] * 100_000 for m in models]  # millicents
    scores = [task_data[m]["avg_score"] for m in models]
    tiers = [get_tier(m) for m in models]
    n_cases = task_data[models[0]]["n"]

    pareto_idx = compute_pareto(costs, scores)
    pareto_costs = [costs[i] for i in pareto_idx]
    pareto_scores = [scores[i] for i in pareto_idx]
    pareto_set = set(pareto_idx)

    fig, ax = plt.subplots(figsize=(10, 6.5))

    # Tier scatter
    for tier in ["Premium", "Standard", "Economy", "Micro"]:
        tier_xy = [(costs[i], scores[i]) for i in range(len(models)) if tiers[i] == tier]
        if not tier_xy:
            continue
        tx, ty = zip(*tier_xy)
        count = len(tier_xy)
        ax.scatter(tx, ty, c=TIER_COLOR[tier], marker=TIER_MARKER[tier],
                   s=50, alpha=0.75, zorder=3, edgecolors="#444444", linewidths=0.5,
                   label=f"{tier} (n={count})")

    # Pareto frontier line
    ax.plot(pareto_costs, pareto_scores, color="#222222", linewidth=2.5,
            alpha=0.8, zorder=2, solid_capstyle="round", label="Pareto frontier")

    # Log scale X
    ax.set_xscale("log")
    cost_min = min(costs) * 0.5
    cost_max = max(costs) * 2.0
    ax.set_xlim(cost_min, cost_max)
    y_min = min(scores) - 0.3
    ax.set_ylim(y_min, 5.2)

    ax.set_xlabel("Cost per query (millicents, log scale)", fontsize=11)
    ax.set_ylabel("Average quality score (1-5)", fontsize=11)
    ax.grid(True, alpha=0.15, which="both")
    ax.tick_params(labelsize=9)
    ax.legend(fontsize=9, loc="lower right", framealpha=0.9)

    # Labels with adjustText
    texts = []
    label_x = []
    label_y = []
    for model_id in label_models:
        if model_id not in task_data:
            continue
        mx = task_data[model_id]["avg_cost"] * 100_000
        my = task_data[model_id]["avg_score"]
        is_frontier = any(abs(costs[pi] - mx) < 1e-6 and abs(scores[pi] - my) < 1e-6
                          for pi in pareto_idx)
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
                expand=(1.2, 1.2), force_text=(0.5, 0.8), force_points=(1.0, 1.0),
                ensure_inside_axes=True, only_move={"text": "xy", "static": "xy", "explode": "xy"})

    ax.set_title(f"{task_title}: Cost vs Quality", fontsize=14, fontweight="bold", pad=12)
    fig.text(0.5, 0.005,
             f"n = 46 models, {n_cases} cases each. X-axis: log scale. "
             f"Black line: Pareto frontier. {CAPTION_TIER_TEXT}",
             ha="center", fontsize=8, color="#555555", style="italic")
    fig.tight_layout(rect=[0, 0.04, 1, 0.97])
    save_all(fig, out_name)


# =====================================================================
# Figure 5: Provider Quality Gradient
# =====================================================================
def fig_provider_gradient(pg):
    from adjustText import adjust_text

    provider_colors = {
        "OpenAI": "#4285F4", "Anthropic": "#E8890C", "Mistral": "#2ECC71",
        "Qwen": "#E74C3C", "Google": "#9B59B6",
    }
    fig, ax = plt.subplots(figsize=(12, 7))
    total_models = 0

    # Collect label candidates: cheapest and most expensive per provider,
    # plus notable outliers (o3, GPT-4o dip)
    label_set = set()
    for provider, entries in pg.items():
        if len(entries) < 2:
            continue
        sorted_entries = sorted(entries, key=lambda e: e["price"])
        label_set.add(sorted_entries[0]["model"])   # cheapest
        label_set.add(sorted_entries[-1]["model"])   # most expensive
    # Add notable points
    notable = {"o3", "gpt-4o"}
    for provider, entries in pg.items():
        for e in entries:
            if e["model"] in notable:
                label_set.add(e["model"])

    texts = []
    text_x = []
    text_y = []

    for provider, entries in pg.items():
        if len(entries) < 2:
            continue
        prices = [e["price"] for e in entries]
        scores = [e["avg_score"] for e in entries]
        color = provider_colors.get(provider, "#888888")
        ax.plot(prices, scores, "-o", color=color, label=provider,
                markersize=6, linewidth=1.8, alpha=0.85, zorder=3)
        total_models += len(entries)

        for e in entries:
            if e["model"] in label_set:
                dname = display_name(e["model"])
                text_x.append(e["price"])
                text_y.append(e["avg_score"])
                texts.append(ax.text(e["price"], e["avg_score"], dname,
                                     fontsize=7.5, color="#333333", zorder=4,
                                     bbox=dict(boxstyle="round,pad=0.12", fc="white",
                                               ec="#cccccc", lw=0.3, alpha=0.88)))

    adjust_text(texts, x=text_x, y=text_y, ax=ax,
                arrowprops=dict(arrowstyle="-|>", color="#555555", lw=0.6),
                expand=(1.3, 1.3), force_text=(0.6, 0.8), force_points=(1.0, 1.0),
                ensure_inside_axes=True)

    ax.set_xscale("log")
    ax.set_xlabel("Input price ($/M tokens, log scale)", fontsize=11)
    ax.set_ylabel("Average V2 quality score (1-5)", fontsize=11)
    ax.set_title("Provider Quality Gradient: Does Paying More Buy Quality?",
                 fontsize=14, fontweight="bold")
    ax.legend(fontsize=9, loc="lower right", framealpha=0.9)
    ax.grid(True, alpha=0.15)
    ax.tick_params(labelsize=9)
    ax.set_ylim(4.2, 5.0)
    fig.text(0.5, 0.005,
             f"Average across 21 production tasks. V2 judge (GPT-4o, correctness-focused). "
             f"{len(pg)} providers shown ({total_models} models).",
             ha="center", fontsize=8, color="#555555", style="italic")
    fig.tight_layout(rect=[0, 0.03, 1, 0.97])
    save_all(fig, "provider_gradient.svg")


# =====================================================================
# Figure 6: Task Discriminativeness (bar chart)
# =====================================================================
def fig_task_discriminativeness(disc):
    tasks_sorted = sorted(disc.items(), key=lambda x: x[1]["spread"], reverse=True)
    names = [TASK_SHORT.get(t, t) for t, _ in tasks_sorted]
    spreads = [d["spread"] for _, d in tasks_sorted]
    stds = [d["std"] for _, d in tasks_sorted]

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ["#d62728" if s >= 2.0 else "#1f77b4" if s >= 1.0 else "#2ca02c" for s in spreads]
    bars = ax.bar(range(len(names)), spreads, color=colors, alpha=0.85, edgecolor="#444444", linewidth=0.5)

    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha="right", fontsize=9)
    ax.set_ylabel("Score spread (max - min)", fontsize=11)
    ax.set_title("Task Discriminativeness: Which Tasks Separate Models?",
                 fontsize=14, fontweight="bold")
    ax.grid(axis="y", alpha=0.2)
    ax.axhline(y=1.0, color="#888888", linestyle="--", linewidth=0.8, alpha=0.5)

    # Annotate spread values on top of bars
    for i, (s, std) in enumerate(zip(spreads, stds)):
        ax.text(i, s + 0.05, f"{s:.1f}", ha="center", va="bottom", fontsize=7.5, fontweight="bold")

    fig.text(0.5, 0.005,
             "Spread = max score - min score across 46 complete models. "
             "Red: spread >= 2.0 (highly discriminative). Blue: 1.0-2.0. Green: < 1.0 (saturated).",
             ha="center", fontsize=8, color="#555555", style="italic")
    fig.tight_layout(rect=[0, 0.04, 1, 0.97])
    save_all(fig, "task_discriminativeness.svg")


# =====================================================================
# Figure 7: Origin Comparison (Chinese / American / European)
# =====================================================================
def fig_origin_comparison(origin):
    origins = ["Chinese", "American", "European"]
    means = [origin[o]["avg"] for o in origins]
    ns = [origin[o]["n"] for o in origins]

    # Use bootstrap CIs instead of min-max to avoid Llama 1B distortion
    # Approximate CI from std: we don't have raw values here, so use min-max
    # but clip to reasonable range
    mins = [origin[o]["min"] for o in origins]
    maxs = [origin[o]["max"] for o in origins]

    # Use std-based error bars (1.96 * std/sqrt(n)) if we can approximate
    # Since we don't have std, use interquartile-like range: show ±(max-min)/4
    yerr = [(ma - mi) / 4 for mi, ma in zip(mins, maxs)]

    colors = ["#E74C3C", "#4285F4", "#2ECC71"]
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(range(3), means, color=colors, alpha=0.85,
                  yerr=yerr, capsize=8, error_kw={"lw": 1.5})
    ax.set_xticks(range(3))
    ax.set_xticklabels([f"{o}\n(n={ns[i]})" for i, o in enumerate(origins)], fontsize=11)
    ax.set_ylabel("Mean V2 Quality Score", fontsize=12)
    ax.set_title("Quality by Provider Origin", fontsize=14, fontweight="bold")

    for i, m in enumerate(means):
        ax.text(i, m + yerr[i] + 0.02, f"{m:.3f}", ha="center", va="bottom",
                fontsize=10, fontweight="bold")

    # Add pairwise test results
    pw = origin.get("pairwise_tests", {})
    notes = []
    for key, data in pw.items():
        if isinstance(data, dict) and "p" in data:
            sig = "p < 0.05" if data["p"] < 0.05 else f"p = {data['p']:.3f}"
            notes.append(f"{key}: {sig}")
    note_text = ". ".join(notes) if notes else ""

    ax.set_ylim(4.2, 5.1)
    ax.grid(axis="y", alpha=0.2)
    fig.text(0.5, 0.005,
             f"Average quality across 21 tasks, 46 complete models. "
             f"Error bars: +/- (range/4). {note_text}",
             ha="center", fontsize=8, color="#555555", style="italic", wrap=True)
    fig.tight_layout(rect=[0, 0.04, 1, 0.97])
    save_all(fig, "origin_comparison.svg")


# =====================================================================
# Figure 8: License Comparison (open vs proprietary)
# =====================================================================
def fig_license_comparison(lic):
    categories = [c for c in ["open", "closed", "proprietary"] if c in lic]
    cat_labels = {"open": "Open-weight", "closed": "Proprietary", "proprietary": "Proprietary"}
    colors_map = {"open": "#2ECC71", "closed": "#E74C3C", "proprietary": "#E74C3C"}

    fig, ax = plt.subplots(figsize=(7, 6))
    for i, cat in enumerate(categories):
        data = lic[cat]
        ax.bar(i, data["avg"], color=colors_map[cat], alpha=0.85,
               edgecolor="#444444", linewidth=0.5)
        ax.text(i, data["avg"] + 0.02, f"{data['avg']:.3f}", ha="center", va="bottom",
                fontsize=10, fontweight="bold")

    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels([f"{cat_labels[c]}\n(n={lic[c]['n']})" for c in categories], fontsize=11)
    ax.set_ylabel("Mean V2 Quality Score", fontsize=12)
    ax.set_title("Quality by License Type", fontsize=14, fontweight="bold")

    # Add test result if available
    mw_p = lic.get("mann_whitney_p")
    test_note = ""
    if mw_p is not None:
        sig = "significant" if mw_p < 0.05 else "not significant"
        test_note = f"Mann-Whitney U: p = {mw_p:.4f} ({sig})."

    ax.set_ylim(3.8, 5.1)
    ax.grid(axis="y", alpha=0.2)
    fig.text(0.5, 0.005,
             f"Average quality across 21 tasks. {test_note}",
             ha="center", fontsize=8, color="#555555", style="italic")
    fig.tight_layout(rect=[0, 0.04, 1, 0.97])
    save_all(fig, "license_comparison.svg")


# =====================================================================
# Figure 9: Generational Delta
# =====================================================================
def fig_generational_delta(gen):
    pairs = list(gen.items())
    pair_labels = [k for k, _ in pairs]
    deltas = [v["avg_quality_delta"] for _, v in pairs]
    price_changes = [v["price_change_pct"] for _, v in pairs]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    x = range(len(pairs))
    bars = ax1.bar(x, deltas, color=["#2ca02c" if d > 0 else "#d62728" for d in deltas],
                   alpha=0.85, edgecolor="#444444", linewidth=0.5, label="Quality delta")
    ax1.set_ylabel("Quality delta (new - old)", fontsize=11, color="#333333")
    ax1.axhline(y=0, color="#888888", linewidth=0.8)
    ax1.set_xticks(x)
    ax1.set_xticklabels(pair_labels, rotation=30, ha="right", fontsize=9)
    ax1.grid(axis="y", alpha=0.2)

    # Annotate delta values
    for i, d in enumerate(deltas):
        ax1.text(i, d + 0.005 if d >= 0 else d - 0.015, f"{d:+.3f}",
                 ha="center", va="bottom" if d >= 0 else "top", fontsize=8, fontweight="bold")

    # Secondary axis for price change
    ax2 = ax1.twinx()
    ax2.plot(x, price_changes, "D-", color="#9B59B6", markersize=8, linewidth=1.5,
             alpha=0.8, label="Price change %")
    ax2.set_ylabel("Price change (%)", fontsize=11, color="#9B59B6")
    ax2.tick_params(axis="y", labelcolor="#9B59B6")

    # Annotate price changes
    for i, p in enumerate(price_changes):
        ax2.text(i, p + 3, f"{p:+d}%", ha="center", va="bottom", fontsize=7.5,
                 color="#9B59B6", fontweight="bold")

    ax1.set_title("Generational Delta: Newer Models vs Predecessors",
                  fontsize=14, fontweight="bold")
    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc="upper left")

    fig.text(0.5, 0.005,
             "Quality delta = average score difference across 21 tasks (new model - predecessor). "
             "Price change = input price change (%).",
             ha="center", fontsize=8, color="#555555", style="italic")
    fig.tight_layout(rect=[0, 0.04, 1, 0.97])
    save_all(fig, "generational_delta.svg")


# =====================================================================
# Figure 10: Per-Task Routing Savings
# =====================================================================
def fig_per_task_routing_savings(routing):
    tasks_sorted = sorted(routing.items(), key=lambda x: x[1]["savings_pct"], reverse=True)
    names = [TASK_SHORT.get(t, t) for t, _ in tasks_sorted]
    savings = [d["savings_pct"] for _, d in tasks_sorted]

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ["#2ca02c" if s >= 95 else "#1f77b4" if s >= 80 else "#ff7f0e" for s in savings]
    ax.barh(range(len(names)), savings, color=colors, alpha=0.85,
            edgecolor="#444444", linewidth=0.5)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel("Cost savings vs o3 (%)", fontsize=11)
    ax.set_title("Per-Task Routing Savings: Cheapest Model with Score >= 4.5",
                 fontsize=14, fontweight="bold")
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.2)
    ax.set_xlim(0, 105)

    for i, s in enumerate(savings):
        cheapest = tasks_sorted[i][1]["cheapest_model"]
        dname = display_name(cheapest)
        ax.text(s + 0.5, i, f"{s:.1f}% ({dname})", va="center", fontsize=7.5)

    fig.text(0.5, 0.005,
             "Savings = 1 - (cheapest qualifying model cost / o3 cost). "
             "Qualifying = avg score >= 4.5 on that task.",
             ha="center", fontsize=8, color="#555555", style="italic")
    fig.tight_layout(rect=[0, 0.04, 1, 0.97])
    save_all(fig, "per_task_routing_savings.svg")


# =====================================================================
# Figure 11: Verbosity vs Quality Delta Scatter
# =====================================================================
def fig_verbosity_scatter(verb, agg):
    # Need to reconstruct per-model verbosity data
    # verb only has summary stats (r, p, n). We need raw points.
    # Read from raw files if available, otherwise just plot the summary stat.
    import glob
    model_verbosity = {}
    raw_dir = "results/raw"

    # Calculate avg tokens per model
    complete = get_complete_models(agg)
    model_tokens = defaultdict(list)
    for task in V2_TASKS:
        for f in glob.glob(os.path.join(raw_dir, f"{task}_*_*.json")):
            try:
                with open(f) as fh:
                    d = json.load(fh)
                m = d.get("model", "")
                if m in complete and "tokens" in d:
                    tok = d["tokens"]
                    out_tok = tok.get("output", tok.get("completion_tokens", 0))
                    model_tokens[m].append(out_tok)
            except:
                pass

    if not model_tokens:
        # Fallback: just create a text figure with the summary stat
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, f"Verbosity correlation: r = {verb['r_verbosity_vs_delta']:.3f}, "
                f"p = {verb['p_verbosity_vs_delta']:.4f}\n(n = {verb['n_models']} models)",
                ha="center", va="center", fontsize=14, transform=ax.transAxes)
        ax.set_title("Verbosity vs Quality: Correlation Summary", fontsize=14, fontweight="bold")
        ax.axis("off")
        save_all(fig, "verbosity_scatter.svg")
        return

    # We have raw tokens — build scatter
    model_avg_tokens = {m: np.mean(toks) for m, toks in model_tokens.items() if len(toks) >= 100}

    # Compute quality delta from mean (deviation from grand mean)
    grand_mean = np.mean([np.mean([agg[t][m]["avg_score"] for t in V2_TASKS]) for m in complete])
    points = []
    for m in complete:
        if m not in model_avg_tokens:
            continue
        score = np.mean([agg[t][m]["avg_score"] for t in V2_TASKS])
        points.append((model_avg_tokens[m], score - grand_mean, m))

    if len(points) < 5:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, f"Verbosity correlation: r = {verb['r_verbosity_vs_delta']:.3f}, "
                f"p = {verb['p_verbosity_vs_delta']:.4f}\n(n = {verb['n_models']} models)",
                ha="center", va="center", fontsize=14, transform=ax.transAxes)
        ax.set_title("Verbosity vs Quality: Correlation Summary", fontsize=14, fontweight="bold")
        ax.axis("off")
        save_all(fig, "verbosity_scatter.svg")
        return

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    fig, ax = plt.subplots(figsize=(10, 7))
    tiers_pts = [get_tier(p[2]) for p in points]
    for tier in ["Premium", "Standard", "Economy", "Micro"]:
        tx = [xs[i] for i in range(len(points)) if tiers_pts[i] == tier]
        ty = [ys[i] for i in range(len(points)) if tiers_pts[i] == tier]
        if tx:
            ax.scatter(tx, ty, c=TIER_COLOR[tier], marker=TIER_MARKER[tier],
                       s=50, alpha=0.75, label=tier, edgecolors="#444444", linewidths=0.5)

    # Trend line
    z = np.polyfit(xs, ys, 1)
    xline = np.linspace(min(xs), max(xs), 100)
    ax.plot(xline, np.polyval(z, xline), "--", color="#888888", linewidth=1, alpha=0.7)

    r = verb["r_verbosity_vs_delta"]
    p = verb["p_verbosity_vs_delta"]
    ax.set_xlabel("Average output tokens per response", fontsize=11)
    ax.set_ylabel("Quality delta from grand mean", fontsize=11)
    ax.set_title("Verbosity vs Quality Delta", fontsize=14, fontweight="bold")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.15)
    ax.axhline(y=0, color="#888888", linewidth=0.8, linestyle="--")

    sig = "significant" if p < 0.05 else "not significant"
    fig.text(0.5, 0.005,
             f"Pearson r = {r:.3f}, p = {p:.4f} ({sig}). n = {len(points)} models. "
             "Dashed line: linear fit.",
             ha="center", fontsize=8, color="#555555", style="italic")
    fig.tight_layout(rect=[0, 0.04, 1, 0.97])
    save_all(fig, "verbosity_scatter.svg")


# =====================================================================
# Figures 12-13: Judge V1→V2 Scatter Plots
# =====================================================================
def fig_judge_validation_scatter(data, title, metric_label, out_name):
    """Scatter plot of V1 judge score vs external metric, showing correlation."""
    fig, ax = plt.subplots(figsize=(8, 6))

    r_val = data.get("r", 0)
    p_val = data.get("p", 0)
    n_val = data.get("n", 0)

    ax.text(0.5, 0.6,
            f"Pearson r = {r_val:.4f}\np = {p_val:.6f}\nn = {n_val} models",
            ha="center", va="center", fontsize=16, fontweight="bold",
            transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.5", fc="#f0f0f0", ec="#cccccc"))

    # Error breakdown if available
    eb = data.get("error_breakdown", {})
    if eb:
        eb_text = "Error breakdown: " + ", ".join(f"{k}: {v}" for k, v in eb.items())
        ax.text(0.5, 0.3, eb_text, ha="center", va="center", fontsize=10,
                transform=ax.transAxes, color="#555555")

    sig = "significant" if p_val < 0.05 else "not significant"
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.axis("off")

    pop_note = " (includes incomplete models)" if n_val != 46 else ""
    fig.text(0.5, 0.005,
             f"Correlation between V2 judge scores and {metric_label}. "
             f"r = {r_val:.3f} ({sig}). n = {n_val} models{pop_note}.",
             ha="center", fontsize=8, color="#555555", style="italic")
    fig.tight_layout(rect=[0, 0.04, 1, 0.97])
    save_all(fig, out_name)


# =====================================================================
# Figures 14-32: Per-Task Pareto Frontiers (Appendix)
# =====================================================================
def fig_pareto_appendix(agg, task_key, task_title, out_name):
    """Simplified Pareto figure for appendix — auto-selects labels."""
    from adjustText import adjust_text

    complete = get_complete_models(agg)
    task_data = agg[task_key]
    models = [m for m in complete if m in task_data]

    costs = [task_data[m]["avg_cost"] * 100_000 for m in models]  # millicents
    scores = [task_data[m]["avg_score"] for m in models]
    tiers = [get_tier(m) for m in models]
    n_cases = task_data[models[0]]["n"]

    pareto_idx = compute_pareto(costs, scores)
    pareto_costs = [costs[i] for i in pareto_idx]
    pareto_scores = [scores[i] for i in pareto_idx]

    fig, ax = plt.subplots(figsize=(10, 6.5))

    # Tier scatter
    for tier in ["Premium", "Standard", "Economy", "Micro"]:
        tier_xy = [(costs[i], scores[i]) for i in range(len(models)) if tiers[i] == tier]
        if not tier_xy:
            continue
        tx, ty = zip(*tier_xy)
        ax.scatter(tx, ty, c=TIER_COLOR[tier], marker=TIER_MARKER[tier],
                   s=50, alpha=0.75, zorder=3, edgecolors="#444444", linewidths=0.5,
                   label=f"{tier} (n={len(tier_xy)})")

    # Pareto frontier line
    ax.plot(pareto_costs, pareto_scores, color="#222222", linewidth=2.5,
            alpha=0.8, zorder=2, solid_capstyle="round", label="Pareto frontier")

    ax.set_xscale("log")
    cost_min = min(costs) * 0.5
    cost_max = max(costs) * 2.0
    ax.set_xlim(cost_min, cost_max)
    y_min = min(scores) - 0.3
    ax.set_ylim(y_min, 5.2)

    ax.set_xlabel("Cost per query (millicents, log scale)", fontsize=11)
    ax.set_ylabel("Average quality score (1-5)", fontsize=11)
    ax.grid(True, alpha=0.15, which="both")
    ax.tick_params(labelsize=9)
    ax.legend(fontsize=9, loc="lower right", framealpha=0.9)

    # Auto-select labels: cheapest, most expensive, best quality, worst quality,
    # plus first/last Pareto point
    label_models = set()
    scored = sorted(range(len(models)), key=lambda i: scores[i])
    label_models.add(models[scored[0]])    # worst quality
    label_models.add(models[scored[-1]])   # best quality
    costed = sorted(range(len(models)), key=lambda i: costs[i])
    label_models.add(models[costed[0]])    # cheapest
    label_models.add(models[costed[-1]])   # most expensive
    if pareto_idx:
        label_models.add(models[pareto_idx[0]])   # first Pareto
        label_models.add(models[pareto_idx[-1]])   # last Pareto

    texts = []
    label_x = []
    label_y = []
    for model_id in label_models:
        mx = task_data[model_id]["avg_cost"] * 100_000
        my = task_data[model_id]["avg_score"]
        is_frontier = any(abs(costs[pi] - mx) < 1e-6 for pi in pareto_idx)
        label_x.append(mx)
        label_y.append(my)
        texts.append(ax.text(mx, my, display_name(model_id),
                             fontsize=8,
                             fontweight="bold" if is_frontier else "normal",
                             color="#222222", zorder=12,
                             bbox=dict(boxstyle="round,pad=0.15", fc="white",
                                       ec="#bbbbbb", lw=0.4, alpha=0.92)))

    if texts:
        adjust_text(texts, x=label_x, y=label_y, ax=ax,
                    arrowprops=dict(arrowstyle="-|>", color="#555555", lw=0.8),
                    expand=(1.2, 1.2), force_text=(0.5, 0.8), force_points=(1.0, 1.0),
                    ensure_inside_axes=True)

    ax.set_title(f"{task_title}: Cost vs Quality", fontsize=14, fontweight="bold", pad=12)
    fig.text(0.5, 0.005,
             f"n = 46 models, {n_cases} cases each. X-axis: log scale. "
             f"Black line: Pareto frontier. {CAPTION_TIER_TEXT}",
             ha="center", fontsize=8, color="#555555", style="italic")
    fig.tight_layout(rect=[0, 0.04, 1, 0.97])
    save_all(fig, out_name)


# =====================================================================
# Main
# =====================================================================
def main():
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print("Loading analysis data...")
    agg = load_json("task_model_aggregates.json")
    stats = load_json("stats_validation.json")
    pg = load_json("provider_gradient.json")

    complete = get_complete_models(agg)
    print(f"Complete models (c==21): {len(complete)}")
    assert len(complete) == 46, f"Expected 46, got {len(complete)}"

    # Verify tier counts
    tier_counts = defaultdict(int)
    for m in complete:
        tier_counts[get_tier(m)] += 1
    print(f"Tier counts: {dict(tier_counts)}")
    assert tier_counts["Premium"] == 2
    assert tier_counts["Standard"] == 18
    assert tier_counts["Economy"] == 23
    assert tier_counts["Micro"] == 3

    print("\n=== MAIN PAPER FIGURES (1-5) ===\n")

    print("Figure 1: Heatmap (46 models x 21 tasks)")
    fig_heatmap(agg)

    print("\nFigure 2: Tier Comparison (bootstrap CIs)")
    fig_tier_comparison(stats)

    print("\nFigure 3: Pareto — RAG QA")
    fig_pareto(agg, "rag_qa", "RAG QA", "pareto_rag_qa.svg", [
        "meta-llama/llama-3.2-1b-instruct",
        "qwen/qwen-turbo",
        "bytedance-seed/seed-2.0-mini",
        "claude-sonnet-4-6",
        "gpt-5.5-pro",
    ])

    print("\nFigure 4: Pareto — Data-to-Text")
    fig_pareto(agg, "data_to_text", "Data-to-Text", "pareto_data_to_text.svg", [
        "meta-llama/llama-3.2-1b-instruct",
        "qwen/qwen-turbo",
        "meta-llama/llama-3.2-3b-instruct",
        "gpt-5.5-pro",
    ])

    print("\nFigure 5: Provider Gradient")
    fig_provider_gradient(pg)

    print("\n=== SUPPLEMENTARY FIGURES (6-13) ===\n")

    print("Figure 6: Task Discriminativeness")
    disc = load_json("task_discriminativeness.json")
    fig_task_discriminativeness(disc)

    print("\nFigure 7: Origin Comparison")
    origin = load_json("origin_comparison.json")
    fig_origin_comparison(origin)

    print("\nFigure 8: License Comparison")
    lic = load_json("license_comparison.json")
    fig_license_comparison(lic)

    print("\nFigure 9: Generational Delta")
    gen = load_json("generational_delta.json")
    fig_generational_delta(gen)

    print("\nFigure 10: Per-Task Routing Savings")
    routing = load_json("per_task_routing_savings.json")
    fig_per_task_routing_savings(routing)

    print("\nFigure 11: Verbosity Scatter")
    verb = load_json("verbosity_correlation.json")
    fig_verbosity_scatter(verb, agg)

    print("\nFigure 12: Judge V2 Validation — Code (HumanEval)")
    code_v4 = load_json("judge_v2_validation_code_v4.json")
    fig_judge_validation_scatter(code_v4,
        "Judge V2 vs HumanEval pass@1",
        "HumanEval pass@1 (automated execution)",
        "judge_v2_code.svg")

    print("\nFigure 13: Judge V2 Validation — Translation (BLEU)")
    trans = load_json("judge_v2_validation_translation.json")
    trans_data = trans.get("translation_enfr", trans)
    fig_judge_validation_scatter(trans_data,
        "Judge V2 vs BLEU Score (EN→FR Translation)",
        "corpus BLEU (sacrebleu)",
        "judge_v2_translation.svg")

    print("\n=== APPENDIX PARETO FIGURES (14-32) ===\n")

    # Generate Pareto for all 19 remaining tasks (not rag_qa or data_to_text)
    done_tasks = {"rag_qa", "data_to_text"}
    appendix_tasks = [t for t in V2_TASKS if t not in done_tasks]
    for i, task in enumerate(appendix_tasks):
        short = TASK_SHORT.get(task, task)
        print(f"Figure {14+i}: Pareto — {short}")
        fig_pareto_appendix(agg, task, short, f"pareto_{task}.svg")

    print(f"\nDone. All figures in {FIG_DIR}/ (SVG + PNG + PDF)")


if __name__ == "__main__":
    main()
