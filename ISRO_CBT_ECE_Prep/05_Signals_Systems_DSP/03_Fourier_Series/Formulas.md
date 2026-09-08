# Fourier Series - Formulas

## Exponential and Trigonometric
```
x(t) = Sum ck e^(j k w0 t),  w0 = 2*pi/T
ck = (1/T) integral[T] x(t) e^(-j k w0 t) dt

x(t) = a0 + Sum[ak cos(k w0 t) + bk sin(k w0 t)]
a0 = (1/T) integral x(t) dt
ak = (2/T) integral x(t) cos(k w0 t) dt
bk = (2/T) integral x(t) sin(k w0 t) dt
```

## Coefficient Conversions
```
ck = (ak - j bk)/2 (k>0); (ak + j bk)/2 (k<0); c0 = a0
ak = 2*Re(ck), bk = -2*Im(ck), a0 = c0
|ck| = (1/2)*sqrt(ak^2 + bk^2)
```

## Parseval's
```
P_avg = (1/T) integral |x|^2 dt = Sum |ck|^2
Also: P_avg = a0^2 + (1/2)Sum(ak^2 + bk^2)
```

## Common Series
```
Square wave (odd, A):
  x(t) = (4A/pi)[sin w0t + (1/3)sin 3w0t + (1/5)sin 5w0t + ...]

Triangle (odd):
  x(t) = (8A/pi^2)[sin w0t - (1/9)sin 3w0t + (1/25)sin 5w0t - ...]

Full-wave rectified sine:
  x(t) = (2A/pi)[1 + ...cos terms]
```

## Convergence Rate
```
Discontinuity (square): coefficients ~ 1/k
Continuous, corner (triangle): ~ 1/k^2
Smooth (parabolic): ~ 1/k^3
Faster decay = faster convergence, less Gibb's oscillation
```

## Gibb's Phenomenon
```
Overshoot ~ 9% of step height (never reduces with more terms)
Occurs at discontinuities
```

## Quick Reference
| Signal | Harmonics | Coeff decay |
|--------|-----------|-------------|
| Even | cosine | depends on shape |
| Odd | sine | depends on shape |
| Half-wave sym | ODD only | ~1/k (sq) or 1/k^2 (tri) |
| ? | all | - |
| Full-wave | even+DC | ~1/k^2 |
