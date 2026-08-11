# 00 — Market Sources Catalog

## Purpose
Catalog every class of data source the system can use, with quality tiers,
so the data layer can pick sources by reliability and cost.

## Source classes
1. **Exchange-provided** — official feed/full-data products; most reliable, most costly.
2. **Broker APIs** — data comes as a side effect of having a brokerage account;
   good quality, single source, also the execution venue (CH_24).
3. **Free/open APIs** — public endpoints (documented per jurisdiction);
   good for learning/historic, rate-limited, may have gaps.
4. **Public file repositories** — downloadable historical datasets (daily/eod,
   some intraday); good for backtests, must validate freshness.
5. **Derived/alternative data** — news, economic calendar, sentiment (CH_12).

## What to record per source (catalog entry)
- instrument universe covered, granularity (tick/1m/5m/daily), history depth
- update latency (real-time vs delayed), reliability history
- license/redistribution terms (critical for open-source distribution!)
- authentication needed, rate limits, cost
- data quality reputation (gaps, corrections, adjusted vs raw)

## Recommended default stack (self-host friendly)
| Need | Primary choice | Backup |
|---|---|---|
| Historic intraday OHLCV | Broker/exchange API backfill | Public file repo |
| Real-time bars | Broker WebSocket feed | Free REST polling (fallback) |
| L2/book + tape | Broker/exchange feed (if provided) | None (degrade gracefully) |
| Corporate actions | Exchange/broker calendar | Manual curated file |
| News/calendar | Free/OS sources (CH_12) | Manual |

## Steps
1. Build `sources.yaml` catalog (never code data about sources into code).
2. Tag every stored record with its source id (data lineage, CH_00/01).
3. Add a health probe per source (latency + gap monitor) in CH_32.

## Rules
- Never silently mix sources for the same instrument/timeframe; label the origin.
- Check redistribution licenses before shipping any data with the open-source project.
- Design for a source to go away: all access behind the data-source interface.
