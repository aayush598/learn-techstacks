# Signal Classification - Key Formulas

## 1. Classification by Time

### Continuous-Time vs Discrete-Time
- **CT signal**: x(t), t ∈ ℝ
- **DT signal**: x[n], n ∈ ℤ
- **Sampling**: x[n] = x(nT_s), where T_s = 1/f_s

### Analog vs Digital
- **Analog**: Continuous in time AND amplitude
- **Digital**: Discrete in time AND quantized amplitude

---

## 2. Classification by Periodicity

### Continuous-Time Periodic Signal
```
x(t) = x(t + T₀),  ∀t
```
- Fundamental period: T₀
- Fundamental frequency: f₀ = 1/T₀
- Angular frequency: ω₀ = 2πf₀ = 2π/T₀

### Discrete-Time Periodic Signal
```
x[n] = x[n + N],  ∀n
```
- N must be an INTEGER
- Fundamental frequency: Ω₀ = 2π/N

### Test for DT Periodicity
1. Compute ω₀/2π = k/N (must be rational)
2. N = (2π/ω₀) × k, where k is smallest integer making N integer

---

## 3. Energy and Power Formulas

### Energy of CT Signal
```
E = ∫_{-∞}^{∞} |x(t)|² dt
```

### Power of CT Periodic Signal
```
P = (1/T₀) ∫_{T₀} |x(t)|² dt
```

### Energy of DT Signal
```
E = Σ_{n=-∞}^{∞} |x[n]|²
```

### Power of DT Periodic Signal
```
P = (1/N) Σ_{n=<N>} |x[n]|²
```

---

## 4. Signal Classification Criteria

| Type | Energy (E) | Power (P) |
|------|-----------|-----------|
| Energy Signal | 0 < E < ∞ | P = 0 |
| Power Signal | E = ∞ | 0 < P < ∞ |
| Neither | E = ∞ | P = ∞ |

---

## 5. Elementary CT Signals

### Unit Step
```
u(t) = { 1, t ≥ 0
        { 0, t < 0
```

### Unit Impulse
```
δ(t) = { ∞, t = 0
        { 0, t ≠ 0
∫_{-∞}^{∞} δ(t) dt = 1
```

### Unit Ramp
```
r(t) = t · u(t)
```

### Sign Function
```
sgn(t) = { 1,  t > 0
          { 0,  t = 0
          {-1,  t < 0
```

### Exponential
```
x(t) = e^(αt),  α = σ + jω
```

---

## 6. Elementary DT Signals

### Unit Impulse (Unit Sample)
```
δ[n] = { 1, n = 0
        { 0, n ≠ 0
```

### Unit Step
```
u[n] = { 1, n ≥ 0
        { 0, n < 0
```

### Relationship
```
δ[n] = u[n] - u[n-1]
u[n] = Σ_{k=-∞}^{n} δ[k]
```

---

## 7. Common Signal Decompositions

### Even and Odd Parts
```
x_e(t) = [x(t) + x(-t)] / 2    (Even part)
x_o(t) = [x(t) - x(-t)] / 2    (Odd part)
x(t) = x_e(t) + x_o(t)
```

### For DT Signals
```
x_e[n] = [x[n] + x[-n]] / 2
x_o[n] = [x[n] - x[-n]] / 2
```

---

## 8. Real Exponential Signal Properties

### CT Exponential: x(t) = Ce^(αt)
| α | Behavior |
|---|----------|
| α real, α > 0 | Exponentially growing |
| α real, α < 0 | Exponentially decaying |
| α = jω₀ | Purely oscillatory |
| α = σ + jω₀ | Growing/decaying sinusoid |

### DT Exponential: x[n] = Cz^n, z = re^(jΩ₀)
| r | Ω₀ | Behavior |
|---|-----|----------|
| r > 1 | 0 | Growing |
| 0 < r < 1 | 0 | Decaying |
| r = 1 | 0 | Constant |
| 1 | any | Oscillatory |

---

## 9. Sinusoidal Signal Properties

### CT Sinusoid
```
x(t) = A cos(ωt + φ)
```
- Always periodic with T₀ = 2π/ω
- ω in rad/s, f in Hz

### DT Sinusoid
```
x[n] = A cos(Ωn + φ)
```
- Periodic ONLY if Ω/2π is rational
- Period: N = (2π/Ω) × k (smallest k ∈ ℤ)

---

## 10. Special Signal Properties

### Delta Function Sifting Property
```
∫_{-∞}^{∞} x(t)δ(t-t₀) dt = x(t₀)
Σ_{n=-∞}^{∞} x[n]δ[n-n₀] = x[n₀]
```

### Delta Function Scaling
```
δ(at) = (1/|a|) δ(t)
```

### Multiplication Property
```
x(t)δ(t-t₀) = x(t₀)δ(t-t₀)
```

---

## 11. Unit Step Integral/Derivative Relations

### CT Relationships
```
∫_{-∞}^{t} δ(τ) dτ = u(t)
du(t)/dt = δ(t)
```

### DT Relationships
```
Σ_{k=-∞}^{n} δ[k] = u[n]
Δu[n] = u[n] - u[n-1] = δ[n]
```

---

## 12. Random vs Deterministic

- **Deterministic**: x(t) completely known for all t
- **Random**: x(t) described by statistical properties
- **Stationary**: Statistical properties time-invariant
- **Ergodic**: Time averages = Ensemble averages

---

## 13. Continuous vs Discrete Amplitude

| Type | Time | Amplitude | Example |
|------|------|-----------|---------|
| CT Analog | CT | CT | Temperature sensor |
| CT Digital | CT | Quantized | ADC output |
| DT Analog | DT | CT | Sampled signal |
| DT Digital | DT | Quantized | Computer data |

---

## 14. Signal Operations Formulas

### Time Shifting
```
x(t - t₀): Delayed by t₀ (right shift)
x(t + t₀): Advanced by t₀ (left shift)
```

### Time Scaling
```
x(at): Compressed by factor |a| > 1
x(at): Expanded by factor |a| < 1
```

### Time Reversal
```
x(-t): Reflected about t = 0
```

---

## 15. Even/Odd Signal Properties

### Even × Even = Even
### Odd × Odd = Even
### Even × Odd = Odd

### Even signal: x(t) = x(-t)
### Odd signal: x(t) = -x(-t)

### If x(t) is real and even → X(ω) is real and even
### If x(t) is real and odd → X(ω) is imaginary and odd
