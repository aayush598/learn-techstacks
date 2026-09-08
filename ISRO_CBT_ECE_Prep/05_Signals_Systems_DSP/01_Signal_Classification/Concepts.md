# Signal Classification - Concepts

## 1. Continuous-Time vs Discrete-Time Signals

### Continuous-Time Signals x(t)
- Defined for every real value of time t
- Independent variable t is continuous
- Examples: speech signal, temperature variations, voltage across capacitor
- Represented as x(t) where t ∈ ℝ

### Discrete-Time Signals x[n]
- Defined only at integer values of n
- Independent variable n is integer-valued
- Obtained by sampling continuous-time signals: x[n] = x(nTₛ)
- Examples: digital data, sampled signals, sequences
- Represented as x[n] where n ∈ ℤ

### Hybrid: Continuous-Valued Discrete-Time
- Discrete in time but continuous in amplitude
- This is what we get after sampling but before quantization

## 2. Periodic vs Aperiodic Signals

### Continuous-Time Periodic Signal
- x(t) = x(t + T₀) for all t
- T₀ is the fundamental period (smallest positive T₀ satisfying the condition)
- Fundamental frequency: f₀ = 1/T₀, angular frequency: ω₀ = 2π/T₀

### Discrete-Time Periodic Signal
- x[n] = x[n + N] for all integer n
- N must be a positive integer
- Fundamental period: smallest positive integer N satisfying the condition
- Fundamental frequency: Ω₀ = 2π/N

### Key Difference
- A continuous-time sinusoid cos(ω₀t) is ALWAYS periodic for any ω₀ ≠ 0
- A discrete-time sinusoid cos(Ω₀n) is periodic ONLY if Ω₀/2π is a rational number
- Example: cos(3n) is NOT periodic because 3/2π is irrational

## 3. Energy and Power Signals

### Energy Signal
- Finite total energy: 0 < E < ∞
- Energy: E = ∫|x(t)|² dt (CT) or E = Σ|x[n]|² (DT)
- Average power P = 0
- Examples: pulse signal, decaying exponential e⁻ᵃᵗ u(t)

### Power Signal
- Finite nonzero average power: 0 < P < ∞
- Power: P = lim(T→∞) (1/2T) ∫₋ₜᵀ |x(t)|² dt
- Total energy E = ∞
- Examples: sinusoids, periodic signals

### Neither Energy nor Power
- Signals with both infinite energy and infinite power
- Example: x(t) = eᵗ (growing exponential)

### Relationship
- Every energy signal is bounded and has finite duration or decays to zero
- Every periodic signal (non-zero) is a power signal
- A signal cannot be both energy and power signal

## 4. Even and Odd Signals

### Even Signals (Symmetric)
- x(t) = x(-t) for all t
- Symmetric about vertical axis (y-axis)
- Examples: cos(t), |t|, t²
- Any signal can be decomposed: xₑ(t) = [x(t) + x(-t)]/2

### Odd Signals (Antisymmetric)
- x(-t) = -x(t) for all t
- Antisymmetric about origin
- Examples: sin(t), t, t³
- Decomposition: xₒ(t) = [x(t) - x(-t)]/2

### Properties
- x(t) = xₑ(t) + xₒ(t) (any signal = even + odd parts)
- Product of two even signals = even
- Product of two odd signals = even
- Product of even and odd = odd
- Integral of even signal over symmetric interval = 2 × integral over half
- Integral of odd signal over symmetric interval = 0

## 5. Deterministic vs Random Signals

### Deterministic Signals
- Completely known for all time
- No uncertainty in value at any instant
- Can be described by a mathematical expression
- Examples: sinusoids, pulses, exponentials

### Random Signals (Stochastic)
- Values known only in terms of probability
- Cannot be described exactly in advance
- Characterized by statistical properties (mean, variance, autocorrelation)
- Examples: noise, speech, thermal noise

## 6. Singularity Functions

### Unit Impulse Function δ(t)
- δ(t) = 0 for t ≠ 0
- ∫δ(t) dt = 1 (over any interval containing t = 0)
- Sifting property: ∫x(t)δ(t-t₀) dt = x(t₀)
- Scaling: δ(at) = (1/|a|)δ(t)
- Not a true function but a distribution/generalized function
- Limit representation: δ(t) = lim(ε→0) [1/ε] rect(t/ε)

### Unit Step Function u(t)
- u(t) = 1 for t > 0, u(t) = 0 for t < 0
- u(0) is typically defined as 0.5 (or left undefined)
- Relationship: u(t) = ∫₋∞ᵗ δ(τ) dτ
- δ(t) = du(t)/dt (in distributional sense)

### Unit Ramp Function r(t)
- r(t) = t · u(t) = t for t > 0, 0 for t < 0
- r(t) = ∫₋∞ᵗ u(τ) dτ
- du(t)/dt = δ(t), dr(t)/dt = u(t)

### Signum Function sgn(t)
- sgn(t) = 1 for t > 0, -1 for t < 0
- Relationship: sgn(t) = 2u(t) - 1
- d/dt sgn(t) = 2δ(t)

### Sinc Function
- sinc(t) = sin(πt)/(πt)
- sinc(0) = 1
- Zero crossings at t = ±1, ±2, ±3, ...
- Important in sampling and Fourier analysis

### Rectangular Pulse rect(t)
- rect(t) = 1 for |t| < 0.5, 0 for |t| > 0.5
- Width = 1, centered at origin
- Fourier transform is sinc function

## 7. Signal Operations

### Time Shifting
- x(t - t₀): delayed signal (shift right if t₀ > 0)
- x(t + t₀): advanced signal (shift left if t₀ > 0)
- Only the t variable is affected: replace t with (t - t₀)

### Time Scaling
- x(at): compressed if |a| > 1, expanded if |a| < 1
- x(t/a): expanded if |a| > 1, compressed if |a| < 1
- Amplitude remains unchanged
- Scaling affects duration and frequency content

### Time Reversal
- x(-t): reflection about vertical axis
- Special case of time scaling with a = -1
- Flips the signal in time

### Amplitude Scaling
- A · x(t): scales amplitude by factor A
- Does not affect time axis
- x(t) + B: shifts signal vertically by B

### Combined Operations
- x(at + b): combination of shift and scaling
- Order matters: first shift, then scale OR first scale then shift with adjusted parameter
- Method 1: x(t) → x(t + b) → x(at + b) [shift then scale]
- Method 2: x(t) → x(at) → x(a(t + b/a)) [scale then shift]

## 8. Classification Summary Table

| Property | Continuous | Discrete |
|----------|-----------|----------|
| Variable | t ∈ ℝ | n ∈ ℤ |
| Periodicity | Any ω₀ ≠ 0 | Only if Ω₀/2π ∈ ℚ |
| Energy | ∫|x(t)|² dt | Σ|x[n]|² |
| Power | lim(1/2T)∫|x(t)|² dt | lim(1/2N+1)Σ|x[n]|² |
| Impulse | δ(t) | δ[n] (Kronecker) |

## 9. ISRO Key Points
- Discrete sinusoid periodicity test: check if frequency/2π is rational
- Energy signals have finite energy, zero power; power signals have finite power, infinite energy
- Singularity functions: δ(t) is the identity element in convolution
- Even part: [x(t)+x(-t)]/2, Odd part: [x(t)-x(-t)]/2
- Time scaling x(at) compresses for |a|>1, expands for |a|<1
