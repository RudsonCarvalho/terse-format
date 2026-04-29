# TERSE Tool Catalog (TTC)

Extension to the [TERSE Format](../../README.md) for compact, semantically enriched MCP tool catalog representation.

**66.6% fewer tokens** than MCP JSON Schema — with richer tool-selection semantics.

## Quick start

```
TOOL gmail_send_email
  PURPOSE: send email via Gmail
  IN: to:string, subject:string, body:string, cc:string?
  OUT: message_id:string
  ERR: auth_failed | quota_exceeded | invalid_recipient
  WHEN: user wants to send or compose an email
  TAGS: gmail, email, communication
```

## Contents

| Path | Description |
|---|---|
| [SPEC.md](SPEC.md) | Full TTC specification v1.0 |
| [converter/mcp_to_ttc.py](converter/mcp_to_ttc.py) | Python reference converter (MCP JSON → TTC) |
| [examples/gmail.ttc](examples/gmail.ttc) | Gmail MCP server catalog |
| [examples/drive.ttc](examples/drive.ttc) | Google Drive MCP server catalog |
| [examples/mixed_catalog.ttc](examples/mixed_catalog.ttc) | Multi-server agent context block |

## Why TTC?

MCP JSON Schema was designed as a machine-readable execution contract, not a semantic contract for LLM tool selection. TTC adds three fields that MCP lacks entirely:

| Field | Purpose |
|---|---|
| `WHEN` | Explicit trigger condition — the primary discriminator for tool selection |
| `ERR` | Failure mode contract — enables graceful degradation reasoning |
| `TAGS` | Retrieval taxonomy — supports RAG over tools |

See [SPEC.md](SPEC.md) for the full specification, benchmark data, and ABNF grammar.

## License

CC BY 4.0 — Rudson Kiyoshi Souza Carvalho
