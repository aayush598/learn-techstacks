# LTI Systems and Convolution - Concepts

## LTI System Properties
- **Linear:** Superposition holds (additivity + homogeneity)
- **Time-Invariant:** Response doesn't change with time shift
- **LTI:** Impulse response completely describes the system
- Output: y(t) = x(t) * h(t) (convolution)

## Causality
- Output depends only on present and past inputs
- h(t) = 0 for t < 0
- For a rational system: ROC is to the right of rightmost pole

## Stability (BIBO)
- Bounded input produces bounded output
- Continuous: integral |h(t)| dt < infinity
- Discrete: sum |h[n]| < infinity
- Poles must be in LHP (continuous) or inside unit circle (discrete)

## Memory
- Memoryless: y(t) depends only on current input
- With memory: output depends on past inputs
- Memoryless LTI: h(t) = K*delta(t)

## Invertibility
- System is invertible if input can be recovered from output
- Inverse system: h(t) * h_inv(t) = delta(t)
- Example: Differentiator and integrator are inverses

---

## Convolution

### Continuous-Time
```
y(t) = integral from -inf to inf of x(tau)*h(t-tau) dtau
Commutative: x*h = h*x
```

### Discrete-Time
```
y[n] = sum from k=-inf to inf of x[k]*h[n-k]
```

## Convolution Properties
```
Identity: x(t)*delta(t) = x(t)
Time shift: x(t-t1)*delta(t-t2) = x(t-t1-t2)
Commutative: x*h = h*x
Associative: (x*h1)*h2 = x*(h1*h2)
Distributive: x*(h1+h2) = x*h1 + x*h2
Differentiation: d/dt(x*h) = dx/dt*h = x*dh/dt
Width: output width = sum of input widths
```

## Graphical Convolution Method
1. Reverse h(tau) -> h(-tau)
2. Shift by t: h(t-tau)
3. Multiply x(tau)*h(t-tau)
4. Integrate over tau where overlap exists
5. Repeat for all t values

---

## ISRO Key Points
- x(t)*delta(t) = x(t) (most tested property)
- Time shift convolution shortcut
- LTI system is fully characterized by impulse response
- Causality and stability can be checked from h(t)
- Causal + stable: both conditions on h(t)
