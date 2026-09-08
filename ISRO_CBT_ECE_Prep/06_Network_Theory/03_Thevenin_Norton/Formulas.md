# Network Theory - Thevenin and Norton - Formulas

## Thevenin
```
V_th = V_oc  (open circuit voltage, load removed, independent sources on)
R_th = V_oc / I_sc   OR  compute with sources deactivated
```

## Norton
```
I_n = I_sc  (short circuit current)
R_n = R_th
```

## Relations
```
V_th = I_n * R_th
I_n = V_th / R_th
R_n = R_th
```

## Maximum Power Transfer
```
Optimum load: R_L = R_th  (matched load)
P_max = V_th^2 / (4 R_th) = I_n^2 * R_th / 4
Efficiency at max power = 50%
For varying R_L: P(R_L) = V_th^2 R_L / (R_th + R_L)^2
  Max when dP/dR_L = 0 -> R_L = R_th
```

## Source Transform
```
Voltage source V with R in series  <->  Current source I=V/R in parallel with R
Both produce identical terminal behavior
```

## Deactivation
```
Voltage source -> short (0 V)
Current source -> open (0 A)
Dependent sources: NOT deactivated
```

## Dependent Source Rth
```
Apply test source at terminals:
  R_th = V_test / I_test
Or: R_th = V_oc / I_sc
```

## Tracking signs
```
Value        Reference
V_oc         positive terminal -> through load (to + ref)
I_sc         terminal -> out positive reference
```

## Quick Reference
| Quantity | Formula |
|----------|---------|
| Vth | V_oc |
| Rth | V_oc/I_sc or deactivated circuit |
| In | I_sc |
| Rn | Rth |
| Match load | RL = Rth |
| Pmax | Vth^2/(4Rth) |
| eff at Pmax | 50% |
