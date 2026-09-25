# Network Theory - Driving Point Impedance - Concepts

## Driving Point Impedance (Z(s))
- Impedance seen looking into a single port of a network
- Z(s) = V(s)/I(s) (ratio of Laplace-transformed voltage/current at port)
- For network with all other sources zeroed

## Properties of Driving-Point Impedance
- For passive RLC networks: Z(s) is a **positive real function**
- Real rational function: coefficients real
- Re[Z(jw)] >= 0 for passive (real part non-negative)
- Z(s) has no right-half-plane poles; simple imaginary-axis poles must have positive residues
- Zeros of a positive-real function may occur in the right-half-plane
- Non-real poles and zeros occur in conjugate pairs because the coefficients are real

## Positive Real (PR) Function Conditions
1. Z(s) rational with real coefficients
2. Z(s) real for real s
3. Re[Z(s)] >= 0 for Re[s] >= 0 (in the RHP, real part >=0)
4. Pole restrictions: no RHP poles; any imaginary-axis poles are simple with positive residues

## Realization
```
Z(s) = N(s)/D(s), with degree difference <= 1
Realizable as RLC ladder / Cauer / Foster networks
```

## Circuits
```
Series R: Z = R
Series L: Z = sL
Capacitor: Z = 1/(sC)
RLC series: Z = R + sL + 1/(sC)
Parallel combinations (reciprocal sum)
```

## Resonance types from Z
- Series resonance: Z minimum (imaginary 0, real=R)
- Parallel resonance: Z maximum (antiresonance)

## Applications
- Network synthesis (realize given Z(s))
- Impedance matching
- Filter design
- Stability checking (PR function => passive)

---

## ISRO Key Points
- Z(s) = V/I at port
- Positive real function for passive networks
- Re[Z] >= 0 in RHP
- R, sL, 1/sC elements
- Ladder/Foster realizations
