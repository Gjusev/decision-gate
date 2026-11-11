"""The gate: policy verdict first, optional LLM conformity check for 'ask'/'block' gray zones.

The LLM layer is where the paper's contribution lives (checking an action
against the agent's instructions before it runs); offline it is a pass-through
so the rule layer is testable without tokens.
"""

from __future__ import annotations

from .policy import RulePolicy
from .types import Action, Decision


class DecisionGate:
    def __init__(self, policy: RulePolicy | None = None, conformity_check=None) -> None:
        # conformity_check: callable(action, policy_verdict) -> Decision | None.
        # Return None to keep the policy verdict. Wire an LLM here in production.
        self.policy = policy or RulePolicy()
        self.conformity_check = conformity_check

    def check(self, action: Action) -> Decision:
        verdict = self.policy.evaluate(action)
        if self.conformity_check is not None:
            overridden = self.conformity_check(action, verdict)
            if overridden is not None:
                return overridden
        return verdict
