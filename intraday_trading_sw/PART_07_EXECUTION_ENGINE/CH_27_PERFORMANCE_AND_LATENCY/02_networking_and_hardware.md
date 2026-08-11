# 02 — Networking and Hardware

## Purpose
Describe the infrastructure choices that keep the live system fast, reliable,
and self-hosted — without requiring HFT-grade colocation.

## Deployment target (recommended)
- A dedicated small VPS or a local always-on machine near the broker's region
  (network latency matters more than CPU here).
- 2 vCPU / 4–8 GB RAM is typically enough for the MVP (hundreds of symbols,
  1m strategies). Scale vertically before horizontally (CH_31).

## Networking
- Prefer the broker/exchange WebSocket feed (push) over REST polling (CH_05/02).
- One persistent connection per data stream; one for order callbacks.
- TCP tuning defaults are usually fine; document kernel buffering if problems appear.
- Keep the machine's clock synchronized (NTP) — timestamps and audits depend on it.

## Hardware guidance
- **Storage**: SSD/NVMe (fast appends + reads); local, not a network mount, for
  the hot tier.
- **Memory**: the hot store should fit in RAM (today's bars + features); warm data
  streams from disk.
- **CPU**: single fast core usually outperforms many slow cores for the
  sequential engine loop.
- **Uptime**: UPS + auto-restart (CH_31/02) beat raw spec.

## Pseudo-code: placement heuristic
```
placement:
  if latency_to_broker < 20ms and always_on: local/server OK
  else: prefer VPS in broker region
  ensure: SSD, NTP, auto-start, firewall only needed ports
```

## Rules
- Network is the largest variable latency source — put the machine near the feed.
- Measure broker round-trip (RTT) and include it in the latency budget (CH_27/00).
- Keep infrastructure boring: standard OS, standard tooling, documented setup
  (CH_31/00).
