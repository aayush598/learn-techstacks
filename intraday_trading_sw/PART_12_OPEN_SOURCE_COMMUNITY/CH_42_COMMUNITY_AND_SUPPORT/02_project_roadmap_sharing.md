# 02 — Project Roadmap Sharing

## Purpose
Share where the project is going, honestly, so users and contributors can plan
around it.

## What to share
- Roadmap (CH_44) with priorities and rough timeframes.
- Per-release: what's in, what's deferred, what was rejected and why.
- Status of the project's own production deployment (dogfooding): what the
  maintainers run, paper vs live, honest results (CH_37).

## Communication channels (self-hosted friendly)
- In-repo `ROADMAP.md` + release notes (canonical, versioned).
- Mailing list / self-hosted forum / chat (optional, per maintainer capacity).
- Issue labels `roadmap:` for tracking.

## Transparency principles
- Never overpromise timelines; state risks and dependencies.
- Results shared (own trading) include the same disclaimers and cost honesty as
  any report (CH_40).
- If a planned feature is dropped, say why (open process, CH_42/01).

## Pseudo-code: roadmap entry
```
roadmap:
  v0.5: { paper-trading complete, docs, CI }
  v1.0: { live support 1 market, graduated scale-up (CH_37/02) }
  v1.x: { more adapters, model registry UI, community strategies }
  never: [ guaranteed-profit claims, manipulation features ]   # policy
```

## Rules
- The roadmap is a living document updated with releases (CH_41/02).
- Honesty applies to the project itself: published backtests include costs and
  assumptions (CH_18/03).
- Community input shapes priorities through open discussion (CH_42/01).
