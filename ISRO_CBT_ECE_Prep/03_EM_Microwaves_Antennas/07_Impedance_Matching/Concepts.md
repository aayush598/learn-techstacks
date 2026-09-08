# Impedance Matching - Concepts

## Why Match
- Maximum power transfer: ZL = Z0 (or conjugate)
- Minimal reflections -> low VSWR
- Reduced loss, improved signal integrity, no standing waves

## Reflection Basics
```
Gamma = (ZL - Z0)/(ZL + Z0)
VSWR = (1+|Gamma|)/(1-|Gamma|)
Matched: ZL = Z0 -> Gamma=0, VSWR=1 (ideal)
Mismatch: |Gamma|>0, VSWR>1
```

## Matching Techniques
1. **Quarter-wave transformer**
2. **Single-stub tuner**
3. **Double-stub tuner**
4. **Lumped L-network (Pi, T)**
5. **Tapered line**
6. **Smith chart-based design**

## Quarter-Wave Transformer
```
Matching Z0 (source) to ZL using quarter-wave (lambda/4) section:
  Z_q = sqrt(Z0 * ZL)
  (for real Z values)
Advantages: simple, broadband-ish
Disadvantages: only real Z matching, lambda/4 physical length
```

## Single-Stub Tuner
- Stub = shorted (or open) length of transmission line
- Placed at distance d from load
- 1) Move to point where real part of admittance = Y0
- 2) Stub cancels remaining susceptance
- Variable with Smith chart
- Two solutions (open/short stub)

## Double-Stub
- Two variable stubs separated by fixed distance (lambda/8 or 3lambda/8)
- Easier to tune (adjustable), limited range

## Lumped L-Match (RF)
```
For R_s < R_L, series L then shunt C (2-element L network)
Q controls bandwidth; higher Q = narrower
Formula from source/load impedance
```

## Stub vs Transformer
| Method | Type | Bandwidth | Application |
|--------|------|-----------|-------------|
| Quarter-wave | lambda/4 | narrow | fixed real loads |
| Single stub | reactive | narrow | general ZL |
| Double stub | reactive | narrow | adjustable |
| Taper | gradual | wide | broadband |
| Lumped-L | reactances | Q-dependent | lumped circuits |

## Tapered Line / Matching
- Continuous transition in impedance (exponential, Klopfenstein)
- Broadband impedance matching
- Used for waveguide/coaxial transitions

## Applications
- Antenna feeds (match antenna to line)
- Amplifier input/output (50 ohm match)
- Power combiner/dividers
- Microwave circuit design

---

## ISRO Key Points
- Quarter-wave: Z_q = sqrt(Z0 ZL), for real Z
- Match: ZL = Z0 -> VSWR=1, Gamma=0
- Smith chart: move on constant |Gamma| to real=Y0, then stub
- Single-stub: distance + stub length
- L-network: series + shunt reactive
