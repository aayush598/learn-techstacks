# Network Theory - Superposition & Maximum Power - Formulas

## Superposition
```
Response = Sum over independent sources of (response with that source alone)
V_source deactivated -> short circuit
I_source deactivated -> open circuit
Dependent sources: NEVER deactivated
```

## Valid/Invalid
```
Valid for: linear circuits, compute V and I only
Invalid for: power P (not linear), nonlinear elements
```

## Maximum Power (resistive load)
```
Optimum: R_L = Rth
P_max = Vth^2/(4 Rth)
P_max = Isc^2 * Rth/4  (via Norton)
```

## Load Power Function
```
P_L(R_L) = Vth^2 R_L / (Rth + R_L)^2
dP_L/dR_L = 0 -> R_L = Rth
P_L(R_L) = Isc^2 * R_L * Rth / ... (Norton equivalent)
```

## Efficiency
```
eta = P_L / P_total = R_L/(Rth + R_L)
At R_L = Rth: eta = 50%
For large R_L: eta -> 100% (but power small)
```

## Complex Impedance (Conjugate Match)
```
Z_L = Zth^*  (conjugate matching)
For real R only: R_L = Rth
ZL = RL + jXL, Zth = Rth + jXth:
  RL = Rth, XL = -Xth
```

## Example: Thevenin Match
```
Given Vth = 12V, Rth = 6 ohms:
  R_L = 6 ohms
  P_max = 12^2/(4*6) = 144/24 = 6 W
  I = 12/12 = 1 A, P_L = I^2*R = 1*6 = 6W
  Efficiency = 50%
```

## Quick Reference
| Quantity | Formula |
|----------|---------|
| Optimum RL | Rth |
| Pmax (resistive) | Vth^2/(4Rth) |
| Efficiency at max | 50% |
| Conjugate match | ZL = Zth* |
| Superposition | sum of single-source responses |
| DEactivate V | short |
| DEactivate I | open |
