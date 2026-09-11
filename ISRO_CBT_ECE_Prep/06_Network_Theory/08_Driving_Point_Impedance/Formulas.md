# Network Theory - Driving Point Impedance - Formulas

## Basic Elements
```
R: Z = R
L: Z = sL
C: Z = 1/(sC)
Series: Z_total = Sum Zi
Parallel: 1/Z = Sum (1/Zi)
```

## RLC
```
Series RLC: Z = R + sL + 1/(sC)
  Resonance: w0 = 1/sqrt(LC)
  Z(jw0) = R (min)
Parallel RLC: 
  Z = 1/(1/R + 1/(sL)+ sC)  (combined)
  At resonance: Z -> L/(RC) max
```

## Positive Real Function Test
```
Real coefficients
Z real for real s
Re[Z(s)] >= 0 for Re[s]>=0
Pole conditions:
  no RHP poles
  imaginary-axis poles simple, + real residues
  degree diff <= 1
```

## Foster (LC) realization
```
Z(s) = k/s + k_inf s + Sum (2ki s/(s^2+w_i^2))
Foster I: series of parallel LC
Foster II: ...
Only L,C (no R) - pure reactance, all poles on jw axis
```

## Cauer (RLC ladder)
```
Continued fraction expansion of Z(s)
Cauer I: alternating series L / shunt C
Impedance ladder
```

## Cycle: given Z(s) -> synthesize
```
Check PR property
Decompose partial fractions
Realize as Foster/Cauer with R, L, C
```

## Quick Reference
| Element | Z(s) |
|---------|------|
| R | R |
| L | sL |
| C | 1/sC |
| Series RLC | R+sL+1/sC |
| PR req | ReZ>=0 in RHP |
| Foster | LC only |
| Cauer | ladder |
