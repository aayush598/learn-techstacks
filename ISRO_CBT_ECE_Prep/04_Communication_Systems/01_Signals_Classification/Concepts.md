# Signals Classification — Concepts

## 1. Basic Definition
- A **signal** is a function of time (or space) carrying information
- **System** processes signals to produce output signals
- Classification helps in choosing appropriate analysis tools

---

## 2. Periodic vs Aperiodic Signals

### Periodic Signal
- Repeats exactly after fixed interval T (period): `x(t) = x(t + T)` for all t
- **Fundamental period T₀**: smallest positive T satisfying the periodicity condition
- Examples: Sinusoids, square wave, sawtooth, impulse train
- **Energy is infinite** over (-∞, +∞); analyzed via Fourier Series

### Aperiodic Signal
- Does not repeat; no such T exists
- Examples: Exponential pulse, single rectangular pulse, Gaussian pulse
- **Finite energy** possible; analyzed via Fourier Transform

### Key Test
If `x(t) = x(t + T₁) = x(t + T₂)`, then x(t) is also periodic with period `T₀ = GCD(T₁, T₂)`

---

## 3. Energy Signal vs Power Signal

### Energy Signal
- **Finite, non-zero total energy**: 0 < E < ∞
- **Average power = 0**
- All finite-duration signals are energy signals
- Examples: Single pulse, truncated sinusoid, exponential decay

### Power Signal
- **Finite, non-zero average power**: 0 < P < ∞
- **Total energy = ∞**
- All periodic signals (with finite amplitude) are power signals
- Examples: Sinusoids, periodic square wave, DC signal

### Neither
- Signals with both E = ∞ and P = ∞ (e.g., ramp function, growing exponential)
- These are **neither energy nor power signals**

---

## 4. Even and Odd Signals

### Even Signal (Symmetric)
- `x(t) = x(-t)` — mirror symmetry about vertical axis
- Graphical test: Fold about y-axis, signal overlaps exactly
- Examples: cos(t), |t|, t², rectangular pulse centered at origin

### Odd Signal (Anti-symmetric)
- `x(t) = -x(-t)` — anti-symmetry about origin
- Graphical test: Fold about y-axis then invert; signal overlaps
- Examples: sin(t), t³, signum function sgn(t)

### Any Signal Decomposition
Every signal can be written as sum of even and odd parts:
- **Even part**: xₑ(t) = [x(t) + x(-t)] / 2
- **Odd part**: xₒ(t) = [x(t) - x(-t)] / 2
- **Verification**: x(t) = xₑ(t) + xₒ(t)

### Properties
- Product of two even signals → even
- Product of two odd signals → even
- Product of even × odd → odd
- Integral of odd signal over symmetric interval = 0

---

## 5. Baseband vs Bandpass Signals

### Baseband (Lowpass) Signal
- Energy concentrated near **zero frequency** (DC to some W Hz)
- Bandwidth occupies frequencies from 0 to W
- Examples: Audio (20 Hz–20 kHz), video, digital data streams
- Directly suitable for **short-distance wired transmission**
- Can be transmitted over cables without modulation

### Bandpass (Passband) Signal
- Energy concentrated around some **carrier frequency f_c** ± W/2
- Bandwidth occupies [f_c - W/2, f_c + W/2]
- Obtained by **modulating** a baseband signal onto a carrier
- Required for **wireless/radio transmission** (antenna size ∝ λ/10)
- Examples: AM/FM radio, mobile phone signals, satellite signals

### Relationship
- Bandpass signal: `s(t) = Re{g(t) · e^(j2πf_c·t)}`
- g(t) = complex envelope (baseband equivalent)
- All bandpass signal analysis reduces to baseband equivalent analysis

---

## 6. Additional Classifications

### Continuous-Time vs Discrete-Time
- **CT**: defined for all real values of t (analog signals)
- **DT**: defined only at integer instants n (sequences x[n])

### Analog vs Digital
- **Analog**: continuous in amplitude AND time
- **Digital**: discrete in both time AND amplitude (quantized)

### Deterministic vs Random
- **Deterministic**: completely specified by mathematical expression
- **Random/Probabilistic**: described only by statistical properties (PDF, PSD)

### Causal vs Non-Causal
- **Causal**: x(t) = 0 for t < 0 (no future dependency)
- **Anti-causal**: x(t) = 0 for t > 0
- **Non-causal**: exists for both t < 0 and t > 0

---

## 7. Important Special Signals

| Signal | Definition | Property |
|--------|-----------|----------|
| Unit step u(t) | 1 for t≥0, 0 otherwise | Even + Odd = 1 |
| Impulse δ(t) | Area 1 at t=0, 0 elsewhere | Even signal |
| Signum sgn(t) | 1 for t>0, -1 for t<0 | Odd signal |
| Rect pulse Π(t/T) | 1 for |t|<T/2 | Even signal |
| Triangular Λ(t/T) | 1-|t/T| for |t|<T | Even signal |
| Sa(x) = sin(x)/x | Sampling function | Even signal |

---

## 8. ISRO-Focused Points
- Energy/power signal distinction is frequently tested
- Even/odd decomposition is a common numerical problem
- Bandpass representation is key to understanding modulation
- Causal signals are critical for realizable systems
- Understanding signal types determines whether to use Fourier Series or Transform
