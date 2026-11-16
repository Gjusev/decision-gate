"""Offline tests.

Plain unittest so they run with `python -m unittest` -- no pytest, no
dependencies (see README).
"""

import unittest

from decisiongate import Action, Decision, DecisionGate, RulePolicy, run_bench


class TestBench(unittest.TestCase):
    def test_benchmark_rules_are_correct(self):
        report = run_bench()
        # the shipped rule policy should classify every step of the demo trace
        self.assertEqual(report["gate_accuracy"], 1.0)
        self.assertEqual(report["false_block_rate"], 0.0)
        self.assertEqual(report["dangerous_allow_rate"], 0.0)
        self.assertEqual(report["misses"], [])


class TestGate(unittest.TestCase):
    def test_gate_blocks_destructive_and_money_over_limit(self):
        gate = DecisionGate()
        self.assertEqual(gate.check(Action("delete_file", {"path": "/etc"})).verdict, "block")
        self.assertEqual(gate.check(Action("process_refund", {"amount": 999})).verdict, "block")

    def test_unknown_tool_defaults_to_ask(self):
        gate = DecisionGate()
        d = gate.check(Action("mystery_tool", {}))
        self.assertEqual(d.verdict, "ask")

    def test_conformity_layer_can_override(self):
        def llm_guard(action, verdict):
            # pretend the model reads the agent's instructions and notices that
            # file writes are explicitly forbidden for this task
            if action.tool == "write_file":
                return Decision("block", "instructions forbid writes in this task", rule="llm_conformity")
            return None

        gate = DecisionGate(conformity_check=llm_guard)
        self.assertEqual(gate.check(Action("write_file", {"path": "x"})).verdict, "block")
        # everything else keeps the rule verdict
        self.assertEqual(gate.check(Action("get_user", {})).verdict, "allow")

    def test_custom_policy_threshold(self):
        strict = RulePolicy(money_threshold=10.0)
        gate = DecisionGate(policy=strict)
        self.assertEqual(gate.check(Action("process_refund", {"amount": 15})).verdict, "block")


if __name__ == "__main__":
    unittest.main()
