# Fourier Transform - Formulas

## Core Pairs
```
delta(t)        <->   1
1               <->   2pi delta(w)
u(t)            <->   pi delta(w) + 1/(jw)
e^(-at)u(t)     <->   1/(a+jw)
e^(-a|t|)       <->   2a/(a^2+w^2)
t^n u(t)        <->   n!/(jw)^(n+1)
cos(w0 t)       <->   pi[delta(w-w0)+delta(w+w0)]
sign(t)         <->   2/(jw)
rect(t/tau)     <->   tau*sinc(w*tau/2)
sinc(Wt/pi)     <->   rect(w/2W)  [duality]
```

## Properties in Wrapper Form
```
x(t-t0)     <-> X(w) e^(-jwt0)
x(-t)       <-> X(-w)
x(at)       <-> (1/|a|)X(w/a)
x(t)e^(jw0t) <-> X(w-w0)
x(t)*h(t)   <-> X(w)H(w)
x(t)h(t)    <-> (1/2pi)X(w)*H(w)   [freq convolution]
dx/dt       <-> jw X(w)
integral x  <-> X(w)/(jw) + pi X(0) delta(w)
x*(t)       <-> X*(-w)
x(t) real   <-> X(-w)=X*(w)  [conjugate symmetry]
```

## Duality
```
If x(t) <-> X(w), then X(t) <-> 2pi x(-w)
```

## Parseval / Energy
```
E = integral |x(t)|^2 dt = (1/2pi) integral |X(w)|^2 dw
|X(w)|^2 = ESD (energy spectral density)
Rxx(tau) <-> |X(w)|^2  (autocorrelation)
```

## Frequency Response
```
For LTI: Y(w) = X(w) H(w)
|H(w)| = magnitude response (gain)
angle H(w) = phase response
Stability: all poles in LHP
```

## Bandwidth Definitions
```
3 dB bandwidth: where |H(w)|^2 = 0.5 max (or -3dB)
Null-to-null (main lobe of sinc): delta = 2/tau
Rectangular bandwidth: integrates to same energy (equivalent)
RMS bandwidth
```

## Quick-Reference Pairs to MEMORIZE
```
pair             transform
delta           1
1               2pi delta
u(t)            pi delta + 1/(jw)
e^-at u(t)      1/(a+jw)
cos(w0t)        pi[delta(w-w0)+delta(w+w0)]
rect(t/tau)     tau sinc(w tau/2)
synth           ...
```

## Energy vs Power Signals
```
Energy signal: finite E, not periodic
Power signal: finite P_avg (periodic/stationary)
delta, rect: energy signals
sinusoid, step: power signals (step has finite energy? No, u(t) has infinite energy)
```
