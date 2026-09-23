"""Local insurance JSON agent and MCP server.

Run an interactive Ollama agent:
    python app.py

Run as an MCP server over stdio:
    python app.py --mcp
"""

from __future__ import annotations

import argparse
import inspect
import json
import re
from pathlib import Path
from typing import Any

import ollama
from fastmcp import FastMCP

DATA_DIR = Path(__file__).resolve().parent
TARGET_MODEL = "qwen2.5-coder:7b-instruct-q4_K_M"
COLLECTION_FILES = {
    "plans": "plans.json",
    "users": "users.json",
    "policies": "policy_purchases.json",
    "claims": "claims.json",
    "payments": "payments.json",
}


def load_collection(collection: str) -> list[dict[str, Any]]:
    """Load one allowed collection from the local data directory."""
    if collection not in COLLECTION_FILES:
        allowed = ", ".join(COLLECTION_FILES)
        raise ValueError(f"Unknown collection '{collection}'. Use one of: {allowed}")

    path = DATA_DIR / COLLECTION_FILES[collection]
    with path.open(encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(f"{path.name} must contain a JSON array")
    return data


def _searchable_text(value: Any) -> str:
    """Flatten nested JSON into lowercase text for simple local searching."""
    if isinstance(value, dict):
        return " ".join(_searchable_text(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(_searchable_text(item) for item in value)
    return str(value).lower()


def dataset_summary() -> dict[str, Any]:
    """Return collection names, record counts, and available top-level fields."""
    summary: dict[str, Any] = {}
    for name in COLLECTION_FILES:
        records = load_collection(name)
        summary[name] = {
            "count": len(records),
            "fields": sorted(records[0].keys()) if records else [],
        }
    return summary


def search_records(
    query: str,
    collection: str = "all",
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Search insurance JSON records by text, ID, name, code, email, or status.

    Args:
        query: Case-insensitive text to find anywhere inside a record.
        collection: plans, users, policies, claims, payments, or all.
        limit: Maximum number of matching records to return (1-50).
    """
    query = query.strip().lower()
    if not query:
        raise ValueError("query cannot be empty")
    limit = max(1, min(limit, 50))

    names = list(COLLECTION_FILES) if collection == "all" else [collection]
    matches: list[dict[str, Any]] = []
    for name in names:
        for record in load_collection(name):
            if query in _searchable_text(record):
                matches.append({"collection": name, "record": record})
                if len(matches) >= limit:
                    return matches
    return matches


def list_plans(
    category: str = "all",
    active_only: bool = True,
    max_yearly_premium: float | None = None,
) -> list[dict[str, Any]]:
    """List insurance plans, optionally filtering category and maximum premium."""
    results = []
    for plan in load_collection("plans"):
        if active_only and not plan.get("isActive"):
            continue
        if category != "all" and plan.get("category", "").lower() != category.lower():
            continue
        premium = plan.get("premium", {}).get("amount", 0)
        if max_yearly_premium is not None and premium > max_yearly_premium:
            continue
        results.append(plan)
    return results


def get_customer_overview(customer: str) -> dict[str, Any]:
    """Get a customer and all their policies, claims, and payments.

    Args:
        customer: Customer ID, customer code, email address, or full/partial name.
    """
    needle = customer.strip().lower()
    users = [u for u in load_collection("users") if needle in _searchable_text(u)]
    if not users:
        return {"found": False, "query": customer}

    user = users[0]
    customer_id = user["_id"]
    policies = [
        p for p in load_collection("policies") if p.get("customerId") == customer_id
    ]
    policy_ids = {p["_id"] for p in policies}
    claims = [c for c in load_collection("claims") if c.get("policyId") in policy_ids]
    payments = [
        p for p in load_collection("payments") if p.get("customerId") == customer_id
    ]
    return {
        "found": True,
        "customer": user,
        "policies": policies,
        "claims": claims,
        "payments": payments,
    }


def get_policy_overview(policy: str) -> dict[str, Any]:
    """Get a policy and its related customer, claims, and payments."""
    needle = policy.strip().lower()
    matches = [p for p in load_collection("policies") if needle in _searchable_text(p)]
    if not matches:
        return {"found": False, "query": policy}

    selected = matches[0]
    policy_id = selected["_id"]
    users = [
        u
        for u in load_collection("users")
        if u.get("_id") == selected.get("customerId")
    ]
    claims = [c for c in load_collection("claims") if c.get("policyId") == policy_id]
    payments = [
        p for p in load_collection("payments") if p.get("policyId") == policy_id
    ]
    return {
        "found": True,
        "policy": selected,
        "customer": users[0] if users else None,
        "claims": claims,
        "payments": payments,
    }


mcp = FastMCP("Insurance JSON MCP")
mcp.tool()(dataset_summary)
mcp.tool()(search_records)
mcp.tool()(list_plans)
mcp.tool()(get_customer_overview)
mcp.tool()(get_policy_overview)

TOOL_FUNCTIONS = {
    function.__name__: function
    for function in (
        dataset_summary,
        search_records,
        list_plans,
        get_customer_overview,
        get_policy_overview,
    )
}

SYSTEM_PROMPT = """You are a local insurance data assistant.
Use the provided tools whenever a question depends on the JSON datasets.
Never invent customers, policies, claims, payments, prices, or totals.
Answer concisely and mention IDs or codes that help the user verify the result.
The data is fictional test data and all monetary values are INR unless stated otherwise.
"""


def process_agent_query(
    user_input: str,
    history: list[dict[str, str]] | None = None,
) -> str:
    """Let Ollama select local tools and produce a grounded final response."""
    history = history or []
    ambiguous_reference = re.search(
        r"\b(that|this|it|its)\s+plan\b", user_input, re.IGNORECASE
    )
    if ambiguous_reference and not history:
        return "Which plan do you mean? Please provide its name or plan code, such as Health Secure or HLT-SEC-01."

    messages: list[Any] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history[-10:],
        {"role": "user", "content": user_input},
    ]

    response = ollama.chat(
        model=TARGET_MODEL, messages=messages, tools=list(TOOL_FUNCTIONS.values())
    )
    messages.append(response.message)

    requested_tools: list[tuple[str, dict[str, Any]]] = []
    for call in response.message.tool_calls or []:
        requested_tools.append((call.function.name, call.function.arguments))

    # Some Qwen Ollama templates return a valid tool request as JSON text
    # instead of populating message.tool_calls. Support both response shapes.
    if not requested_tools and response.message.content:
        try:
            raw_request = json.loads(response.message.content)
            name = raw_request.get("name")
            arguments = raw_request.get("arguments", {})
            if name in TOOL_FUNCTIONS and isinstance(arguments, dict):
                requested_tools.append((name, arguments))
        except (json.JSONDecodeError, AttributeError):
            pass

    completed_tools: list[dict[str, Any]] = []
    for name, arguments in requested_tools:
        function = TOOL_FUNCTIONS.get(name)
        if function is None:
            result: Any = {"error": f"Unknown tool requested: {name}"}
        else:
            try:
                allowed_arguments = inspect.signature(function).parameters
                clean_arguments = {
                    key: value
                    for key, value in arguments.items()
                    if key in allowed_arguments
                }
                result = function(**clean_arguments)
            except Exception as error:
                result = {"error": str(error)}

        print(f"🔧 Tool used: {name}")
        completed_tools.append({"tool": name, "result": result})
        messages.append(
            {
                "role": "tool",
                "tool_name": name,
                "content": json.dumps(result, ensure_ascii=False),
            }
        )

    if requested_tools:
        response = ollama.chat(
            model=TARGET_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *history[-10:],
                {"role": "user", "content": user_input},
                {
                    "role": "system",
                    "content": "The requested local tools returned this JSON. Answer the user's question using only these results:\n"
                    + json.dumps(completed_tools, ensure_ascii=False),
                },
            ],
        )
    return response.message.content


def interactive_loop() -> None:
    print(f"--- Starting Interactive JSON Engine with {TARGET_MODEL} ---")
    print("Type your questions below (or type 'exit' to quit)\n")
    history: list[dict[str, str]] = []
    while True:
        try:
            user_input = input("💡 Ask about insurance data: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nShutting down agent backend. Goodbye!")
            break
        if user_input.lower() in {"exit", "quit"}:
            print("Shutting down agent backend. Goodbye!")
            break
        if not user_input:
            continue
        try:
            answer = process_agent_query(user_input, history)
            print(f"\n{answer}\n")
            history.extend(
                [
                    {"role": "user", "content": user_input},
                    {"role": "assistant", "content": answer},
                ]
            )
        except Exception as error:
            print(f"\nUnable to proess query: {error}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insurance JSON agent and MCP server")
    parser.add_argument(
        "--mcp", action="store_true", help="run the FastMCP stdio server"
    )
    args = parser.parse_args()
    if args.mcp:
        mcp.run()
    else:
        interactive_loop()
