# Tier Recomputation

**Date:** 2026-05-22
**Purpose:** Resolve tier-count inconsistency found in critical review.

---

## The Problem

The original analysis (`analyze_v3.py`) had three inconsistencies:

1. **Economy boundary at $0.08**, not $0.05 as stated in the paper.
2. **Missing claude-haiku-4-5-20251001** from MODEL_PRICES (defaulted to
   Standard at $0.50, should be Standard at $0.80).
3. **Wrong prices** for 4 models: grok-4-fast ($0.60 should be $0.20),
   grok-code-fast-1 ($0.60 should be $0.20), seed-2-0-pro ($0.20 should
   be $0.60), seed-2-0-code-preview ($0.10 should be $0.30).
4. **Partial models included** in tier comparison (nemotron, gemini-2.0-flash,
   deepseek-v4-flash had < 40 cases on some tasks but were counted in tier
   stats where they had enough data).

## The Fix

Modified `analyze_v3.py`:
- Changed `get_tier()` boundary from $0.08 to $0.05.
- Fixed 5 prices in MODEL_PRICES (4 corrections + 1 addition).
- Added `get_complete_models()` filter: tier comparison now uses only the
  46 models with 21/21 tasks at >= 40 cases each.
- Added Mann-Whitney Economy vs Premium per task to `stats_validation()`.

## The Rule (canonical, paper-final)

```
Tier assignment uses provider-published input prices at benchmark time
(April-May 2026). Boundaries:
  Premium  >= $5.00/M input tokens
  Standard >= $0.50/M and < $5.00/M
  Economy  >= $0.05/M and < $0.50/M
  Micro    <  $0.05/M

Only the 46 models completing all 21 tasks with >= 40 valid cases each
are included in tier-level statistics.
```

## Old vs New Numbers

### Tier Counts

| Tier | Old n | New n | Change |
|------|:-----:|:-----:|--------|
| Premium | 2 | 2 | unchanged |
| Standard | ~22 | 19 | grok-4-fast, grok-code-fast-1 moved to Economy; seed-2-0-pro added |
| Economy | ~13 | 21 | gained models from boundary change + price corrections |
| Micro | ~9 | 4 | lost models to Economy due to $0.05 boundary |
| **Total** | **~46** | **46** | |

### Bootstrap CIs (global, all tasks)

| Tier | Old mean [CI] | New mean [CI] | Change |
|------|:---:|:---:|--------|
| Premium | 4.791 [4.729, 4.853] | 4.791 [4.729, 4.853] | **Unchanged** |
| Standard | 4.787 [4.765, 4.808] | 4.783 [4.760, 4.805] | mean -0.004 |
| Economy | 4.749 [4.715, 4.777] | 4.741 [4.710, 4.768] | mean -0.008 |
| Micro | 4.519 [4.435, 4.599] | 4.287 [4.128, 4.449] | mean **-0.232** |

Premium is exactly the same (still 2 models x 21 tasks = 42 pairs).
Standard and Economy shift by < 0.01 points (negligible).
Micro drops significantly because it now has only 4 models (including
Llama 1B at 3.394 avg, which pulls the mean down).

### Mann-Whitney Economy vs Premium

| Metric | Old | New |
|--------|-----|-----|
| Tasks tested | 21 | 21 |
| Significant at 0.05 | 0/21 | **2/21** |
| Economy-Premium gap | 0.042 | 0.050 |

The two significant tasks:
- `multistep_reasoning`: Economy 4.910 > Premium 4.650, p=0.029 (Economy wins)
- `instruction_following`: Economy 4.763 < Premium 4.880, p=0.043 (Premium wins)

The two results go in **opposite directions**. With 21 simultaneous tests
at alpha=0.05, 1-2 rejections are expected by chance (Bonferroni: none
would survive at 0.05/21 = 0.0024). The pattern is consistent with no
systematic tier effect.

## Does the Finding Hold?

**Yes.** The headline finding survives with minor rewording:

Old: "No significant difference on any of the 21 tasks (p>0.05, 21/21)."
New: "No significant difference on 19 of 21 tasks (p>0.05). The two
significant results favor opposite tiers."

The core message is unchanged: there is no consistent quality advantage
to paying for Premium models. The Economy-Premium gap (0.050 points,
1.0% of the scale) is statistically and practically negligible.

## Provider Count

Old: "9 API providers"
New: **12 API providers**

| Provider | Models | Country |
|----------|:------:|---------|
| OpenAI | 10 | American |
| Qwen | 7 | Chinese |
| ByteDance | 5 | Chinese |
| Mistral | 5 | European |
| Anthropic | 4 | American |
| Google | 4 | American |
| xAI | 3 | American |
| Meta | 3 | American |
| DeepSeek | 2 | Chinese |
| MiniMax | 1 | Chinese |
| Moonshot | 1 | Chinese |
| Microsoft | 1 | American |

Definition: a provider is a distinct organization offering API access
to its own models. ByteDance Seed models accessed via ByteDance API
count as one provider. Gemma (Google open-weight) counts under Google.
