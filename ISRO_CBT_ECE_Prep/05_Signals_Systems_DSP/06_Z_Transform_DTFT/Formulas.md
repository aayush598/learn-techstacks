# Z-Transform and DTFT - Formulas

## Pairs (MEMORIZE)
```
delta[n]          <->  1
u[n]              <->  z/(z-1)      , |z|>1
a^n u[n]          <->  z/(z-a)      , |z|>|a|
na^n u[n]         <->  az/(z-a)^2
n u[n]            <->  z/(z-1)^2
a^n u[-n-1]       <->  -z/(z-a)     , |z|<|a|
sin(w0n)u[n]      <->  z sin(w0)/(z^2-2z cos(w0)+1)
cos(w0n)u[n]      <->  z(z-cos(w0))/(z^2-2z cos(w0)+1)
r^n sin(w0n)u[n]  <->  r z sin(w0)/(z^2 - 2 r z cos(w0)+ r^2)
```

## Properties
```
Z[x[n-m]] = z^(-m)X(z)
Z[a^n x[n]] = X(z/a)
Z[n x[n]] = -z dX(z)/dz
Z[x[n]*h[n]] = X(z)H(z)
Z[x[-n]] = X(1/z)
Initial value: x[0] = lim[z->inf] X(z)
Z[sum x[k] for k=0..n] = X(z) z/(z-1)  [accumulation]
```

## Shift (two-sided)
```
Right shift: Z[x[n-1]] = z^(-1) X(z)
Left shift:  Z[x[n+1]] = z X(z) - z x[0]
```

## Inverse via Partial Fractions
```
X(z) = z/((z-a)(z-b)) separate as:
  X(z)/z = A/(z-a) + B/(z-b)
  A = [X(z)/z]*(z-a) at z=a
Then x[n] = A a^n u[n] + B b^n u[n] (if causal)
```

## DTFT Core
```
X(e^jw) = Sum x[n] e^(-jwn)
x[n] = (1/2pi) integral[-pi,pi] X(e^jw)e^(jwn) dw
Period: 2pi
Evaluate Z at z=e^jw if ROC includes unit circle
```

## DTFT Pairs & Properties
```
delta[n]      <-> 1
a^n u[n]      <-> 1/(1 - a e^(-jw))   |a|<1
u[n]          <-> 1/(1-e^(-jw)) + pi Sum delta(w-2pi k)
1             <-> 2pi Sum delta(w-2pi k)
cos(w0n)      <-> pi[delta(w-w0)+delta(w+w0)] (periodic)
x[n-m]        <-> X e^(-jwm)
x[n]h[n]      <-> (1/2pi) X*H (periodic convolution)
Parseval: Sum|x[n]|^2 = (1/2pi) int|X|^2
```

## Stability / Causality Checks
```
Causal: x[n]=0 for n<0 (ROC: outside vs inside)
BIBO stable: |z|=1 within ROC, poles inside unit circle
Causal + stable: ALL poles |z|<1
```

## Quick Reference
| Op | Z | DTFT |
|----|----|------|
| shift m | z^-m X | e^-jwm X |
| conv | X·Z | X·H |
| scale a^n | X(z/a) | - |
| mult n | -z dX/dz | j dX/dw |
| reversal | X(1/z) | X(-w) |
