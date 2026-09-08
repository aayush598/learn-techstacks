# Two-Port Networks - Formulas

## Z (open-circuit impedance)
```
[V1] = [Z11 Z12] [I1]
[V2]   [Z21 Z22] [I2]
Z11 = V1/I1@I2=0, Z12 = V1/I2@I1=0
Z21 = V2/I1@I2=0, Z22 = V2/I2@I1=0
```

## Y (short-circuit admittance)
```
[I1] = [Y11 Y12] [V1]
[I2]   [Y21 Y22] [V2]
Y11 = I1/V1@V2=0, Y12 = I1/V2@V1=0
Y21 = I2/V1@V2=0, Y22 = I2/V2@V1=0
```

## h (hybrid)
```
V1 = h11 I1 + h12 V2
I2 = h21 I1 + h22 V2
h11 = V1/I1@V2=0 (input imped, shorted)
h12 = V1/V2@I1=0 (reverse V ratio)
h21 = I2/I1@V2=0 (current gain)
h22 = I2/V2@I1=0 (output adm)
```

## ABCD
```
V1 = A V2 - B I2
I1 = C V2 - D I2
A = V1/V2@I2=0, B = -V1/I2@V2=0
C = I1/V2@I2=0, D = -I1/I2@V2=0
Cascade: [ABCD]_total = [ABCD]_1 * [ABCD]_2
```

## Conversion Z <-> Y
```
Delta = Z11 Z22 - Z12 Z21
Y11 = Z22/Delta, Y12 = -Z12/Delta
Y21 = -Z21/Delta, Y22 = Z11/Delta
```

## Reciprocity / Symmetry
```
Reciprocal (passive): Z12=Z21, Y12=Y21, h12=-h21, AD-BC=1
Symmetric: Z11=Z22, Y11=Y22, A=D
Both: reciprocal + symmetric
```

## Input/Output Impedance
```
Z_in (with load ZL): Zin = Z11 - Z12 Z21/(Z22+ZL)
     For ABCD: Zin = (A ZL + B)/(C ZL + D)
Z_out (with source Zs): 
     For ABCD: Zout = (D Zs + B)/(C Zs + A)
```

## Image Parameters
```
Z_image = sqrt(Z11/Z22 * (...
For matched: transmission without reflection
```

## Special Networks
```
Series Z: 
  Z11 = Z22 = Z, Z12 = Z21 = Z  (symmetric)
Series RLC simple cases
Shunt element:
  Y11 = Y12 = Y21 = Y22 = Y
```

## Quick Reference
| Quantity | Open | Short |
|----------|------|-------|
| Z params | yes (I2=0) | no |
| Y params | no | yes (V2=0) |
| h11 | - | yes |
| h12 | yes (I1=0) | - |
| h21 | - | yes |
| h22 | yes | - |
