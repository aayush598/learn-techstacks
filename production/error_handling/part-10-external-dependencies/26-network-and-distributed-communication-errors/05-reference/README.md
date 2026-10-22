# Chapter 26 — Reference

> Part X · Chapter 26 · All subsections 26.1–26.20 · _Estimated reading time: 12 min_

## Network Error Cheat Sheet

### errno mapping
| errno/code | Category | Phase | Retryable | Notes |
| ---------- | -------- | ----- | ---------- | -----|
| `ENOTFOUND`, `EAI_NONAME` | dns_failure | dns | No | Config/hostname issue |
| `EAI_AGAIN` | dns_timeout | dns | Yes (with backoff) | Transient DNS |
| `ECONNREFUSED` | connection_refused | connect | Yes | No listener |
| `ETIMEDOUT` | connect_timeout/read_timeout | connect/read | Phase-dependent | Read ambiguous |
| `ECONNRESET` | connection_reset | write/read/connect | Idempotent only | May be ambiguous |
| `ECONNABORTED` | connection_aborted | any | Idempotent only | App closed |
| `EHOSTUNREACH`, `ENETUNREACH` | network_unreachable | connect | Sometimes | Routing |

### TLS errors
| Error | Category | Retryable | Notes |
| ----- | -------- | ---------- | -----|
| Certificate expired/invalid | tls_cert_invalid | No | Config |
| Hostname mismatch | tls_hostname_mismatch | No | SNI/cert |
| Handshake failure | tls_handshake_failed | No | Version/cipher/config |

### gRPC mapping
| gRPC code | Maps to | Notes |
| --------- | ------- | -----|
| `UNAVAILABLE` | connectivity/upstream unavailable | Often retryable |
| `DEADLINE_EXCEEDED` | timeout | May be ambiguous if after send |
| `UNAUTHENTICATED` | auth | Non-retryable |
| `PERMISSION_DENIED` | forbidden | Non-retryable |
| `RESOURCE_EXHAUSTED` | rate limit/quota | Retry with backoff |

### HTTP gateway codes
| Status | Category | Retryable | Ambiguous | Notes |
| ------ | -------- | ---------- | ---------- | -----|
| `502` | bad_gateway | Often yes | Sometimes | Origin issue |
| `503` | gateway_unavailable | Yes | No | Overload/maintenance |
| `504` | gateway_timeout | No by default | **Yes** | Origin may have processed |
| `429` | rate_limited | Yes | No | Respect Retry-After |

### Decision table: retry on timeout/reset
| Phase | Request sent fully? | Idempotent? | Retry? | Action |
| ----- | ------------------- | ----------- | ------ | ------ |
| connect | No | N/A | Usually yes | Retry with backoff |
| write | No (partial) | If idempotent | Cautious | Usually no/retry carefully |
| write | Yes (full) | If idempotent | No (ambiguous) | Status lookup first |
| read | Yes | If idempotent | No (ambiguous) | **Status lookup required** |
| read | Yes | No | Never | Status lookup/reconciliation |

## Related

- [Chapter 26 README](../README.md)
- [Dos and Don'ts](../04-dos-and-donts/README.md)
- [Network Error Classification Code](../03-practical-examples/01-network-error-classification-code.md)
- [Handling Lost Responses Safely](../03-practical-examples/02-handling-lost-responses-and-retries-safely.md)
- [Chapter 25 Reference](../../25-third-party-api-error-handling/05-reference/README.md)
- [Glossary](../../../GLOSSARY.md)
