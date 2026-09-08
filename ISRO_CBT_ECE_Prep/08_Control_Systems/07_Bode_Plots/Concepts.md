# Bode Plots - Concepts

## 1. Introduction
- The **Bode plot** is a frequency-response plot of a transfer function G(jω) evaluated on the imaginary axis.
- Consists of TWO plots:
  1. **Magnitude plot**: 20·log₁₀|G(jω)| (in dB) vs log₁₀(ω).
  2. **Phase plot**: ∠G(jω) (in degrees) vs log₁₀(ω).
- Uses logarithmic frequency axis (decades) and logarithmic (or linear in dB) magnitude scale.
- Straight-line asymptotic approximations are used for easy hand-drawing.

## 2. Why Bode Plots Matter
- Quickly determine stability margins (gain margin, phase margin) graphically.
- Identify transfer function from the magnitude/phase plot (ISRO favorite).
- Design compensators (lead, lag).
- Analyze system behavior over frequency without solving for roots.

## 3. Standard Form for Bode Plotting
Write G(s) in time-constant form:
G(s) = K₀ · Π(1+sτ_i) / [s^N · Π(1+sT_j)]

Where:
- K₀ = gain constant (constant term), includes effect of integrators count.
- N = number of integrators (poles at origin) → type number.
- Real poles: factors (1+sT), corner at ω=1/T.
- Real zeros: factors (1+sτ), corner at ω=1/τ.

## 4. Magnitude Plot Construction (Asymptotes)
- **Constant K₀**: horizontal line at 20log₁₀(K₀) dB.
- **Integrator 1/s**: -20 dB/decade straight line through 0 dB at ω=1.
- **Second integrator 1/s²**: -40 dB/decade.
- **Real pole (1+sT)⁻¹**: flat 0 dB until ω=1/T, then -20 dB/decade (slope change).
- **Real zero (1+sτ)**: flat 0 dB until ω=1/τ, then +20 dB/decade.
- **Complex pole pair**: -40 dB/decade after ω_n, with resonance peak 20log₁₀(1/(2ζ√(1-ζ²))) near ω_n.

### Corner Frequencies
- Each real pole/zero introduces a corner (break) frequency at ω = 1/T (or 1/τ).
- Slopes are added: total slope after each corner accumulates.

### Starting Slope
- For a type N system (N integrators): starting slope = -20N dB/decade.
- Leftmost (lowest frequency) asymptote has slope -20N dB/dec.

## 5. Phase Plot Construction
- **Constant K₀**: contributes 0° (if positive) or 180° (if negative).
- **Integrator 1/s**: -90° throughout.
- **Real pole (1+sT)⁻¹**: starts at 0°, -45° at corner, asymptotes -90°.
- **Real zero (1+sτ)**: 0°, +45° at corner, +90°.
- **Complex pole pair**: 0° to -180° transition around ω_n.
- Phase plot is twice the slope contributions summed.

## 6. Reading the Bode Plot

### Gain Margin (GM)
- Find frequency where phase = -180° (phase crossover frequency ω_pc).
- Gain margin = 0 dB − |G(jω)|dB at ω_pc = -(magnitude in dB at phase crossover).
- Also GM = 1/|G(jω_pc)| (linear) = -20log₁₀|G(jω_pc)| dB.

### Phase Margin (PM)
- Find frequency where |G(jω)| = 1 (0 dB) → gain crossover frequency ω_gc.
- PM = 180° + ∠G(jω_gc).
- PM measures how much additional phase lag would cause instability.

## 7. Transfer Function Identification from Bode
Given a Bode magnitude plot:
1. Identify the low-frequency slope (gives number of integrators / type number).
2. Read DC/zero-frequency gain from the flat low-frequency portion.
3. Locate corner frequencies (where slope changes).
4. Each -20 dB/dec step-down = a real pole (or complex pole pair = -40 dB/dec).
5. Each +20 dB/dec = a real zero.
6. Determine K from the magnitude at ω=1 or the low-freq gain.
7. Check the starting slope: if it starts at +20N, there are N differentiators.

## 8. Complex Conjugate Poles (Second-Order Factor)
- Factor: 1/(s²/ω_n² + 2ζs/ω_n + 1).
- Corner at ω = ω_n.
- Magnitude asymptotes: 0 dB until ω_n, then -40 dB/decade.
- Resonance peak near ω_n (close to ω_r = ω_n√(1-2ζ²) for 0<ζ<0.707).
- Peak magnitude ≈ 1/(2ζ√(1-ζ²)).
- Phase: 0° → -180° in a step of -90°/decade transition.

## 9. Non-minimum phase (RHP zeros, delay)
- RHP zero (1-sτ) or delay: phase decreases (adds lag) while magnitude behaves like LHP zero.
- Delay e^{-jωT}: magnitude unchanged, phase adds -(ωT) in radians (= -57.3·ωT degrees).

## 10. Bode vs Other Frequency Methods
- Bode: magnitude & phase separately, good for additivity (logarithmic).
- Nyquist: single complex plane plot, handles the whole frequency range including negative frequencies, better for delay analysis.
- Bode more common for compensator design since margins read directly.

## 11. ISRO Commonly Tests
- Identify transfer function from Bode slope/corners.
- Compute gain/phase margins from Bode.
- Determine K for specified phase margin.
- Recognize slope changes at corner frequencies.

## 12. Resonance & Quality Factor
For a second-order system with damping ζ:
- Q factor = 1/(2ζ) (relationship).
- Peak magnitude in dB = 20log₁₀(Q) = 20log₁₀(1/(2ζ)) approximately for small ζ.
- Less resonant peak with larger ζ.
