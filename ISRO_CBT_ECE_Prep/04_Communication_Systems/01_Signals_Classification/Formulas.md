# Signals Classification — Formulas

## 1. Energy of a Continuous-Time Signal

### Energy
```
E = ∫_{-∞}^{∞} |x(t)|² dt
```
- For real signals: `E = ∫_{-∞}^{∞} x²(t) dt`
- Finite energy → Energy signal

### Parseval's Theorem
```
E = ∫_{-∞}^{∞} |x(t)|² dt = ∫_{-∞}^{∞} |X(f)|² df
```
- Energy in time domain = Energy in frequency domain

---

## 2. Power of a Continuous-Time Signal

### Average Power
```
P = lim_{T→∞} (1/2T) ∫_{-T}^{T} |x(t)|² dt
```

### For Periodic Signals (Period T₀)
```
P = (1/T₀) ∫_{T₀} |x(t)|² dt
```
- Average over ONE period is sufficient for periodic signals

### Power of Sinusoid A·cos(ωt + φ)
```
P = A²/2
```

### Power of Square Wave (amplitude A, 50% duty cycle)
```
P = A²
```

---

## 3. Even and Odd Decomposition

### Even Part
```
x_e(t) = [x(t) + x(-t)] / 2
```

### Odd Part
```
x_o(t) = [x(t) - x(-t)] / 2
```

### Verification
```
x(t) = x_e(t) + x_o(t)
x_e(t) · x_o(t) = 0  (orthogonal property over symmetric interval)
```

### Energy of Decomposed Parts
```
E_total = E_even + E_odd
```
(Cross-term integrates to zero because integrand is odd)

---

## 4. Common Signal Energy/Power Values

### Rectangular Pulse of amplitude A, width τ
```
E = A²τ
P = 0  (energy signal, not power signal)
```

### Exponential Pulse e^(-at)·u(t), a > 0
```
E = ∫₀^∞ e^(-2at) dt = 1/(2a)
P = 0
```

### Periodic Sinusoid A·cos(ω₀t)
```
E = ∞
P = A²/2
```

### Impulse δ(t)
```
E = ∫ δ²(t) dt → ∞  (undefined, but handled via distribution theory)
Power = ∞
```

---

## 5. Periodicity Conditions

### For Sum of Two Periodic Signals
```
If x₁(t) has period T₁ and x₂(t) has period T₂
x(t) = x₁(t) + x₂(t) is periodic IF T₁/T₂ is rational
T₀ = LCM(T₁, T₂)  [as fractions]
```

### For Discrete-Time Periodic Signal
```
x[n] = x[n + N]
N must be INTEGER
If N₁/N₂ is rational → periodic with N = LCM(N₁, N₂)
```

### Example
```
x(t) = cos(2π·3t) + sin(2π·5t)
T₁ = 1/3, T₂ = 1/5
T₁/T₂ = 5/3 (rational) → Periodic
T₀ = LCM(1/3, 1/5) = LCM(1,1)/GCD(3,5) = 1/1 = 1 sec
```

---

## 6. Baseband-Bandpass Conversion

### Bandpass Signal from Baseband
```
s(t) = Re{g(t) · e^(j2πf_c·t)}
```
- g(t) = complex envelope (baseband signal)
- f_c = carrier frequency

### For Real Baseband Signal g(t) = A(t)cos(θ(t))
```
s(t) = A(t) · cos(2πf_c·t + θ(t))
```

### Complex Envelope from Bandpass
```
g(t) = s_I(t) + j·s_Q(t)
```
- s_I(t) = in-phase component
- s_Q(t) = quadrature component

---

## 7. Cross-Correlation and Autocorrelation

### Autocorrelation (Energy Signal)
```
R_xx(τ) = ∫_{-∞}^{∞} x(t) · x*(t-τ) dt
```

### Autocorrelation (Power Signal)
```
R_xx(τ) = lim_{T→∞} (1/2T) ∫_{-T}^{T} x(t) · x*(t-τ) dt
```

### Properties
```
R_xx(0) = E (for energy signal) or P (for power signal)
R_xx(τ) = R_xx(-τ)*  (conjugate symmetric)
|R_xx(τ)| ≤ R_xx(0)  (maximum at origin)
```

### Wiener-Khintchine Theorem
```
S_xx(f) = F{R_xx(τ)}
```
Power Spectral Density is Fourier Transform of autocorrelation

---

## 8. Important Transform Pairs (Quick Reference)

| Signal x(t) | Transform X(f) |
|-------------|----------------|
| δ(t) | 1 |
| 1 | δ(f) |
| e^(j2πf₀t) | δ(f - f₀) |
| cos(2πf₀t) | [δ(f-f₀) + δ(f+f₀)]/2 |
| u(t) | ½δ(f) + 1/(j2πf) |
| e^(-at)u(t), a>0 | 1/(a + j2πf) |
| Π(t/τ) | τ·Sa(πfτ) |
| e^(-a|t|) | 2a/(a² + 4π²f²) |

---

## 9. ISRO-Quick Formulas
```
Energy of rectangular pulse = A²τ
Power of sinusoid = A²/2
Even part = [x(t)+x(-t)]/2
Odd part = [x(t)-x(-t)]/2
Periodic sum condition: T₁/T₂ = rational
Bandpass: s(t) = Re{g(t)e^(j2πfct)}
```
