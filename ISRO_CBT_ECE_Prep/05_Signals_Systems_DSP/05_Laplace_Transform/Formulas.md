# Laplace Transform - Formulas

## Pairs (MEMORIZE)
```
delta(t)          <->  1
u(t)              <->  1/s
t u(t)            <->  1/s^2
t^n u(t)          <->  n!/s^(n+1)
e^(-at) u(t)      <->  1/(s+a)
sin(wt) u(t)      <->  w/(s^2+w^2)
cos(wt) u(t)      <->  s/(s^2+w^2)
e^(-at)sin(wt)    <->  w/((s+a)^2+w^2)
e^(-at)cos(wt)    <->  (s+a)/((s+a)^2+w^2)
r(t) = t u(t)     <->  1/s^2
```

## Properties
```
L[ax(t)+by(t)] = aX(s)+bY(s)
L[x(t-t0)u(t-t0)] = X(s)e^(-st0)
L[e^(-at)x(t)] = X(s+a)
L[dx/dt] = sX(s) - x(0-)
L[d2x/dt2] = s^2X(s) - s x(0-) - x'(0-)
L[integral x dtau] = X(s)/s
L[x(t)*h(t)] = X(s)H(s)
L[x(at)] = (1/a)X(s/a)
```

## Value Theorems
```
Initial:  x(0+) = lim[s->inf] s X(s)
Final:    x(inf) = lim[s->0] s X(s),  requires poles in LHP
```

## Partial Fractions
```
Distinct poles: X(s) = A/(s+p1) + B/(s+p2)
  A = (s+p1)X(s) evaluated at s=-p1
Repeated: X(s) = A/(s+p) + B/(s+p)^2 + ...
  Use differentiation for repeated coefficients
Complex conjugate poles: 
  X(s) = (As+B)/((s+a)^2+w^2) -> exponential * sin/cos
```

## Circuit Elements (s-domain)
```
Impedance: Z_R=R, Z_L=sL, Z_C=1/(sC)
Admittance: Y_R=1/R, Y_L=1/(sL), Y_C=sC
Initial condition L: source Li(0-)
Initial condition C: source Vc(0-)/s
```

## Table: transform of derivative chains
```
For y'' + 3y' + 2y = x:
  s^2Y - s y(0) - y'(0) + 3(sY - y(0)) + 2Y = X(s)
  Y(s)(s^2+3s+2) = X(s) + [s y(0) + y'(0) + 3 y(0)]
```

## Quick Reference (ROC)
```
Pair              ROC
1/s               Re(s)>0
1/(s+a)           Re(s)>-a
w/(s^2+w^2)       Re(s)>0
s/(s^2+w^2)       Re(s)>0
1/(s+a)^2         Re(s)>-a
```

## Solving Circuit with L.T.
1. Transform to s-domain with initial conditions
2. Solve algebraically for V(s) or I(s)
3. Partial fractions
4. Inverse transform (table lookup)
```
