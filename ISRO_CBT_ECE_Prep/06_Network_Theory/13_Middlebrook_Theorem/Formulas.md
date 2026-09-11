# Middlebrook Theorem - Formulas

## Extra Element Theorem (EET)
```
T(z) = T(0) * (1 + Z_n/Z) / (1 + Z_d/Z)

T(0): transfer function with extra element shorted/removed
Z_n: null output driving-point impedance (output = 0, element removed)
Z_d: driving-point impedance with input zeroed (element removed)
Z: value of the added element
```

## Equivalent Admittance Form
```
T(z) = T(0) * (1 + Y_d/Y) / (1 + Y_n/Y)  (using admittance)
Equivalent form with Y=1/Z
```

## Where:
```
Z_d = Req seen at element location with input source off
Z_n = Req seen at element location with output forced to zero
```

## N-Element (N-EET)
```
Generalizable: multiply correction factors for each extra element
T = T0 * PT (correction for each extra element)
Commonly 1-2 elements in practice
```

## Nulling the Output
```
"Null" = make the transfer output zero (not just grounded)
For a transfer of interest, null = 
  set dependent-variable (output) to zero via adjusting source
```

## Quick Reference
| Symbol | Meaning |
|--------|---------|
| T(0) | transfer with element shorted |
| Z_d | driving impedance (input zeroed) |
| Z_n | null impedance (output nulled) |
| Z | element value |
| Correction | (1+Zn/Z)/(1+Zd/Z) |

## Typical application: add capacitor C
```
To add compensation cap C:
  T = T0*(1+Zn*C... convert)
  Produces pole/zero, used in feedback compensation
```
