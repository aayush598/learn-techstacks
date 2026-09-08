# Network Theory - RLC Resonance - Concepts

## Series RLC Resonance
- At resonance: XL = XC (inductive reactance = capacitive reactance)
- Impedance: Z = R (minimum)
- Current: I = V/R (maximum)
- Voltage across L and C: VL = VC = Q*V (larger than input!)
- Resonant frequency: f0 = 1/(2*pi*sqrt(LC))

### Key Parameters:
```
Resonant frequency: f0 = 1/(2*pi*sqrt(LC))
Impedance at resonance: Z = R (minimum)
Quality factor: Q = (1/R)*sqrt(L/C) = w0*L/R = 1/(w0*R*C)
Bandwidth: BW = f0/Q = R/(2*pi*L)
Half-power frequencies: f1, f2 where amplitude = peak/sqrt(2)
  BW = f2 - f1
Selectivity = Q (higher Q = more selective/narrower BW)
```

---

## Parallel RLC Resonance
- At resonance: susceptances cancel
- Impedance: Z = L/(R*C) (maximum)
- Current: minimum (antiresonance)
- Quality factor: Q = R*sqrt(C/L) = R/(w0*L)

### Key Parameters:
```
Resonant frequency: f0 = 1/(2*pi*sqrt(LC)) (same for series and parallel)
Impedance at resonance: Z = L/(R*C) (maximum)
Quality factor: Q = R*sqrt(C/L)
Bandwidth: BW = f0/Q = 1/(2*pi*R*C)
```

---

## Q-Factor Significance
- Higher Q = narrower bandwidth, more selective
- Q = w0*L/R (series) = R/(w0*L) (parallel)
- Q is dimensionless, typically 1-100 in practical RLC circuits

## Applications
- Band-pass filters
- Tuned amplifiers
- Radio receivers (frequency selection)
- Oscillators (high Q = stable frequency)
- Impedance matching

---

## ISRO Key Points
- Series: Z minimum at resonance (current max)
- Parallel: Z maximum at resonance (current min)
- f0 same for both: 1/(2*pi*sqrt(LC))
- Series Q = w0*L/R, Parallel Q = R/(w0*L)
- These are OPPOSITE (series uses R in numerator, parallel uses R in denominator)
