# TERSE

[![Spec](https://img.shields.io/badge/spec-Draft_v0.6-blue)](spec/TERSE-Spec-v0.6.pdf)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19058364.svg)](https://doi.org/10.5281/zenodo.19058364)

**Token-Efficient Recursive Serialization Encoding** — a compact, LLM-native alternative to JSON that covers the full JSON data model with **30–55% fewer tokens**.

## Why TERSE?

LLMs are billed per token. Every quotation mark, brace, comma, and repeated key in a JSON payload is a token with no informational value — pure structural noise. TERSE eliminates that noise while preserving the full expressive power of JSON.

Existing alternatives fall short:

| Format | Nested objects | Heterogeneous arrays | Typed nulls | LLM-readable |
|--------|:-:|:-:|:-:|:-:|
| JSON   | ✓ | ✓ | ✓ | ✓ |
| TOON   | ✗ | ✗ | ✗ | ✓ |
| YAML   | ✓ | ✓ | ✓ | ✓ (verbose) |
| CSV    | ✗ | ✗ | ✗ | ✓ (flat only) |
| **TERSE** | **✓** | **✓** | **✓** | **✓** |

## Quick example: JSON vs TERSE

**JSON** (85 tokens with cl100k_base):
```json
{
  "name": "my-app",
  "private": true,
  "port": 3000,
  "tags": ["web", "typescript", "spa"],
  "author": { "name": "Alice", "email": "alice@co.com" }
}
```

**TERSE** (~48 tokens — **≈44% fewer**):
```
name: my-app
private: T
port: 3000
tags: [web typescript spa]
author: {name:Alice email:alice@co.com}
```

## Token savings by document type

Measurements using the `cl100k_base` tokenizer (GPT-3.5/GPT-4):

| Document type | TERSE vs JSON | TOON vs JSON | CSV vs JSON |
|---|:-:|:-:|:-:|
| App config (package.json style) | **35–45%** | 15–20% | N/A |
| User list (flat, 5 records) | **40–55%** | 40–55% | 40–55% |
| Structured logs (5 entries) | **35–45%** | 35–45% | 35–45% |
| Product catalog (nested + array) | **30–40%** | 10–15% | N/A |
| Complex order (deep nesting) | **25–35%** | 5–10% | N/A |
| AI tool call payload (deep) | **20–30%** | 5–10% | N/A |

TOON and CSV savings are N/A for nested/complex types because those formats cannot represent those structures. TERSE maintains savings across **all** document types.

## Format rules in 30 seconds

| Concept | Syntax | Example |
|---|---|---|
| null | `~` | `score: ~` |
| true / false | `T` / `F` | `active: T` |
| number | JSON number grammar | `port: 3000` |
| bare string | safe identifier | `env: production` |
| quoted string | `"..."` (JSON escapes) | `msg: "hello world"` |
| inline object | `{k:v k2:v2}` | `point: {x:1 y:2}` |
| inline array | `[v1 v2 v3]` | `tags: [a b c]` |
| schema array | `#[fields]` + rows | see below |
| document | top-level key-value pairs | no outer `{}` |
| comments | `// ...` (line only) | `// config section` |

**Schema arrays** — the primary source of savings for tabular data. Uniform arrays of objects declare their fields once:

```
users:
  #[id name role active]
  1 Alice admin T
  2 Bob editor T
  3 Carla viewer F
```

Equivalent JSON would repeat `"id"`, `"name"`, `"role"`, `"active"` on every row.

## Why not compress further?

TERSE is optimized for the intersection of two constraints: token efficiency and human auditability. Further compression techniques — key abbreviation, binary type encoding, dictionary compression — would yield additional token savings but would break the ability to inspect, debug, and audit payloads without tooling. For LLM pipelines in production, auditability is a safety property, not just a convenience.

## Implementations

| Language | Repo | CI |
|---|---|---|
| TypeScript / JavaScript | [terse-js](https://github.com/RudsonCarvalho/terse-js) | [![CI](https://github.com/RudsonCarvalho/terse-js/actions/workflows/ci.yml/badge.svg)](https://github.com/RudsonCarvalho/terse-js/actions/workflows/ci.yml) |
| Python | [terse-py](https://github.com/RudsonCarvalho/terse-py) | [![CI](https://github.com/RudsonCarvalho/terse-py/actions/workflows/ci.yml/badge.svg)](https://github.com/RudsonCarvalho/terse-py/actions/workflows/ci.yml) |
| Java | [terse-java](https://github.com/RudsonCarvalho/terse-java) | [![CI](https://github.com/RudsonCarvalho/terse-java/actions/workflows/ci.yml/badge.svg)](https://github.com/RudsonCarvalho/terse-java/actions/workflows/ci.yml) |

## Specification

| File | Description |
|---|---|
| [spec/TERSE-Spec-v0.6.pdf](spec/TERSE-Spec-v0.6.pdf) | Full specification (PDF) |
| [spec/TERSE-Spec-v0.6.docx](spec/TERSE-Spec-v0.6.docx) | Full specification (Word) |
| [spec/abnf/terse.abnf](spec/abnf/terse.abnf) | ABNF grammar (Appendix A) |

## Examples

| File | Description |
|---|---|
| [examples/b1-app-config.terse](examples/b1-app-config.terse) | Application configuration |
| [examples/b2-rest-api-response.terse](examples/b2-rest-api-response.terse) | REST API response with schema array |
| [examples/b3-nested-order.terse](examples/b3-nested-order.terse) | Deeply nested e-commerce order |
| [examples/b4-mixed-types.terse](examples/b4-mixed-types.terse) | Mixed types and edge cases |

## Status

**Draft v0.6** — not yet ratified. The specification is open for community review. Sections 11 (Open Questions) and 13 (Security Considerations) are still under discussion. Target ratification: v1.0.

Contributions and issue reports are welcome.

## License

Specification: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
Implementations: MIT
