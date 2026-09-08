# Network Theory - RLC Resonance - Formulas

## Series RLC Resonance
```
Resonant frequency: f0 = 1/(2*pi*sqrt(LC))
Impedance at resonance: Z = R (minimum)
Current at resonance: I_max = V/R
Voltage across L: VL = I*XL = (V/R)*(w0*L) = Q*V
Voltage across C: VC = I*XC = Q*V

Quality factor: Q = (1/R)*sqrt(L/C) = w0*L/R = 1/(w0*R*C)
Bandwidth: BW = f0/Q = R/(2*pi*L)
Half-power points: f1, f2 where:
  f1 = f0 - BW/2 (approximately, for high Q)
  f2 = f0 + BW/2
```

## Parallel RLC Resonance
```
Impedance at resonance: Z = L/(R*C) (maximum) = R*Q^2
Current at resonance: minimum (draws minimum from source)

Quality factor: Q = R*sqrt(C/L) = R/(w0*L) = w0*R*C
Bandwidth: BW = f0/Q = 1/(2*pi*R*C)
```

## Universal Resonance Formulas
```
Characteristic impedance: Z0 = sqrt(L/C) [impedance level]
Quality factor: 
  Series: Q = Z0/R
  Parallel: Q = R/Z0

Selectivity: Higher Q -> narrower bandwidth -> more selective
```

## Quick Formula Table
| Parameter | Series RLC | Parallel RLC |
|-----------|-----------|--------------|
| Z at resonance | R (min) | L/RC = R*Q^2 (max) |
| f0 | 1/(2*pi*sqrt(LC)) | 1/(2*pi*sqrt(LC)) |
| Q | (1/R)*sqrt(L/C) | R*sqrt(C/L) |
| Q (alt) | w0*L/R | R/(w0*L) |
| BW | f0/Q = R/(2*pi*L) | f0/Q = 1/(2*pi*R*C) |
| At resonance | Z = R (resistive) | Z = L/(RC) (resistive) |

## Critical Frequencies
```
Lower half-power: f1 = f0*sqrt(1 + 1/(4Q^2)) - f0/(2Q)  (approx: f0 - BW/2)
Upper half-power: f2 = f0*sqrt(1 + 1/(4Q^2)) + f0/(2Q)  (approx: f0 + BW/2)
```
