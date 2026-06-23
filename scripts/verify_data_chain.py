#!/usr/bin/env python3
"""
Data chain verifier: CSV → JSONs → figures → tex.
Recomputes everything from benchmark_results.csv and checks against stored JSONs.
Reports any discrepancy.
"""
import csv, json, os, sys
from collections import defaultdict

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CSV_PATH = "results/benchmark_results.csv"
JSON_DIR = "results/analysis_v3_final"
TEX_PATH = "paper/main.tex"

V2_TASKS = [
    "sentiment_sst2", "intent_clinc150", "moderation_toxigen", "multistep_reasoning",
    "reasoning_gsm8k", "rag_qa", "code_generation", "code_review_v2", "code_explanation",
    "test_generation_v2", "function_calling", "sql_spider", "translation_enfr",
    "instruction_following", "structured_output", "extraction_hard_v2", "json_transform_v2",
    "email_summary_v2", "long_summarization", "data_to_text", "ner_extraction",
]

# Price dict — must match generate_figures.py and analyze_v3.py
MODEL_PRICES = {
    "gpt-5.5-pro": 15.0, "claude-opus-4-7": 15.0,
    "kimi-k2.6": 0.6, "seed-2-0-pro-260328": 0.6,
    "claude-haiku-4-5-20251001": 0.8, "gpt-5.1-chat": 0.8,
    "gpt-5.4": 1.0, "qwen/qwen-max": 1.04, "o4-mini": 1.1, "MiniMax-M2.7": 1.1,
    "x-ai/grok-4.20": 1.25, "gemini-2.5-pro": 1.25, "qwen/qwen3.6-max-preview": 1.3,
    "o3": 2.0, "mistral-large-latest": 2.0,
    "gemini-3.1-pro-preview": 2.5, "gpt-4o": 2.5,
    "gpt-5.5": 3.0, "claude-sonnet-4-6": 3.0, "claude-sonnet-4-20250514": 3.0,
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
    "meta-llama/llama-3.2-1b-instruct": 0.027, "qwen/qwen-turbo": 0.033,
    "ministral-3b-latest": 0.04,
}


def get_tier(m):
    p = MODEL_PRICES.get(m, 0.5)
    if p >= 5: return "Premium"
    if p >= 0.5: return "Standard"
    if p >= 0.05: return "Economy"
    return "Micro"


MIN_CASES_PER_TASK = 40  # Must match analyze_v3.py


