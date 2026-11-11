"""decisiongate: implementation test of Think Before You Act / Decision Gate
for LLM agents (arXiv:2610.38620).

The idea: before an agent executes a tool call, a cheap gate checks the action
against policy and conformity rules and returns allow / ask / block. The
paper's concern is agents that act first and deal with consequences later.

Use case built in: an office assistant with email, file and payment tools
(the tau-bench-retail shape, close to our gate-calibrated work). Rules score
each action; an optional LLM conformity check handles the gray zone.
"""

from .types import Action, Decision
from .policy import RulePolicy
from .gate import DecisionGate
from .bench import GateBench, run_bench

__version__ = "0.1.0"
__all__ = ["Action", "Decision", "RulePolicy", "DecisionGate", "GateBench", "run_bench"]
