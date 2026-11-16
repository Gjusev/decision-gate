# ROADMAP — decision-gate

Ordered by value. Items marked **(money-gated)** need LLM calls and therefore
explicit owner approval before running.

## 1. Real LLM conformity layer over the Z.ai endpoint (money-gated)

Wire `conformity_check` to a real model reading the agent's task instructions,
then re-run the demo trace with the gate metrics (`gate_accuracy`,
`false_block_rate`, `dangerous_allow_rate`). Owner rules: Z.ai Coding Plan
only, `glm-5.3-flash` only, stop on any billing/endpoint error.

## 2. Conformal thresholds on top of rule verdicts

Natural merge with [gate-calibrated](https://github.com/Gjusev/gate-calibrated):
calibrated probability + conformal threshold decide the ask band instead of the
current fixed money limit. Needs per-action outcome labels from a trace
dataset; gate-calibrated's tau-bench retail trajectories are the candidate.

## 3. Rule sets per agent profile

The six-agent setup (see gate-calibrated) has different risk maps: read-only
agents, write agents, money agents. Ship `RulePolicy` presets per profile and
bench them against each other on the same trace.

## 4. More traces

One demo trace is thin. Add tau-bench retail write-step traces (already
collected in gate-calibrated) as a second bench and report both.

## Done

- v0.1.0 — rule policy + optional conformity layer + demo-trace bench
  (12/12 correct, 0 false blocks, 0 dangerous allows), 5 offline tests,
  CI on Linux/Windows/macOS.
