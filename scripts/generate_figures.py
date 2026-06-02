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

# Canonical MODEL_PRICES — synced with analyze_v3.py
MODEL_PRICES = {
    "claude-opus-4-7": 15.0, "gpt-5.5-pro": 15.0, "claude-sonnet-4-20250514": 3.0,
    "claude-sonnet-4-6": 3.0, "gpt-4o": 2.5, "gpt-5.5": 3.0, "gpt-5.1-chat": 0.8,
    "o3": 2.0, "gemini-2.5-pro": 1.25, "gemini-3.1-pro-preview": 1.25, "MiniMax-M2.7": 1.0,
    "mistral-large-latest": 2.0, "qwen/qwen-max": 2.0, "x-ai/grok-4.20": 2.0,
    "qwen/qwen3.6-max-preview": 1.5, "kimi-k2.6": 0.6, "gpt-5.4": 1.0, "o4-mini": 1.1,
    "gpt-4o-mini": 0.15, "gemini-2.5-flash": 0.15, "mistral-small-latest": 0.1,
    "mistral-medium-latest": 0.4, "gpt-5.4-mini": 0.1, "deepseek/deepseek-v3.2": 0.14,
    "deepseek/deepseek-v4-pro": 0.435, "devstral-latest": 0.2, "x-ai/grok-4-fast": 0.2,
    "x-ai/grok-code-fast-1": 0.2, "qwen/qwen3-coder": 0.3, "qwen/qwen3.6-flash": 0.3,
    "qwen/qwen3.6-plus": 0.5, "meta-llama/llama-4-maverick": 0.2,
    "seed-2-0-pro-260328": 0.6, "seed-2-0-code-preview-260328": 0.3,
    "bytedance-seed/seed-2.0-mini": 0.15, "bytedance-seed/seed-2.0-lite": 0.075,
    "gpt-5.4-nano": 0.02, "ministral-3b-latest": 0.04, "qwen/qwen-turbo": 0.05,
    "qwen/qwen3-8b": 0.05, "bytedance-seed/seed-1.6-flash": 0.075,
    "google/gemma-4-26b-a4b-it": 0.05, "microsoft/phi-4": 0.02,
    "meta-llama/llama-3.2-1b-instruct": 0.027, "meta-llama/llama-3.2-3b-instruct": 0.051,
    "nvidia/nemotron-3-super-120b-a12b": 0.09,
    "claude-haiku-4-5-20251001": 0.8,
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

    costs = [task_data[m]["avg_cost"] * 100 for m in models]  # millicents
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
        mx = task_data[model_id]["avg_cost"] * 100
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
                expand=(2.0, 2.0), force_text=(1.5, 1.5), force_points=(2.0, 2.0),
                ensure_inside_axes=True)

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
    provider_colors = {
        "OpenAI": "#4285F4", "Anthropic": "#E8890C", "Mistral": "#2ECC71",
        "Qwen": "#E74C3C", "Google": "#9B59B6",
    }
    fig, ax = plt.subplots(figsize=(12, 7))
    total_models = 0
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
            dname = display_name(e["model"])
            ax.annotate(dname, xy=(e["price"], e["avg_score"]),
                        xytext=(5, 6), textcoords="offset points",
                        fontsize=6.5, color="#333333", zorder=4)

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
    assert tier_counts["Standard"] == 19
    assert tier_counts["Economy"] == 21
    assert tier_counts["Micro"] == 4

    print("\nGenerating all 5 paper figures:\n")

    print("Figure 1: Heatmap (46 models x 21 tasks)")
    fig_heatmap(agg)

    print("\nFigure 2: Tier Comparison (bootstrap CIs)")
    fig_tier_comparison(stats)

    print("\nFigure 3: Pareto — RAG QA")
    fig_pareto(agg, "rag_qa", "RAG QA", "pareto_rag_qa.svg", [
        "meta-llama/llama-3.2-1b-instruct",  # cheapest, lowest quality
        "qwen/qwen-turbo",                    # Pareto: huge quality jump
        "bytedance-seed/seed-2.0-mini",       # Pareto: Economy sweet spot
        "claude-sonnet-4-6",                  # Pareto winner: best quality
        "gpt-5.5-pro",                        # most expensive Premium
    ])

    print("\nFigure 4: Pareto — Data-to-Text")
    fig_pareto(agg, "data_to_text", "Data-to-Text", "pareto_data_to_text.svg", [
        "meta-llama/llama-3.2-1b-instruct",  # cheapest, lowest quality
        "qwen/qwen-turbo",                    # Pareto winner: 5.0 at near-zero cost
        "meta-llama/llama-3.2-3b-instruct",   # below 5.0 cluster
        "gpt-5.5-pro",                        # most expensive, same score
    ])

    print("\nFigure 5: Provider Gradient")
    fig_provider_gradient(pg)

    print(f"\nDone. All figures in {FIG_DIR}/ (SVG + PNG + PDF)")


if __name__ == "__main__":
    main()
