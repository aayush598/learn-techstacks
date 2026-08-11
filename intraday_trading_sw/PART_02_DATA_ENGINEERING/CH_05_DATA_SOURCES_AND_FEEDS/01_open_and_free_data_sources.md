# 01 — Open and Free Data Sources

## Purpose
List the *kind* of open/free sources to consider and how to integrate them
responsibly. (Exact endpoints change often; treat them as configuration.)

## Categories to evaluate
- **Public market-data APIs** (free tiers with rate limits). Decide per your
  jurisdiction and market.
- **Exchange-provided public datasets** (some exchanges publish daily/eod files).
- **Open data portals** for macro/calendar items (economic events, indices).
- **Community datasets** — verify quality; treat as untrusted until validated.

## Integration guidance (vendor-neutral)
1. Read the source's documentation and license before writing code.
2. Abstract the source behind `DataSource` interface (fetch → normalized frame).
3. Implement rate-limit handling and retry-with-backoff (CH_06).
4. Cache everything locally; free sources are for *acquisition*, not runtime
   dependency — the store is the runtime source of truth (CH_08).
5. Tag each batch with fetch timestamp and source id; validate on ingest (CH_07).

## Pseudo-code: generic free source adapter
```
class FreeSource(DataSource):
    def fetch(self, symbol, start, end):
        data = http_get(self.url(symbol, start, end))   # urllib, retry/backoff
        return normalize_to_bars(data)
    # normalize: map fields -> (ts, open, high, low, close, volume), UTC start-stamps
```

## Risks and mitigations
- Rate limits → token-bucket client + conservative defaults.
- Data gaps/corrections → validation + gap detector on ingest (CH_07).
- Delayed data → mark `is_delayed=True`; never use delayed data for live decisions.
- License change → pin a snapshot locally and document the license.

## Rules
- Free data is for research/backtest; live trading decisions require a feed whose
  latency and reliability you trust.
- Always store the license text next to the data directory.
