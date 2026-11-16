# decision-gate

[![tests](https://github.com/Gjusev/decision-gate/actions/workflows/tests.yml/badge.svg)](https://github.com/Gjusev/decision-gate/actions/workflows/tests.yml)
[![dependencies](https://img.shields.io/badge/dependencies-0-success)]()
[![python](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/logo-animated-dark.svg">
    <img src="assets/logo/logo-animated-light.svg" alt="decision-gate: an action dot meets the gate — pass, pause and ask, or bounce back" width="560">
  </picture>
</p>

<p align="center">
  <a href="assets/video/decision-gate.mp4">
    <img src="assets/video/preview.gif" alt="decision-gate: the animated mark beside the headline number, 12/12 demo actions classified correctly" width="720">
  </a>
  <br>
  <sub><a href="assets/video/decision-gate.mp4">Watch the 8-second film (MP4, 0.2 MB)</a>. Every number in it comes from the committed results in this repo.</sub>
</p>

Implementation test of [Think Before You Act: Decision Gate for LLM Agents](https://arxiv.org/abs/2610.38620):
a cheap gate sits between the agent and its tools and returns allow / ask /
block for every action before it executes.

## Use case

An office assistant with retail-style tools (look up orders, modify orders,
refunds, emails, files). The demo trace walks one customer ticket end to end:
12 actions, each with the verdict the gate should return. The two failure
modes tracked are the ones that matter in production:

- **false block**: a safe action stopped. Kills user trust.
- **dangerous allow**: an unsafe action let through. The one that hurts.

## Offline result

The shipped rule policy classifies all 12 steps of the demo trace correctly:
1.0 gate accuracy, 0 false blocks, 0 dangerous allows. The architecture is two
layers: deterministic rules decide the clear cases; an optional conformity
layer (LLM in production, injected as a callable) can override in the gray
zone, for example when the agent's task instructions forbid an otherwise
normal tool.

## Use it

```python
from decisiongate import Action, DecisionGate

gate = DecisionGate()
print(gate.check(Action("process_refund", {"amount": 500})).verdict)  # block
print(gate.check(Action("search_orders", {"order_id": "O-1"})).verdict)  # allow
print(gate.check(Action("modify_order", {"order_id": "O-1"})).verdict)  # ask
```

Wire an LLM conformity check:

```python
def llm_guard(action, verdict):
    # read the agent's task instructions, check the action against them,
    # return a Decision to override or None to keep the rule verdict
    ...

gate = DecisionGate(conformity_check=llm_guard)
```

```bash
python -m unittest   # offline, zero dependencies, runs on Linux/macOS/Windows
```

## Where this goes next

See [ROADMAP.md](ROADMAP.md) — next up: a real LLM conformity layer over the
Z.ai endpoint (owner-gated), conformal thresholds merged from
[gate-calibrated](https://github.com/Gjusev/gate-calibrated), and rule sets
per agent profile. [CONTINUE.md](CONTINUE.md) has the handoff rules for
coding agents picking this up.

## Repository layout

```
decisiongate/   Action, Decision, DecisionGate, RulePolicy, demo-trace bench
tests/          offline unit tests (python -m unittest, zero dependencies)
assets/         animated logo + launch film (SVG, MP4, GIF)
ROADMAP.md      ordered next steps
CONTINUE.md     agent handoff: working rules + STOP points
```

## Citation

Independent implementation test. Cite the paper first:
arXiv:2610.38620 (Think Before You Act: Decision Gate for LLM Agents).

MIT
