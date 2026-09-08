# Transmission Lines - Concepts

## Transmission Line Parameters
- **R**: Resistance per unit length (ohm/m)
- **L**: Inductance per unit length (H/m)
- **G**: Conductance per unit length (S/m)
- **C**: Capacitance per unit length (F/m)

## Characteristic Impedance (Z0)
- Ratio of voltage to current of a single wave
- Z0 = sqrt((R+jwL)/(G+jwC))
- For lossless line: Z0 = sqrt(L/C)
- Independent of line length

## Propagation Constant
- gamma = alpha + j*beta
- alpha = attenuation constant (Np/m)
- beta = phase constant (rad/m)
- For lossless: gamma = j*beta, alpha = 0

## Lossless Transmission Line
```
Z0 = sqrt(L/C)
vp = 1/sqrt(L*C) (phase velocity)
lambda = vp/f (wavelength)
beta = omega*sqrt(L*C) = 2*pi/lambda
```

## Reflection Coefficient
- Gamma = (ZL - Z0)/(ZL + Z0)
- At load end: |Gamma| ranges from 0 (matched) to 1 (open/short)
- Gamma = 0 when ZL = Z0 (matched, no reflection)

## VSWR (Voltage Standing Wave Ratio)
- VSWR = (1 + |Gamma|)/(1 - |Gamma|)
- VSWR ranges from 1 (matched) to infinity (open/short)
- For matched load: VSWR = 1

## Input Impedance
- Zin = Z0 * (ZL + j*Z0*tan(beta*l))/(Z0 + j*ZL*tan(beta*l))
- Quarter-wave transformer: Zin = Z0^2/ZL (at l = lambda/4)
- Half-wave line: Zin = ZL (at l = lambda/2)

---

## ISRO Key Points
- Z0 = sqrt(L/C) for lossless line (most important formula)
- Reflection coeff: Gamma = (ZL-Z0)/(ZL+Z0)
- VSWR = (1+|Gamma|)/(1-|Gamma|)
- Quarter-wave: Zin = Z0^2/ZL (impedance inversion)
- Half-wave: Zin = ZL (impedance repetition)
