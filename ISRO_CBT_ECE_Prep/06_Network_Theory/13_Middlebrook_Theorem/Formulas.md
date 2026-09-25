# Middlebrook Theorem - Formulas

## Extra Element Theorem (EET)
```
T(Z) = T(infinity) * (1 + Z_n/Z) / (1 + Z_d/Z)

T(infinity): transfer with the extra impedance open-circuited
T(0): transfer with the extra impedance short-circuited
Z_n: null double-injection driving-point impedance
Z_d: single-injection impedance with the input signal zeroed
Z: value of the added element
```

## Equivalent Forms
```
T(Z) = T(infinity) * (1 + Z_n/Z)/(1 + Z_d/Z)
T(Z) = T(0) * (1 + Z/Z_n)/(1 + Z/Z_d)
T(0) = T(infinity) * Z_n/Z_d
```

## Where:
```
Z_d = Req seen at element location with the input signal set to zero
Z_n = Null double-injection driving-point impedance
```

## N-Element (N-EET)
```
The theorem extends to several inserted elements.
The general bilinear correction includes higher-order cross terms,
so multiple-element corrections are not generally a simple product
of independent single-element factors.
```
```

## Null Double Injection
```
A null condition sets the relevant transfer response to zero.
It determines the null driving-point impedance needed by EET;
it is not generally the same as grounding the physical output node.
```

## Quick Reference
| Symbol | Meaning |
|--------|---------|
| T(infinity) | transfer with the extra impedance open |
| T(0) | transfer with the extra impedance shorted |
| Z_d | driving-point impedance with the input zeroed |
| Z_n | null double-injection impedance |
| Z | extra-element impedance |

## Typical application: add capacitor C
```
Z = 1/(sC)
T(Z) = T(infinity) * (1 + s C Z_n)/(1 + s C Z_d)
The correction factor introduces the associated pole-zero behavior
```
