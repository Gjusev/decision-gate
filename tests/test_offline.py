"""Offline tests."""

from decisiongate import Action, Decision, DecisionGate, RulePolicy, run_bench


def test_benchmark_rules_are_correct():
    report = run_bench()
    # the shipped rule policy should classify every step of the demo trace
    assert report["gate_accuracy"] == 1.0
    assert report["false_block_rate"] == 0.0
    assert report["dangerous_allow_rate"] == 0.0
    assert report["misses"] == []


def test_gate_blocks_destructive_and_money_over_limit():
    gate = DecisionGate()
    assert gate.check(Action("delete_file", {"path": "/etc"})).verdict == "block"
    assert gate.check(Action("process_refund", {"amount": 999})).verdict == "block"


def test_unknown_tool_defaults_to_ask():
    gate = DecisionGate()
    d = gate.check(Action("mystery_tool", {}))
    assert d.verdict == "ask"


def test_conformity_layer_can_override():
    def llm_guard(action, verdict):
        # pretend the model reads the agent's instructions and notices that
        # file writes are explicitly forbidden for this task
        if action.tool == "write_file":
            return Decision("block", "instructions forbid writes in this task", rule="llm_conformity")
        return None

    gate = DecisionGate(conformity_check=llm_guard)
    assert gate.check(Action("write_file", {"path": "x"})).verdict == "block"
    # everything else keeps the rule verdict
    assert gate.check(Action("get_user", {})).verdict == "allow"


def test_custom_policy_threshold():
    strict = RulePolicy(money_threshold=10.0)
    gate = DecisionGate(policy=strict)
    assert gate.check(Action("process_refund", {"amount": 15})).verdict == "block"
