# Oscillators - Concepts

## Barkhausen Criteria for Oscillation
1. Loop gain magnitude: |A*beta| >= 1
2. Loop phase shift: angle(A*beta) = 0 or 360 degrees (n*360)

### At startup: |A*beta| > 1 (to build up oscillations)
### At steady state: |A*beta| = 1 (for sustained oscillations)

---

## Wien Bridge Oscillator
- Uses RC feedback network (lead-lag network)
- Frequency: f = 1/(2*pi*R*C)
- Uses non-inverting amplifier with gain >= 3
- Beta = 1/3 at resonant frequency
- Low distortion sine wave output
- Most commonly used audio oscillator

### Circuit:
- Series RC arm + Parallel RC arm form voltage divider
- Feedback fraction beta = 1/3 at f0
- Amplifier gain A >= 3 for oscillation (A*beta >= 1)

## RC Phase Shift Oscillator
- Uses 3 RC sections (each providing 60 degrees phase shift)
- Total phase shift = 180 degrees (from network) + 180 (from inverting amp) = 360
- Frequency: f = 1/(2*pi*R*C*sqrt(6))
- Required gain: A >= 29 (for 3-section network)
- Alternative: f = 1/(2*pi*RC*sqrt(2N)) for N sections

## Colpitts Oscillator
- Uses two capacitors and one inductor in tank circuit
- Frequency: f = 1/(2*pi*sqrt(L*Ceq)) where Ceq = C1*C2/(C1+C2)
- Feedback fraction: beta = C1/C2 (or C2/C1 depending on connection)
- Uses BJT or FET as amplifying element
- Good for high frequency applications (MHz range)

## Hartley Oscillator
- Uses two inductors and one capacitor in tank circuit
- Frequency: f = 1/(2*pi*sqrt(C*Leq)) where Leq = L1 + L2 + 2M (with mutual inductance)
- Feedback fraction: beta = L1/L2 (or L2/L1)
- Similar to Colpitts but with inductors instead of capacitors

## Crystal Oscillator
- Uses quartz crystal as frequency determining element
- Crystal has series and parallel resonant frequencies
- Very high Q-factor (10^4 to 10^6)
- Excellent frequency stability (ppm accuracy)
- Frequency: approximately fs (series resonance)
- Pierce oscillator uses crystal in feedback path

## Clapp Oscillator
- Modified Colpitts with additional capacitor in series with inductor
- Frequency: f = 1/(2*pi*sqrt(L*Ceq)) where 1/Ceq = 1/C1 + 1/C2 + 1/C3
- Better frequency stability than Colpitts

---

## ISRO Key Points
- Wien bridge: f = 1/(2*pi*RC), gain needed >= 3
- RC phase shift: f = 1/(2*pi*RC*sqrt(6)), gain needed >= 29
- Colpitts: Uses capacitive divider for feedback
- Hartley: Uses inductive divider for feedback
- Crystal oscillator: Highest frequency stability
- Barkhausen: |A*beta| = 1, phase = 0 or 360 degrees
