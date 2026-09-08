# Signals & Systems / DSP - Complete Formula Sheet

## Fourier Transform Pairs
```
delta(t)           <-> 1
1                  <-> 2*pi*delta(w)
e^(jw0t)           <-> 2*pi*delta(w-w0)
cos(w0t)           <-> pi*[delta(w-w0)+delta(w+w0)]
sin(w0t)           <-> j*pi*[delta(w+w0)-delta(w-w0)]
e^(-at)*u(t)       <-> 1/(a+jw), a>0
rect(t/T)          <-> T*sinc(wT/2)
e^(-a|t|)          <-> 2a/(a^2+w^2)
```

## Fourier Transform Properties
```
Linearity:       ax(t)+by(t)          <-> aX(jw)+bY(jw)
Time shift:      x(t-t0)              <-> e^(-jwt0)*X(jw)
Freq shift:      e^(jw0t)*x(t)        <-> X(j(w-w0))
Scaling:         x(at)                <-> (1/|a|)*X(jw/a)
Differentiation: dx/dt                <-> jw*X(jw)
Integration:     integral x(tau)dtau  <-> X(jw)/(jw) + pi*X(0)*delta(w)
Convolution:     x(t)*y(t)            <-> X(jw)*Y(jw)
Multiplication:  x(t)*y(t)            <-> (1/2pi)*X(jw)*Y(jw)
Time reversal:   x(-t)                <-> X(-jw) = X*(jw) for real x
Parseval:        integral |x(t)|^2 dt <-> (1/2pi)*integral |X(jw)|^2 dw
```

## Laplace Transform
```
Key pairs:
  e^(-at)*u(t)  <-> 1/(s+a)
  t*e^(-at)*u(t) <-> 1/(s+a)^2
  sin(wt)*u(t)  <-> w/(s^2+w^2)
  cos(wt)*u(t)  <-> s/(s^2+w^2)

Initial value theorem: x(0+) = lim(s->inf) s*X(s)
Final value theorem: x(inf) = lim(s->0) s*X(s) (poles in LHP only)
```

## Z-Transform
```
Key pairs:
  delta[n]      <-> 1
  u[n]          <-> z/(z-1)
  a^n*u[n]      <-> z/(z-a)
  n*a^n*u[n]    <-> az/(z-a)^2

Properties:
  x[n-n0]       <-> z^(-n0)*X(z)
  a^n*x[n]      <-> X(z/a)
  x[n]*y[n]     <-> X(z)*Y(z)

Stability: all poles inside unit circle (|z|<1)
ROC includes unit circle for stable system
```

## Convolution
```
Continuous: y(t) = integral x(tau)*h(t-dtau) from -inf to inf
Discrete:   y[n] = sum x[k]*h[n-k] from -inf to inf

Width: output width = input width + impulse response width
Identity: x*delta = x
Commutative: x*h = h*x
Associative: (x*h1)*h2 = x*(h1*h2)
```

## DFT/FFT
```
DFT: X[k] = sum x[n]*e^(-j*2*pi*k*n/N) for n=0 to N-1
IDFT: x[n] = (1/N)*sum X[k]*e^(j*2*pi*k*n/N) for k=0 to N-1

FFT (Radix-2):
  Complexity: (N/2)*log2(N) butterflies
  Stages: log2(N)
  Input: bit-reversed order (DIT)
  Output: natural order (DIT)
```

## System Properties
```
LTI: determined by impulse response h(t)
Stable: integral |h(t)|dt < infinity (continuous)
         sum |h[n]| < infinity (discrete)
Causal: h(t)=0 for t<0, h[n]=0 for n<0
```

## Sampling
```
Nyquist: fs >= 2*fmax
Aliasing: fs < 2*fmax
Reconstruction: LPF with cutoff fmax
ZOH transfer function: (1-e^(-sT))/s
```
