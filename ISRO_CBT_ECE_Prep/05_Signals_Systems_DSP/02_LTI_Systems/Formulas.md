# LTI Systems and Convolution - Formulas

## Convolution
```
Continuous: y(t) = x(t)*h(t) = integral x(tau)*h(t-tau) dtau
Discrete:   y[n] = x[n]*h[n] = sum x[k]*h[n-k]
```

## Convolution Properties
```
Identity:     x*delta = x
Time shift:   x(t-t0)*delta(t-t1) = x(t-t0-t1)
Commutative:  x*h = h*x
Associative:  (x*h1)*h2 = x*(h1*h2)
Distributive: x*(h1+h2) = x*h1 + x*h2
Differentiation: d/dt(x*h) = (dx/dt)*h = x*(dh/dt)
Integration:   integral(x*h)dt = integral(x)dt * h = x * integral(h)dt
```

## Common Convolution Results
```
u(t) * u(t) = t*u(t) = ramp
u(t) * e^(-at)*u(t) = (1/a)(1-e^(-at))*u(t)
e^(-at)*u(t) * e^(-bt)*u(t) = (e^(-at)-e^(-bt))/(b-a) * u(t) [for a != b]
delta(t-t0) * x(t) = x(t-t0)
```

## LTI System Properties from h(t)
```
Causal:    h(t) = 0 for t < 0 (continuous)
           h[n] = 0 for n < 0 (discrete)
Stable:    integral |h(t)| dt < infinity (continuous)
           sum |h[n]| < infinity (discrete)
Memoryless: h(t) = K*delta(t)
```

## System from Differential Equation
```
ay'' + by' + cy = x(t)
Characteristic equation: ar^2 + br + c = 0
Transfer function: H(s) = 1/(as^2 + bs + c)
```

## Quick Reference
| Operation | Result |
|-----------|--------|
| x * delta | x |
| u * u | ramp (t*u(t)) |
| x(t-t1) * delta(t-t2) | x(t-t1-t2) |
| x * (h1+h2) | x*h1 + x*h2 |
| (x*h1)*h2 | x*(h1*h2) |
