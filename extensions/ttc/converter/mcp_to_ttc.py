"""
MCP JSON Schema -> TERSE Tool Catalog (TTC) converter.
Reference implementation -- TTC Extension Specification v1.0.
"""

from __future__ import annotations

TYPE_MAP = {
    "string": "string",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "array": "array",
    "object": "object",
}


def _map_type(schema: dict) -> str:
    base = TYPE_MAP.get(schema.get("type", ""), "any")
    if base == "array":
        items = schema.get("items", {})
        item_type = TYPE_MAP.get(items.get("type", ""), "")
        return f"array[{item_type}]" if item_type else "array[object]"
    return base


def _convert_params(input_schema: dict) -> str:
    props = input_schema.get("properties", {})
    required = set(input_schema.get("required", []))
    if not props:
        return "none:any"
    parts = []
    for name, schema in props.items():
        type_str = _map_type(schema)
        optional = "" if name in required else "?"
        parts.append(f"{name}:{type_str}{optional}")
    return ", ".join(parts)


def tool_to_ttc(tool: dict, indent: str = "  ") -> str:
    name = tool["name"]
    description = tool.get("description", "")
    input_schema = tool.get("input_schema", {})

    purpose = description[:80].rstrip()
    when_raw = description.split(".")[0].strip()
    when = when_raw if when_raw else description[:60].rstrip()
    params = _convert_params(input_schema)

    return "\n".join([
        f"{indent}TOOL {name}",
        f"{indent}  PURPOSE: {purpose}",
        f"{indent}  IN: {params}",
        f"{indent}  OUT: result:any",
        f"{indent}  ERR: error",
        f"{indent}  WHEN: {when}",
    ])


def server_to_ttc(server_id: str, version: str, tools: list[dict]) -> str:
    header = f"MCP {server_id} v{version}"
    blocks = "\n\n".join(tool_to_ttc(t) for t in tools)
    return f"{header}\n{blocks}"


def catalog_to_ttc(
    servers: list[dict],
    active: int | None = None,
    total: int | None = None,
) -> str:
    annotation = f" [{active}/{total}]" if active is not None and total is not None else ""
    header = f"TOOLS v1.0{annotation}"
    blocks = []
    for srv in servers:
        blocks.append(
            server_to_ttc(srv["server_id"], srv["version"], srv["tools"])
        )
    return header + "\n" + "\n\n".join(blocks)


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) < 2:
        print("Usage: mcp_to_ttc.py <mcp_schema.json>")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        for tool in data:
            print(tool_to_ttc(tool, indent=""))
            print()
    else:
        print(tool_to_ttc(data, indent=""))
