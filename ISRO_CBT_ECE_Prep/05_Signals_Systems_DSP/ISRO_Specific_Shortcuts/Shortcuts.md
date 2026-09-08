# Signals and Systems - Quick Solving Shortcuts

## Signal Classification Quick Facts
```
Energy signal: 0 < E < infinity, P = 0
Power signal: 0 < P < infinity, E = infinity
Periodic: x(t) = x(t+T) for all t
Even: x(t) = x(-t)
Odd: x(t) = -x(-t)
```

## Convolution Shortcuts
```
Convolution identity: x(t) * delta(t) = x(t)
Time shift: x(t-t1) * delta(t-t2) = x(t-t1-t2)
Width of convolution = sum of widths of individual signals
Commutative: x*h = h*x
Associative: (x*h1)*h2 = x*(h1*h2)
```

## Fourier Transform Quick Reference
```
x(t) <-> X(jw)
x(at) <-- (1/|a|) X(jw/a)         [scaling]
x(t-t0) <-- e^(-jwt0) X(jw)      [time shift]
dx/dt <-- jw X(jw)                [differentiation]
e^(jw0t) x(t) <-- X(j(w-w0))     [frequency shift]
x(t)*y(t) <-- X(jw).Y(jw)        [convolution = multiplication]
x(t).y(t) <-- (1/2pi) X(jw)*Y(jw) [multiplication = convolution]
```

## Fourier Series Quick Properties
```
DC component: a0 = (1/T) integral of x(t) over one period
Exponential: cn = (1/T) integral of x(t)*e^(-jnw0t)
Parseval's: (1/T)integral |x(t)|^2 = Sum |cn|^2
Half-wave symmetry: only odd harmonics present
Quarter-wave symmetry: only odd sine or cosine terms
```

## Laplace Transform Quick Reference
```
ROC determines uniqueness of inverse LT
Left-sided signal: ROC is left half plane
Right-sided signal: ROC is right half plane
Stable system: ROC includes jw axis
Causal system: ROC is right of rightmost pole

Initial value: x(0+) = lim(s->inf) s*X(s) (if X(s) proper)
Final value: x(inf) = lim(s->0) s*X(s) (if poles in LHP)
```

## Z-Transform Quick Reference
```
ROC inside unit circle: stable system
ROC outside unit circle: causal system
Stable + causal: ROC includes unit circle

x(n) <-> X(z)
x(n-n0) <-- z^(-n0) X(z)         [time shift]
a^n x(n) <-- X(z/a)              [scaling]
x(n)*y(n) <-- X(z).Y(z)          [convolution]
```

## FFT Quick Facts
```
DFT of N points: N^2 complex multiplications
Radix-2 DIT FFT: (N/2)*log2(N) complex multiplications
Stages = log2(N)
Example: N=1024, stages = 10, savings = 1024^2 vs 5120
Bit-reversal reordering at input (DIT) or output (DIF)
Butterfly: basic computation unit
```

## System Properties Quick Check
```
LTI: Linear + Time-Invariant (impulse response determines everything)
BIBO stable: impulse response absolutely summable (discrete) or integrable (continuous)
Causal: h(t) = 0 for t < 0 (continuous), h(n) = 0 for n < 0 (discrete)
Memoryless: h(t) = K*delta(t) (output depends only on current input)
```
