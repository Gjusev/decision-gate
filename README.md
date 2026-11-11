# decision-gate

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
python3 -m pytest tests/   # offline, zero dependencies
```

## Where this goes next

- Same architecture as [gate-calibrated](https://github.com/Gjusev/gate-calibrated)
  (conformal risk control on tau-bench retail) but scoped to per-action gates:
  natural merge is conformal thresholds on top of these rule verdicts
- Real LLM conformity layer over the Z.ai endpoint, evaluated on the trace
  with the gate metrics
- Rule sets per agent profile (the six-agent setup has different risk maps)

## Citation

Independent implementation test. Cite the paper first:
arXiv:2610.38620 (Think Before You Act: Decision Gate for LLM Agents).

MIT
