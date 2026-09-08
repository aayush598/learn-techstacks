# Coupled Circuits and Transformers - Formulas

## Mutual Inductance & Coupling
```
M = k sqrt(L1 L2)
k = M/sqrt(L1 L2)
0 <= k <= 1
```

## Voltage Equations
```
Coil1: V1 = L1 di1/dt + M di2/dt
Coil2: V2 = L2 di2/dt + M di1/dt
Sign of M term depends on dot convention (add if similar current direction into dots)
```

## Series
```
Aiding:  L_eq = L1 + L2 + 2M
Opposing: L_eq = L1 + L2 - 2M
```

## Parallel
```
Aiding:  L_eq = (L1 L2 - M^2)/(L1 + L2 - 2M)
Opposing: L_eq = (L1 L2 - M^2)/(L1 + L2 + 2M)
```

## Ideal Transformer
```
Turns ratio: n = N2/N1
V2 = n V1
I1 = n I2  (so I2 = I1/n)
Impedance: Z_in = Vi/Ii = Z_L / n^2
Power: V1 I1 = V2 I2
All referred by n or n^2
```

## Reflected Impedance
```
Primary load view: Z_in = Z_L/n^2  (Z_L on secondary)
Secondary source view: Z_out = Z_source * n^2
```

## Absolute Ideal conditions
```
k = 1, no losses, no magnetizing current
L1, L2 infinite ideally (finite in phasor but ratio fixed)
```

## Energy (passive)
```
W = (1/2)L1 i1^2 + (1/2)L2 i2^2 + M i1 i2
(-M if opposing polarity)
Passive if M^2 <= L1 L2 (realizability)
```

## Quick Reference
| Quantity | Formula |
|----------|---------|
| M | k sqrt(L1L2) |
| k | M/sqrt(L1L2) |
| Series aiding | L1+L2+2M |
| Series opp | L1+L2-2M |
| Ideal V2 | n V1 |
| Ideal I1 | n I2 |
| Zin (secondary load) | ZL/n^2 |
