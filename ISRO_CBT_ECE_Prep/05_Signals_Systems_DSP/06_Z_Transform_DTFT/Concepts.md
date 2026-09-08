# Z-Transform and DTFT - Concepts

## Z-Transform
```
X(z) = Sum[n=-inf to inf] x[n] z^(-n)
One-sided: Sum[n=0 to inf] x[n] z^(-n) for causal
Region of Convergence (ROC): values of z where sum converges
```

## Important Pairs
```
delta[n]        <->   1, ROC: all z
u[n]            <->   z/(z-1), ROC: |z|>1
a^n u[n]        <->   z/(z-a), ROC: |z|>|a|
n a^n u[n]      <->   az/(z-a)^2
a^n u[-n-1]     <->   -z/(z-a), ROC: |z|<|a|
n u[n]          <->   z/(z-1)^2
sin(w0 n) u[n]  <->   z sin(w0)/(z^2 - 2z cos(w0)+1)
cos(w0 n) u[n]  <->   z(z - cos(w0))/(z^2 - 2z cos(w0)+1)
```

## Properties
| Property | Signal | Transform |
|----------|--------|-----------|
| Linearity | ax+by | aX+bY |
| Right shift | x[n-m] | z^(-m)X(z) |
| Left shift | x[n+m] | z^(m)(X(z) - sum) |
| Scale | a^n x[n] | X(z/a) |
| Convolution | x*h | X(z)H(z) |
| Multiply by n | n x[n] | -z dX/dz |
| Time reversal | x[-n] | X(1/z) |
| Initial value | x[0] | lim z->inf X(z) |

## ROC Properties
1. ROC is always ring/annulus (or outside/inside circle)
2. Right-sided -> ROC outside: |z| > largest pole
3. Left-sided -> ROC inside: |z| < smallest pole
4. Two-sided -> annulus between poles
5. Causal + stable: all poles inside unit circle
6. ROC contains unit circle -> stable (for DT)

## Stability (Discrete)
```
Causal system stable iff all poles inside UNIT CIRCLE (|z|<1)
Non-causal stable iff poles outside unit circle
BIBO stable: Sum|h[n]| < inf -> ROC includes unit circle
```

## DTFT
```
X(e^(jw)) = Sum[n] x[n] e^(-jwn)
Inverse: x[n] = (1/2pi) integral[-pi to pi] X(e^(jw)) e^(jwn) dw
Relation: DTFT = Z-transform evaluated on unit circle (z=e^(jw)), IF unit circle in ROC
```

## DTFT Properties
```
Time shift: x[n-m] <-> e^(-jwm) X(e^jw)
Convolution: x*h <-> X*H
Modulation: x[n]e^(jw0n) <-> X(e^(j(w-w0)))
Parseval: Sum|x[n]|^2 = (1/2pi) integral |X|^2 dw
Periodicity: DTFT always period 2pi
```

## Inverse Z-Transform Methods
1. **Partial fractions** (like Laplace)
2. **Power series expansion** (long division, for causal)
3. **Contour integration** (residue)
4. **Inspection / table lookup**

---

## ISRO Key Points
- Pair: a^n <-> z/(z-a) - most common
- Shift property: x[n-m] <-> z^-m X(z)
- Stability: poles inside unit circle
- DTFT periodic in 2pi
- ROC determines causality/sidedness
- Convolution <-> multiplication
