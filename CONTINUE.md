# CONTINUE.md — read this first when an agent picks up this repo

## What this repo is

Implementation test of *Think Before You Act: Decision Gate for LLM Agents*
(arXiv:2610.38620): an allow/ask/block gate between an agent and its tools.
Two layers: deterministic rules for the clear cases, an optional LLM
conformity layer (injected callable) for the gray zone. Bench = one demo
customer ticket, 12 actions, rule policy classifies all 12 correctly.
Related: [gate-calibrated](https://github.com/Gjusev/gate-calibrated) is the
conformal-threshold sibling evaluated on tau-bench retail.

## Working rules

- **Offline-first**: `python -m unittest` from the repo root must stay green
  with zero dependencies. Any LLM client stays lazy/injected — nothing in
  `decisiongate/` imports network code.
- **Honest claims**: the 12-step demo trace is a mechanism check, not a
  benchmark result. Never present it as one.
- Independent implementation — cite the paper first, never imply affiliation
  with the authors. Commits: English, conventional style.
- Before pushing: run `python -m unittest`; it must be green.

## Models — Z.ai Coding Plan (MANDATORY, no other provider)

- base: `https://api.z.ai/api/coding/paas/v4`
- model: `glm-5.3-flash` ONLY
- key: `DECISION_GATE_ZAI_KEY` (env var, when item 1 lands)
- Flat subscription. On a billing/quota/endpoint error: **STOP and report** —
  do NOT switch providers or models. Real runs are owner-approval-gated.

## Current task (do this now)

Nothing in progress. Start with ROADMAP item 1 (real LLM conformity layer) —
but it is money-gated: propose the exact run plan and wait for the owner's OK
before any API call.

## STOP points

- Any billing/auth/endpoint error → stop, report, wait.
- If the demo trace and a new trace disagree on a rule → stop and surface the
  conflict; do not silently retune thresholds.
