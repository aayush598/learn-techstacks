# BJT and FET Amplifiers - Formulas

## BJT relations
```
gm = IC/VT = IC/26mV
r_pi = beta/gm = VT/IB = beta*VT/IC
r_o = VA/IC  (Early)
IC = beta IB = alpha IE
alpha = beta/(beta+1)
IC ~ IE (large beta)
```

## CE Amplifier
```
Av = -gm*(RC || r_o || RL)
Av(no load) = -gm*(RC || r_o)
Zi = RB || r_pi
Zo = RC || r_o
Phase: 180 deg (inverting)
Current gain = beta (approx)
```

## CC (Emitter follower)
```
Av = gm RE/(1 + gm RE) ~ 1 (slightly <1)
Zi (high) = r_pi + (1+beta)RE
Zo (low) = RE || (r_pi+Rs)/(1+beta)
Buffer: current gain high, voltage ~1
```

## CB
```
Av = gm*(RC || r_o)  (positive, ~high)
Zi = 1/gm (low)
Current gain ~ 1
High frequency use
```

## MOSFET amplifiers
```
gm = 2 ID/Vov = sqrt(2 kn ID)
  Vov = Vgs - Vt
r_o = 1/(lambda ID) = VA/ID

Common Source: Av = -gm(RD || r_o || RL)
Common Drain: Av ~ 1 (follower)
Common Gate: Av = gm(RD||r_o)
```

## Miller Effect (CS/CE with Cgd/Cbc)
```
Cm = Cgd*(1 + Av)
Input high-freq pole reduced by high Av
Cascode lowers Miller cap (Av of driver low)
```

## DC Bias (self-bias, CE)
```
VBB = VCC*R2/(R1+R2)  (divider)
VB = VBB (ignoring base current)
VE = VB - VBE
IE = VE/RE
IC ~ IE, VCE = VCC - IC(RC+RE)
Q-point stabilized by RE (negative feedback)
```

## Gain-Bandwidth
```
GBW = Av * BW (constant for many amps)
Higher gain -> lower bandwidth
```

## Quick Reference
| Config | Av | Zi | Zo | Phase |
|--------|-----|----|----|-------|
| CE | -gmRC | med | high | 180 |
| CB | high | low | high | 0 |
| CC | ~1 | high | low | 0 |
| CS | -gmRD | high | high | 180 |
| CD | ~1 | high | low | 0 |
| CG | high | low | high | 0 |