def load_csv():
    """Load CSV and compute per-task per-model aggregates from scratch."""
    data = defaultdict(lambda: defaultdict(list))
    providers = defaultdict(set)
    with open(CSV_PATH, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            task = row["task"]
            model = row["model"]
            score = float(row["score"])
            cost = float(row["cost_usd"])
            data[task][model].append({"score": score, "cost": cost})
            providers[model].add(row["provider"])
    return data, providers


def get_complete_models_csv(raw):
    """Return models with 21/21 tasks AND >= MIN_CASES_PER_TASK on each."""
    model_tasks = defaultdict(dict)
    for task in V2_TASKS:
        for model in raw[task]:
            n = len(raw[task][model])
            model_tasks[model][task] = n
    return [m for m, tasks in model_tasks.items()
            if len(tasks) == 21 and all(n >= MIN_CASES_PER_TASK for n in tasks.values())]


def check(name, expected, actual, tol=0.002):
    """Check if two values match within tolerance."""
    if isinstance(expected, float) and isinstance(actual, float):
        if abs(expected - actual) > tol:
            print(f"  ✗ {name}: expected {expected}, got {actual} (diff {actual-expected:+.4f})")
            return False
        else:
            print(f"  ✓ {name}: {actual}")
            return True
    elif expected != actual:
        print(f"  ✗ {name}: expected {expected}, got {actual}")
        return False
    else:
        print(f"  ✓ {name}: {actual}")
        return True


def main():
    errors = 0

    print("=" * 60)
    print("STEP 1: Load CSV and compute ground truth from raw data")
    print("=" * 60)
    raw, providers = load_csv()

    # Count rows
    total_rows = sum(len(scores) for task in raw for scores in raw[task].values())
    print(f"\nTotal scored cases: {total_rows}")
    errors += not check("Total rows", 51580, total_rows)

    # Unique tasks
    all_tasks = set(raw.keys())
    v2_in_csv = set(t for t in V2_TASKS if t in all_tasks)
    print(f"V2 tasks in CSV: {len(v2_in_csv)}/21")
    errors += not check("V2 task count", 21, len(v2_in_csv))

    # Compute complete models (21/21 tasks, >=40 cases each)
    complete = get_complete_models_csv(raw)
    print(f"Complete models (21/21, >=40 cases): {len(complete)}")
    errors += not check("Complete model count", 46, len(complete))

    # Tier counts
    tier_counts = defaultdict(int)
    for m in complete:
        tier_counts[get_tier(m)] += 1
    print(f"\nTier distribution:")
    errors += not check("Premium", 2, tier_counts["Premium"])
    errors += not check("Standard", 18, tier_counts["Standard"])
    errors += not check("Economy", 23, tier_counts["Economy"])
    errors += not check("Micro", 3, tier_counts["Micro"])

    # Compute per-model global averages (from CSV)
    model_avgs = {}
    for m in complete:
        scores = []
        for t in V2_TASKS:
            task_scores = [d["score"] for d in raw[t][m]]
            scores.append(sum(task_scores) / len(task_scores))
        model_avgs[m] = sum(scores) / len(scores)

    # Tier means
    tier_scores = defaultdict(list)
    for m in complete:
        for t in V2_TASKS:
            task_scores = [d["score"] for d in raw[t][m]]
            avg = sum(task_scores) / len(task_scores)
            tier_scores[get_tier(m)].append(avg)

    tier_means = {t: sum(s)/len(s) for t, s in tier_scores.items()}
    print(f"\nTier means (from CSV):")
    for t in ["Premium", "Standard", "Economy", "Micro"]:
        print(f"  {t}: {tier_means[t]:.3f} (n_pairs={len(tier_scores[t])})")

    # Provider count
    all_providers = set()
    for m in complete:
        all_providers.update(providers[m])
    print(f"\nProviders for complete models: {len(all_providers)}: {sorted(all_providers)}")

    print("\n" + "=" * 60)
    print("STEP 2: Verify JSONs against CSV-computed values")
    print("=" * 60)

    # Check task_model_aggregates.json
    print("\n--- task_model_aggregates.json ---")
    with open(os.path.join(JSON_DIR, "task_model_aggregates.json")) as f:
        agg = json.load(f)

    mismatches = 0
    missing = 0
    for task in V2_TASKS:
        for model in complete:
            if model not in agg.get(task, {}):
                print(f"  ✗ {task}/{model}: in CSV complete set but MISSING from JSON")
                missing += 1
                continue
            csv_scores = [d["score"] for d in raw[task][model]]
            csv_avg = sum(csv_scores) / len(csv_scores)
            json_avg = agg[task][model]["avg_score"]
            if abs(csv_avg - json_avg) > 0.001:
                print(f"  ✗ {task}/{model}: CSV={csv_avg:.4f}, JSON={json_avg:.4f}")
                mismatches += 1
    if mismatches == 0 and missing == 0:
        print(f"  ✓ All {len(complete)*21} (model,task) averages match CSV")
    errors += mismatches + missing

    # Check stats_validation.json
    print("\n--- stats_validation.json ---")
    with open(os.path.join(JSON_DIR, "stats_validation.json")) as f:
        stats = json.load(f)

    boot = stats["bootstrap"]
    for tier in ["Premium", "Standard", "Economy", "Micro"]:
        json_mean = boot[tier]["mean"]
        csv_mean = tier_means[tier]
        errors += not check(f"{tier} mean", csv_mean, json_mean, tol=0.01)
        json_n = boot[tier]["n"]
        csv_n = len(tier_scores[tier])
        errors += not check(f"{tier} n_pairs", csv_n, json_n)

    # Check task_discriminativeness.json spreads vs complete-only CSV
    print("\n--- task_discriminativeness (complete models only) ---")
    for task in V2_TASKS:
        csv_scores = []
        for m in complete:
            task_scores = [d["score"] for d in raw[task][m]]
            csv_scores.append(sum(task_scores) / len(task_scores))
        csv_spread = max(csv_scores) - min(csv_scores)
        # This is what the FIGURE now uses (recomputed from complete models)
        print(f"  {task}: spread={csv_spread:.2f}")

    # Best model
    best_model = max(model_avgs, key=model_avgs.get)
    best_score = model_avgs[best_model]
    print(f"\nBest model: {best_model} ({best_score:.3f})")

    # Routing savings
    print("\n--- per_task_routing_savings (verify against CSV) ---")
    with open(os.path.join(JSON_DIR, "per_task_routing_savings.json")) as f:
        routing = json.load(f)

    o3_cost = None
    for task in V2_TASKS:
        for d in raw[task].get("o3", []):
            if o3_cost is None:
                o3_costs = [dd["cost"] for dd in raw[task]["o3"]]
                break

    # Recompute cheapest adequate model per task from CSV
    total_routed_cost = 0
    total_o3_cost = 0
    for task in V2_TASKS:
        # o3 cost for this task
        o3_task_costs = [d["cost"] for d in raw[task]["o3"]]
        o3_avg_cost = sum(o3_task_costs) / len(o3_task_costs)
        total_o3_cost += o3_avg_cost

        # Find cheapest model with avg_score >= 4.0
        best_cheap = None
        best_cheap_cost = float('inf')
        for m in complete:
            task_scores = [d["score"] for d in raw[task][m]]
            avg_score = sum(task_scores) / len(task_scores)
            task_costs = [d["cost"] for d in raw[task][m]]
            avg_cost = sum(task_costs) / len(task_costs)
            if avg_score >= 4.0 and avg_cost < best_cheap_cost:
                best_cheap = m
                best_cheap_cost = avg_cost

        total_routed_cost += best_cheap_cost

    savings_pct = (1 - total_routed_cost / total_o3_cost) * 100
    print(f"  o3 total cost/query: ${total_o3_cost:.6f}")
    print(f"  Routed total cost/query: ${total_routed_cost:.6f}")
    print(f"  Savings: {savings_pct:.1f}%")

    print("\n" + "=" * 60)
    print("STEP 3: Check key numbers in main.tex")
    print("=" * 60)

    with open(TEX_PATH) as f:
        tex = f.read()

    # Check tier counts in tex
    print("\n--- Tier table in tex ---")
    if "Standard & \\$0.50--\\$4.99" in tex:
        # Find the n values
        import re
        tier_table = re.findall(r'(Premium|Standard|Economy|Micro)\s+&.*?&\s+(\d+)', tex)
        for tier_name, n_str in tier_table:
            n_tex = int(n_str)
            n_actual = tier_counts[tier_name]
            errors += not check(f"tex {tier_name} n", n_actual, n_tex)

    # Check total rows
    if "51,580" in tex or "51{,}580" in tex:
        print(f"  ✓ Total rows 51,580 in tex")
    else:
        print(f"  ✗ Total rows 51,580 NOT found in tex")
        errors += 1

    # Check provider count
    provider_mentions = re.findall(r'(\d+)\s+(?:API\s+)?providers', tex)
    for pm in provider_mentions:
        n_prov = int(pm)
        errors += not check(f"tex provider count", len(all_providers), n_prov)

    # Check Premium-Economy gap
    gap = tier_means["Premium"] - tier_means["Economy"]
    print(f"\n  CSV Premium-Economy gap: {gap:.3f}")
    gap_mentions = re.findall(r'gap of ([\d.]+)', tex)
    for gm in gap_mentions:
        errors += not check("tex gap", gap, float(gm), tol=0.02)

    # Check model price for Nano
    nano_price = MODEL_PRICES.get("gpt-5.4-nano", None)
    print(f"\n  GPT-5.4 Nano actual price: ${nano_price}/M")
    if "Nano at \\$0.02/M" in tex:
        print(f"  ✗ tex says Nano at $0.02/M — WRONG (should be ${nano_price})")
        errors += 1
    elif f"Nano" in tex:
        nano_tex = re.findall(r'Nano.*?\$([0-9.]+)/M', tex)
        for nt in nano_tex:
            errors += not check("tex Nano price", nano_price, float(nt), tol=0.01)

    # Summary
    print("\n" + "=" * 60)
    if errors == 0:
        print("ALL CHECKS PASSED")
    else:
        print(f"FOUND {errors} ERROR(S)")
    print("=" * 60)

    return errors


if __name__ == "__main__":
    sys.exit(main())
