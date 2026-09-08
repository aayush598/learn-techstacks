# Fourier Series - Concepts

## Fourier Series Representation
Any periodic signal can be expressed as a sum of harmonically related sinusoids.
- Period T, fundamental frequency w0 = 2*pi/T
- Harmonic frequencies: k*w0 for integer k

## Exponential Form
```
x(t) = Sum[k=-inf to inf] ck * e^(j k w0 t)
ck = (1/T) integral over one period x(t) e^(-j k w0 t) dt
```

## Trigonometric Form
```
x(t) = a0 + Sum[ak*cos(k w0 t) + bk*sin(k w0 t)]
a0 = (1/T) integral x(t) dt  [DC value]
ak = (2/T) integral x(t) cos(k w0 t) dt
bk = (2/T) integral x(t) sin(k w0 t) dt
```

## Relationship Between Forms
```
ck = (ak - j*bk)/2 for k>0, ck = (ak + j*bk)/2 for k<0
c0 = a0
For real signal: ck and c(-k) are conjugates
```

## Symmetry Simplifications (Real x(t))
| Symmetry | Condition | Coeffs Present |
|----------|-----------|----------------|
| Even | x(t)=x(-t) | Only cos terms (ak, ck real) |
| Odd | x(t)=-x(-t) | Only sin terms (bk, ck imaginary) |
| Half-wave | x(t)=-x(t+T/2) | Only ODD harmonics |
| Even + half-wave | both | Odd cos harmonics |
| Odd + half-wave | both | Odd sin harmonics |

## Parseval's Theorem
```
(1/T) integral |x(t)|^2 dt = Sum[k=-inf to inf] |ck|^2
Average power in time domain = sum of harmonic powers
```

## Common Periodic Signals (Fourier Series)
1. **Square wave (amplitude A, 50% duty)**
   - Only odd harmonics, coefficients ~1/k
   - ck ~ (2A)/(pi*k) for odd k
   - Fourier: (4A/pi)[sin(w0t) + (1/3)sin(3w0t) + (1/5)sin(5w0t)+...]
2. **Triangle wave**
   - Coefficients ~1/k^2 (converges faster)
3. **Half-wave rectified sine**
   - Has DC + all harmonics

## Gibb's Phenomenon
- At discontinuities, Fourier series overshoots by ~9%
- Overshoot doesn't decrease with more terms
- Ringing occurs at step edges

## Convergence Conditions (Dirichlet)
1. x(t) has finite number of discontinuities in one period
2. Finite number of maxima/minima
3. Absolutely integrable in one period
(Square wave satisfies these)

---

## ISRO Key Points
- Half-wave symmetry -> only ODD harmonics (very common question)
- Even -> cosine only, Odd -> sine only
- DC: c0 = a0 = average value
- Parseval: time power = freq power
- Square wave has ~1/k falloff, triangle ~1/k^2
