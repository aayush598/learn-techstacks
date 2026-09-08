# Fourier Transform - Concepts

## Definition
```
X(w) = integral[-inf to inf] x(t) e^(-j w t) dt
x(t) = (1/2pi) integral[-inf to inf] X(w) e^(j w t) dw
```
- Non-periodic signals represented as continuous spectrum
- X(w) is complex (magnitude + phase)

## Key Properties Table
| Property | Signal | Transform |
|----------|--------|-----------|
| Linearity | ax + by | aX + bY |
| Time shift | x(t-t0) | X(w) e^(-j w t0) |
| Time scaling | x(at) | (1/|a|)X(w/a) |
| Frequency shift | x(t) e^(j w0 t) | X(w - w0) |
| Conjugation | x*(t) | X*(-w) |
| Time reversal | x(-t) | X(-w) |
| Time convolution | x*h | X*H |
| Frequency convolution | x*y | (1/2pi)(X*Y) |
| Differentiation | dx/dt | jw X(w) |
| Integration | integral x dt | X(w)/(jw) + pi X(0) delta(w) |
| Parseval | |x(t)|^2 dt | (1/2pi)|X(w)|^2 dw |
| Duality | X(t) | 2pi x(-w) |
| Multiplication | x(t) y(t) | (1/2pi) X(w)*Y(w) |

## Important Fourier Transform Pairs
```
delta(t)            <->   1
1                    <->   2*pi*delta(w)
u(t)                <->   pi*delta(w) + 1/(jw)
e^(-at) u(t)        <->   1/(a + jw)
e^(-a|t|)           <->   2a/(a^2 + w^2)
cos(w0 t)           <->   pi[delta(w-w0) + delta(w+w0)]
sin(w0 t)           <->   j pi[delta(w+w0) - delta(w-w0)]
rect(t/tau)         <->   tau*sinc(w*tau/2)
sinc(w0 t/pi)       <->   rect... (duality)
sign(t)             <->   2/(jw)
e^(-t^2/2) (Gaussian)<->  sqrt(2pi)e^(-w^2/2)
```

## sinc Function
```
sinc(x) = sin(pi x)/(pi x)
sinc(0) = 1, zeros at integer x
Bandwidth of sinc: -1/tau to 1/tau (main lobe)
```

## Sampling/Window Relationships
```
rect(t/T) -> T*sinc(wT/2): narrow time => wide freq, and vice versa
delta(t) -> 1 (impulse has flat spectrum)
```
KEY: Time-bandwidth product. Short time signals need large bandwidth.

## Parseval/Energy
```
Energy = integral |x(t)|^2 dt = (1/2pi) integral |X(w)|^2 dw
|X(w)|^2 = energy spectral density (ESD)
Autocorrelation <-> ESD (Wiener-Khinchin)
```

## Convolution Theorem (crucial)
```
x(t)*h(t) <-> X(w) H(w)
Convolution in time = multiplication in frequency
This is the basis of linear filtering and LTI analysis
```

## ISRO Key Points
- Convolution property most tested
- delta <-> 1, u(t) <-> pi delta + 1/(jw)
- duality property is heavily used
- Parseval/energy relation
- Sinc function appears with rect, filtering
