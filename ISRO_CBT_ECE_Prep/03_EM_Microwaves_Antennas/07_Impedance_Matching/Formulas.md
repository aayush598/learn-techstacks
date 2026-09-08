# Impedance Matching - Formulas

## Reflection & VSWR
```
Gamma = (ZL - Z0)/(ZL + Z0)
VSWR = (1+|Gamma|)/(1-|Gamma|)
Return loss (dB) = -20 log10 |Gamma|
Mismatch loss (dB) = -10 log10(1 - |Gamma|^2)
```

## Quarter-Wave Transformer
```
Z_q = sqrt(Z0 * ZL)   (real ZL)
Electric length: lambda/4 (90 degrees)
At lambda/4: Z_in = Z_q^2/ZL  -> if Z_q=sqrt(Z0 ZL): Z_in = Z0
```

## Series section to match
```
Given Z_in needed; solve via Smith chart or:
Input impedance at distance d:
  Z_in = Z0 (ZL + j Z0 tan(beta d))/(Z0 + j ZL tan(beta d))
```

## Single Stub (Admittance approach)
```
Step 1: Move from load to point on constant |Gamma| where
  Re(y) = 1  (normalized conductance = 1)
  This gives stub distance d1
Step 2: Read remaining susceptance B_stub = -Im(y)
  Shorted stub length:  l = (1/beta) atan(Y0/B_stub)... (tune)
  For shorted stub input susceptance: y_in = -j cot(beta l)
    -> l to give B cancels
```

## Lumped L-Match
```
Two reactances (L, C):
  Q = sqrt(RL/Rs - 1)  (for RL>Rs)
  Xs = Q*Rs, Xp = RL/Q  (approx)
Bandwidth ~ proportional 1/Q
```

## Return/Mirror
```
Power delivered to matched load = maximum
Condition: Z_in = Z0* (conjugate for complex)
```

## Quick Reference
| Quantity | Use |
|----------|-----|
| Z_q | sqrt(Z0 ZL) |
| Gamma | (ZL-Z0)/(ZL+Z0) |
| VSWR | (1+G)/(1-G) |
| Return loss | -20log|G| |
| Single stub | Re(y)=1 then cancel B |
| L-match Q | sqrt(RL/Rs - 1) |
