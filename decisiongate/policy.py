"""Rule policy: deterministic risk scoring for tool calls.

Rules are ordered; the first match wins. Custom policies subclass and override
evaluate(). This offline policy encodes the tau-bench-retail-like office
assistant: read tools are safe, writes ask, destructive or external actions
block unless whitelisted.
"""

from __future__ import annotations

from .types import Action, Decision


class RulePolicy:
    def __init__(
        self,
        allow_tools: set[str] | None = None,
        ask_tools: set[str] | None = None,
        block_tools: set[str] | None = None,
        money_threshold: float = 50.0,
        external_domains: set[str] | None = None,
    ) -> None:
        self.allow_tools = allow_tools or {
            "search_orders", "get_user", "read_file", "list_files", "lookup_product",
        }
        self.ask_tools = ask_tools or {
            "modify_order", "write_file", "move_file", "update_user",
        }
        self.block_tools = block_tools or {
            "delete_file", "drop_database", "run_shell",
        }
        self.money_threshold = money_threshold
        self.external_domains = external_domains or {"gmail.com", "outlook.com"}

    def evaluate(self, action: Action) -> Decision:
        tool = action.tool
        args = action.args

        if tool in self.block_tools:
            return Decision("block", "destructive tool is never allowed", rule="block_list")

        if tool in ("send_email", "post_webhook"):
            recipient = str(args.get("to", args.get("url", "")))
            if any(dom in recipient for dom in self.external_domains):
                return Decision("ask", f"external recipient {recipient}", rule="external_recipient")
            return Decision("allow", "internal recipient", rule="internal_recipient")

        if tool in ("process_refund", "charge_card", "create_payment"):
            amount = float(args.get("amount", 0))
            if amount > self.money_threshold:
                return Decision("block", f"{amount} exceeds limit {self.money_threshold}", rule="money_limit")
            if amount <= 0:
                return Decision("block", "non-positive amount", rule="money_invalid")
            return Decision("ask", f"money action of {amount} needs confirmation", rule="money_confirm")

        if tool in self.ask_tools:
            return Decision("ask", "write action needs confirmation", rule="write_confirm")

        if tool in self.allow_tools:
            return Decision("allow", "read-only tool", rule="allow_list")

        return Decision("ask", "unknown tool defaults to ask", rule="unknown_tool")
