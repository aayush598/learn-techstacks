# Oscillators - Formulas

## Barkhausen Criterion
```
|A * beta| >= 1 (for oscillation to start)
|A * beta| = 1 (for sustained oscillations)
Phase of (A * beta) = 0 or 360 degrees (n * 2pi)
```

## Wien Bridge Oscillator
```
Frequency: f0 = 1/(2*pi*R*C)
Required gain: A >= 3
Feedback fraction: beta = 1/3

For R1 = R2 = R, C1 = C2 = C:
  f0 = 1/(2*pi*R*C)
  At resonance: beta = 1/3, so A = 3 for oscillation
```

## RC Phase Shift Oscillator
```
Frequency: f0 = 1/(2*pi*R*C*sqrt(6))  [for 3 RC sections]
Required gain: A >= 29

For N identical RC sections:
  f0 = 1/(2*pi*R*C*sqrt(2*N))
  Required gain: A >= 2^N
```

## Colpitts Oscillator
```
Equivalent capacitance: Ceq = C1*C2/(C1+C2)
Frequency: f0 = 1/(2*pi*sqrt(L*Ceq))
Feedback fraction: beta = C1/C2 (or C2/C1)

For oscillation: gm*RL*C1/C2 >= 1
```

## Hartley Oscillator
```
Equivalent inductance: Leq = L1 + L2 + 2M  (with mutual inductance M)
Or: Leq = L1 + L2  (without mutual inductance)

Frequency: f0 = 1/(2*pi*sqrt(C*Leq))
Feedback fraction: beta = L1/L2
```

## Crystal Oscillator
```
Series resonance: fs = 1/(2*pi*sqrt(L*C))
Parallel resonance: fp = fs*sqrt(1 + C/Cm)

Quality factor: Q = (1/R)*sqrt(L/C) (very high: 10^4 to 10^6)
Frequency stability: ppm (parts per million)
```

## Clapp Oscillator
```
1/Ceq = 1/C1 + 1/C2 + 1/C3
Frequency: f0 = 1/(2*pi*sqrt(L*Ceq))
```

## Quick Reference Table
| Oscillator | Frequency Formula | Min Gain |
|------------|------------------|----------|
| Wien Bridge | 1/(2*pi*RC) | 3 |
| RC Phase Shift | 1/(2*pi*RC*sqrt(6)) | 29 |
| Colpitts | 1/(2*pi*sqrt(L*Ceq)) | gm*RL*C1/C2 >= 1 |
| Hartley | 1/(2*pi*sqrt(C*Leq)) | gm*RL*L1/L2 >= 1 |
| Crystal | fs = 1/(2*pi*sqrt(LC)) | Very high Q |
