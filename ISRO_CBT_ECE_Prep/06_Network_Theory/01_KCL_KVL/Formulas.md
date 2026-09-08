# Network Theory - KCL, KVL Formulas

## Ohm & Power
```
V = IR
P = VI = I^2 R = V^2/R
Energy: W = integral P dt
```

## KCL
```
Sum I_in = Sum I_out  (at node)
Sum I = 0 (with sign)
```

## KVL
```
Sum V_rise = Sum V_drop  (around loop)
Sum V = 0 (with sign)
```

## Series/Parallel
```
Series R: Req = Sum Rk
Parallel R: 1/Req = Sum 1/Rk
Two parallel: Req = R1 R2/(R1+R2)
N equal parallel: Req = R/N
```

## Dividers
```
Voltage divider: V_Rk = V_s Rk / (R1+R2+...)
Current divider (2 parallel): I_R1 = I_s R2/(R1+R2)
Current divider: I_Rk = I_s R_total_parallel/Rk
```

## Delta-Wye
```
Y->Delta: R_ab = Ra+Rb + RaRb/Rc; (R_bc, R_ac cycl.) 
Delta->Y: Ra = R_ab R_ac/(R_ab+R_bc+R_ac)
Balanced: R_delta = 3 R_Y
```

## Inductors/Capacitors (DC steady state)
```
DC: L -> short (V=0), C -> open (I=0)
Series C: 1/Ceq = Sum 1/Ck
Parallel C: Ceq = Sum Ck
Series L: Leq = Sum Lk; Parallel L: 1/Leq = Sum 1/Lk
```

## Time constant
```
RC: tau = RC
RL: tau = L/R
(t for 63.2% in 1 tau in first order, to 5 tau ~99.3%)
```

## Quick Frequents
| Computation | Formula |
|-------------|---------|
| 2 parallel R | R1 R2/(R1+R2) |
| N parallel equal | R/N |
| Balanced del-Y | 3x |
| C series | harmonic sum |
| Divider V | V*Rk/Sum |
| Divider I (2) | Is*R_other/Sum |
