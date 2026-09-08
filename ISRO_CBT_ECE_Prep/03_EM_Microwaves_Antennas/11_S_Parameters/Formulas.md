# S-Parameters - Formulas

## S-Matrix Definition
```
b = S * a
where:
  b = reflected wave vector
  a = incident wave vector
  S = scattering matrix
```

## Two-Port Network
```
b1 = S11*a1 + S12*a2
b2 = S21*a1 + S22*a2

With port 2 matched (a2 = 0):
  S11 = b1/a1 = input reflection coefficient
  S21 = b2/a1 = forward transmission coefficient

With port 1 matched (a1 = 0):
  S12 = b1/a2 = reverse transmission coefficient
  S22 = b2/a2 = output reflection coefficient
```

## Power Relations
```
Incident power at port i: Pi = |ai|^2/2 (normalized to Z0)
Reflected power at port i: Pi_ref = |bi|^2/2

Power delivered to port i: Pi_delivered = (|ai|^2 - |bi|^2)/2
                        = |ai|^2 * (1 - |Sii|^2)/2

Transmitted power from port 1 to 2:
  P2 = |S21|^2 * |a1|^2 / 2
```

## Reciprocal Network
```
S = S^T (transpose)
S12 = S21

Example: Coupled lines, filters, dividers
```

## Lossless Network
```
S^H * S = I (conjugate transpose times itself = identity)
|S11|^2 + |S21|^2 = 1 (column 1)
|S12|^2 + |S22|^2 = 1 (column 2)

Also: |S11|^2 + |S12|^2 = 1 (row 1)
|S21|^2 + |S22|^2 = 1 (row 2)
```

## Matched Network
```
S11 = 0 (input matched to Z0)
S22 = 0 (output matched to Z0)
```

## Key Properties
```
For reciprocal lossless 2-port:
  S11 = S22 = 0 and |S21| = |S12| = 1
  (This is an ideal through-connection)

For reciprocal lossless 3-port:
  IMPOSSIBLE to have all ports matched
  (At least one port must be mismatched)
```

## Reference Impedance Conversion
```
If S-matrix measured in Z0, convert to Z0':
S' = (A - Gamma*inv(I - S*Gamma)) * inv(I - Gamma*S*Gamma)
where Gamma = diagonal matrix of reflection coefficients
```

## Quick Reference
| Network | S11 | S21 | S12 | S22 |
|---------|-----|-----|-----|-----|
| Matched load | 0 | - | - | - |
| Open circuit | 1 | - | - | - |
| Short circuit | -1 | - | - | - |
| Through (matched) | 0 | 1 | 1 | 0 |
| Isolator | 0 | 1 | 0 | 0 |
