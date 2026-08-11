# 00 — News Ingestion

## Purpose
Bring scheduled and breaking news into the system as structured events, tagged
by time, so strategies can react to or avoid them.

## News types
- **Scheduled (known time)**: economic releases, earnings, index changes,
  expirations, holidays. Pre-event uncertainty is predictable.
- **Breaking (unknown time)**: headlines, company news, market-moving tweets.
  Requires real-time ingestion.

## Design
1. **Source adapters** (calendar feeds, RSS/API, optionally a curated list) —
   each behind `NewsSource` interface.
2. **Normalization** → event record: `{ts, source, headline, tags[], symbols[],
   sentiment?, url, category}`.
3. **Store** in a local events table (SQLite) with the same validation discipline.
4. **Publish** typed `NEWS_EVENT` to the pipeline with precise receive timestamps.

## Scheduled-event handling
- Pre-load the economic calendar for the day.
- Compute minutes-to-event as a feature (CH_09/03); many strategies pause
  or reduce size in the minutes around major releases.

## Pseudo-code: news event record
```
record = { ts_received: now, ts_published: src.ts,
           headline: normalized, tags: extract_tags(headline),
           symbols: resolve_symbols(headline), category: classify() }
```

## Rules
- Timestamps matter: record both publisher time and receive time (latency metric).
- Never auto-trade on raw headlines without content filtering and confirmation —
  news is noisy and sometimes stale by arrival.
- Tag news events so strategies can *choose* to be aware or blind (configurable).
