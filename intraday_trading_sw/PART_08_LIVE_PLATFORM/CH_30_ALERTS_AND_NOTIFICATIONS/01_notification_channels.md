# 01 — Notification Channels

## Purpose
Deliver alerts through reliable, self-hosted-friendly channels with guaranteed
delivery for critical events.

## Channel options (ranked for reliability)
1. **Email (SMTP)** — self-hostable, async, good audit trail. Recommended base.
2. **Push (self-hosted)** — e.g., a self-hosted push gateway or Telegram/Matrix
   bot (open protocols) for near-real-time.
3. **Webhook to your own server/phone app** — full control.
4. **SMS/phone** — only if truly necessary (cost, dependency).
5. **Dashboard in-app banner** — best-effort, never the only channel.

## Delivery guarantees
- **Critical alerts**: 2+ channels, with acknowledgment tracking.
- **Retry with backoff** on failure (email 3×; push 5×).
- **Dead-letter log**: if all channels fail, the alert stays in a local queue
  and is re-attempted; never silently dropped.
- **Heartbeat**: a periodic "system alive" notification (e.g., every session
  open) proves the pipeline works.

## Pseudo-code: notifier
```
def notify(alert):
    for ch in alert.channels:
        ok = ch.send(alert)
        if ok: record_delivery(alert, ch); break
    if not any_delivered: deadletter_queue.push(alert)
```

## Channel abstraction
```
channels/email.py   # SMTP
channels/push.py    # self-hosted push gateway / bot
channels/webhook.py # your endpoint
```
One interface (`send(alert) -> bool`), registry by name in config.

## Rules
- Critical alerts use ≥ 2 independent channels.
- Every channel has a health check (is it up?) in monitoring (CH_32/01).
- Notification content must be self-contained: what, when, severity, context.
