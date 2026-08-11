# 04 — Volume Indicators

## Purpose
Measure participation and conviction behind price moves, and locate value zones.

## Volume indicator set
- **OBV** (On-Balance Volume): cumulative volume signed by close direction.
- **Volume-by-price / Volume profile**: distribution of volume across price
  levels → POC (point of control), high-volume nodes, low-volume nodes.
- **Volume delta / cumulative delta** (from tape aggressor side) — CH_03/02.
- **Money flow**: MFI = 100 − 100/(1+ positive money flow / negative), where
  MF = typical × volume.
- **Market-adjusted volume**: volume / index volume (relative participation).

## Volume profile construction (intraday)
1. Bin prices into levels (e.g., 0.1% steps or tick-grid).
2. Assign each bar's volume to its close/high-low range (or VWAP-weighted).
3. POC = level with max volume; high-volume nodes act as magnets/support;
   low-volume nodes = areas where price moves fast (thin).

## Pseudo-code: OBV
```
obv = 0
for bar:
    obv += bar.volume if close > close_prev else (-bar.volume if close < close_prev else 0)
```

## Pseudo-code: POC scan
```
hist = defaultdict(float)
for bar: hist[level(bar)] += bar.volume
poc = max(hist, key=hist.get)
support = [lv for lv in hist if hist[lv] > 0.6*hist[poc]]
```

## Usage guidance
- Breakouts into *thin* zones (low volume) run fast; breakouts into thick zones
  stall — use profile to pick targets (CH_22).
- Divergence: price new high + OBV/volume lower = weak; often precedes reversal.
- VWAP acts as intraday fair value; crossovers of price vs VWAP are common
  filters (especially institution-driven names).

## Rules
- Volume profile resets per session (intraday) unless modeling multi-day.
- Volume indicators confirm price; they do not replace it.
- Tape-derived deltas require aggressor side; degrade gracefully when absent.
