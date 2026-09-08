# Transmission Lines - Formulas

## Lossless Line Parameters
```
Characteristic impedance: Z0 = sqrt(L/C)
Phase velocity: vp = 1/sqrt(L*C)
Wavelength: lambda = vp/f = 1/(f*sqrt(L*C))
Phase constant: beta = omega*sqrt(L*C) = 2*pi/lambda
Propagation constant: gamma = j*beta (lossless)
```

## Reflection Coefficient
```
At load: Gamma_L = (ZL - Z0)/(ZL + Z0)
At distance l from load: Gamma(l) = Gamma_L * e^(-2*gamma*l)
Magnitude: |Gamma| = |ZL - Z0|/|ZL + Z0|
Phase: angle(Gamma) = arctan...
```

## VSWR
```
VSWR = (1 + |Gamma|)/(1 - |Gamma|)
|Gamma| = (VSWR - 1)/(VSWR + 1)

VSWR = 1 when ZL = Z0 (matched)
VSWR = infinity when ZL = 0 or infinity (short or open)
```

## Input Impedance
```
General: Zin = Z0 * (ZL + j*Z0*tan(beta*l))/(Z0 + j*ZL*tan(beta*l))

Quarter-wave (l = lambda/4, beta*l = pi/2):
  Zin = Z0^2/ZL

Half-wave (l = lambda/2, beta*l = pi):
  Zin = ZL

Lossless line terminated in Z0:
  Zin = Z0 for any length (matched line)
```

## Quarter-Wave Transformer
```
Impedance transformation: Zin = Z0^2/ZL
Used for impedance matching
If Z0 = sqrt(Z1*Z2), matches Z1 to Z2
```

## Standing Wave Pattern
```
Vmax = Vincident * (1 + |Gamma|)   (at voltage maxima)
Vmin = Vincident * (1 - |Gamma|)   (at voltage minima)
Distance between maxima: lambda/2
Distance between first max and load: depends on Gamma phase
```

## Power Relations
```
Power delivered to load: PL = |V+|^2 * (1-|Gamma|^2)/(2*Z0)
Reflected power: PR = |V+|^2 * |Gamma|^2/(2*Z0)
Power dissipated in line: PD = PL*(e^(2*alpha*l) - 1)
```

## Lossy Line
```
alpha (attenuation) = R/(2*Z0) for low-loss line (R << wL)
Z0 = sqrt((R+jwL)/(G+jwC))
For very low loss: Z0 approximately sqrt(L/C)
```

## Quick Reference Table
| Condition | Gamma | VSWR | Zin |
|-----------|-------|------|-----|
| Matched (ZL=Z0) | 0 | 1 | Z0 |
| Open (ZL=inf) | 1 | inf | Open at load |
| Short (ZL=0) | -1 | inf | Short at load |
| Quarter-wave | Gamma_L rotated 90 deg | Same | Z0^2/ZL |
| Half-wave | Gamma_L | Same | ZL |
