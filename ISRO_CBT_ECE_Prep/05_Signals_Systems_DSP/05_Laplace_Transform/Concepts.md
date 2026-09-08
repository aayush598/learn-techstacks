# Laplace Transform - Concepts

## Definition
```
X(s) = integral[0- to inf] x(t) e^(-s t) dt  (one-sided)
s = sigma + jw (complex frequency)
Region of Convergence (ROC): where integral converges
```

## Two-Sided vs One-Sided
- One-sided (unilateral): causal signals, initial conditions handled
- Two-sided (bilateral): needs ROC for uniqueness
- ISRO mostly uses one-sided for circuit analysis

## Important Pairs
```
delta(t)        <->  1, ROC: all s
u(t)            <->  1/s, ROC: Re(s) > 0
t u(t)          <->  1/s^2
t^n u(t)        <->  n!/s^(n+1)
e^(-at) u(t)    <->  1/(s+a), ROC: Re(s) > -a
sin(wt) u(t)    <->  w/(s^2+w^2)
cos(wt) u(t)    <->  s/(s^2+w^2)
e^(-at) sin(wt) <->  w/((s+a)^2+w^2)
e^(-at) cos(wt) <->  (s+a)/((s+a)^2+w^2)
```

## Properties
| Property | Signal | Transform |
|----------|--------|-----------|
| Linearity | ax+by | aX+bY |
| Time shift | x(t-t0)u(t-t0) | X(s)e^(-st0) |
| s-domain shift | x(t)e^(-at) | X(s+a) |
| Time scaling | x(at) | (1/a)X(s/a) |
| Differentiation | dx/dt | sX(s) - x(0-) |
| Second derivative | d2x/dt2 | s^2X(s)-sx(0)-x'(0) |
| Integration | integral x dt | X(s)/s |
| Convolution | x*h | X(s)H(s) |
| Initial value | x(0+) | lim s->inf sX(s) |
| Final value | x(inf) | lim s->0 sX(s) (if pole stable) |

## Initial & Final Value Theorems
```
x(0+) = lim[s->inf] s X(s)
x(inf) = lim[s->0] s X(s)  [only if stable, poles in LHP]
```

## Inverse Laplace
- Partial fraction expansion
- Distinct poles: X(s) = A/(s+p1) + B/(s+p2)...
- Repeated poles: partial fractions with extra terms
- Transfer function: H(s) = Y(s)/X(s)

## System Analysis
```
Transfer function: H(s) = N(s)/D(s)
Poles: D(s) = 0 (roots of denominator)
Zeros: N(s) = 0 (roots of numerator)
Stable if all poles in LHP (for causal)
Natural response: poles
Forced response: input poles
```

## ROC Rules (bilateral)
- Right-sided signal -> ROC right of rightmost pole
- Left-sided signal -> ROC left of leftmost pole
- Two-sided -> strip between poles
- Causal and stable -> all poles in LHP (ROC includes jw axis)

## Circuit Applications
```
R: Z = R
L: Z = sL
C: Z = 1/(sC)
Independent sources: transformed directly
Initial conditions: additional sources (I0/s or Li0)
```

---

## ISRO Key Points
- Pairs: e^-at <-> 1/(s+a); sin/cos standard
- Initial/final value theorems - frequent
- H(s) poles decide stability
- L: sL, C: 1/(sC) in s-domain for circuits
- Convolution in time = multiply in s
- Partial fractions for inverse
