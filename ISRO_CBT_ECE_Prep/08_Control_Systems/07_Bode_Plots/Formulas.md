# Bode Plots - Formulas

## 1. Decibel (dB) Definition
|G(jω)|_dB = 20·log₁₀|G(jω)|

## 2. Time-Constant Form for Bode Plotting
G(s) = K₀ · Π(1+sτᵢ) / [s^N · Π(1+sTⱼ)]

- N = number of integrators (type number).
- Corner (break) frequencies: ω = 1/τᵢ (zeros), ω = 1/Tⱼ (poles).

## 3. Magnitude of Individual Factors

### Constant C
Magnitude: 20·log₁₀|C| dB (horizontal), phase 0°.

### s^N (integrator, N>0)
Magnitude: -20·N·log₁₀(ω)  (−20N dB/decade line).
At ω=1: 0 dB. Phase: -90·N degrees.

### Real pole (1+jωT)⁻¹
Magnitude: 0 dB for ωT<<1; −20log₁₀(ωT) for ωT>>1.
Corner at ω=1/T.
Phase: 0°→(at ω=1/T)−45°→−90°.

### Real zero (1+jωτ)
Magnitude: 0 dB for ωτ<<1; +20log₁₀(ωτ) for ωτ>>1.
Corner at ω=1/τ. Phase: 0°→+45°→+90°.

### Complex pole pair 1/(1+2ζjω/ω_n+(jω/ω_n)²)
Corner at ω=ω_n. Slope -40 dB/decade.
Resonant peak (ω<ω_n, ζ<0.707):
M_r ≈ 1/(2ζ√(1−ζ²))
Peak frequency: ω_r = ω_n·√(1−2ζ²)

### Delay e^{-jωT}
Magnitude: 0 dB. Phase: −57.3·ω·T degrees.

## 4. Total Magnitude (sum of factors, in dB)
|G(jω)|_dB = Σ(contributions of each factor) — addition in dB.

## 5. Total Phase
∠G(jω) = Σ(phase contributions of each factor).

## 6. Slope Rules
- Each real pole of order N: −20·N dB/decade added after its corner.
- Each real zero of order M: +20·M dB/decade added after its corner.
- Each complex pole pair: −40 dB/decade after ω_n.
- Integrator(s) at origin: starting slope −20N dB/dec.
- Differentiators (s^M numerator): starting slope +20M dB/dec.

## 7. Starting Slope
For type N system: starting magnitude slope = −20N dB/decade.
Starting phase = −90·N degrees.

## 8. Gain Margin (from Bode)
ω_pc = phase crossover freq (where ∠G(jω) = −180°).
GM (dB) = −20log₁₀|G(jω_pc)| = 0 dB − (magnitude dB at ω_pc).
GM (linear) = 1/|G(jω_pc)|.

## 9. Phase Margin (from Bode)
ω_gc = gain crossover freq (where |G(jω)| = 1, i.e. 0 dB).
PM = 180° + ∠G(jω_gc).

## 10. Gain Margin for Systems with Integrator/Bode typical
For G(s)=K/[s(1+T1s)(1+T2s)...].
- Compute PM = 180° + phase(gain crossover).
- GM computed at phase crossover.

## 11. Frequency Where |G|=1 for PM Calculation
Actually solve |G(jω)|=1 → ω_gc.
For a given K, ω_gc found from magnitude equation.

## 12. Setting K to Achieve a Desired PM
1. Find ω where ∠G(jω) = −180° + PM_desired.
2. At that ω, compute |G(jω)| without K (normalized).
3. K = 1/(|G(jω)|_norm).

## 13. Transfer Function from Bode (Identification)
Steps/formulas:
- Low-freq slope → type number (integrators N).
- Low-freq magnitude value → gain K₀ (then gain margin/DC).
- Corner frequencies (slope changes) → pole/zero time constants T=1/ω_c.
- Each −20dB/dec slope → one real pole; −40dB/dec → complex pair; +20 → zero.
- Write: G(s)=K₀·Π(1+sτᵢ)/[s^N Π(1+sTⱼ)].
- Verify at ω=1: magnitude = 20log|K₀| (if no other contributors at ω=1).

## 14. Corner Frequency for Second-Order Factor
ω_n from location slope changes twice step (-40).
Resonance check with ζ.

## 15. Bode Plot Relation to Damping
For closed-loop second order with dominant poles:
PM ≈ 100·ζ (approx.), valid 0<ζ<0.6 (approximation).
More exactly: PM roughly correlates to ζ; lower ζ → lower PM.

## Formula Cheatsheet (Bode)
| Item | Formula |
|---|---|
| Magnitude (dB) | 20log₁₀|G| |
| Pole corner | ω=1/T (slope −20dB/dec) |
| Zero corner | ω=1/τ (slope +20dB/dec) |
| Complex pair | ω_n, −40dB/dec, peak 1/(2ζ√(1−ζ²)) |
| Starting slope | −20N dB/dec (type N) |
| GM (dB) | −20log₁₀|G(jω_pc)| |
| PM | 180°+∠G(jω_gc) |
| ω_r | ω_n√(1−2ζ²) |
| PM≈ζ | ~100·ζ (deg) |
