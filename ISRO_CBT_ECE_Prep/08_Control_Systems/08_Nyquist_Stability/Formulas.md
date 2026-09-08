# Nyquist Stability - Formulas

## 1. Encirclement Criterion
**Z = N + P**

- Z = # closed-loop poles in RHP.
- N = # CCW encirclements of point (−1,0) by Nyquist plot.
- P = # open-loop poles (of G(s)H(s)) in RHP.

### Stability condition
Stable ⇔ Z = 0 ⇔ N = −P

(Must encircle −1 exactly −P times in counterclockwise... P times CCW if P open-loop RHP poles, i.e., N=P usually meaning P CCW encirclements for unstable open-loop.)

Careful: With the standard clockwise Nyquist contour:
- For stable closed loop with P open-loop RHP poles → require N (CCW net) = P.

## 2. Characteristic Equation
1 + G(s)H(s) = 0

Zeros of 1+GH = closed-loop poles.
Poles of 1+GH = open-loop poles.
Encirclement of −1 by GH ⇔ encirclement of 0 by (1+GH).

## 3. Gain Margin from Nyquist
GM (linear) = 1/|G(jω_pc)H(jω_pc)|
GM (dB) = −20log₁₀|G(jω_pc)H(jω_pc)|
Where ω_pc = frequency where GH crosses negative real axis (phase=−180°).

If plot crosses negative real axis at multiple points (conditionally stable), there are multiple GMs.

## 4. Phase Margin from Nyquist
ω_gc: freq where |GH|=1 (unit circle crossing).
PM = 180° + ∠GH(jω_gc)

Geometrically: angle from negative real axis to the point where plot crosses unit circle.

## 5. Mapping of a Pole at Origin (indentation)
For a system with pole at s=0, indentation (small RHP semicircle at origin) maps to an infinite-radius arc on Nyquist:
- G(s)≈K/s near origin → as s goes 0⁻→0⁺ around, GH sweeps infinite arc.
- For type 1: arc goes from −180° to +180° (left).
- For type 2 (two integrators): arc adds 360° more, etc.

Magnitude → ∞, phase rotates accordingly.

## 6. Nyquist Contour Path
1. jω axis: ω: 0→+∞.
2. Large RHP semicircle: s = Re^{jθ}, R→∞, θ:90°→−90° (maps to origin for strictly proper GH).
3. jω axis: ω: −∞→0.
4. Small semicircles around jω poles (origin): indentation into RHP.
5. Encircles entire RHP clockwise.

## 7. Number of Infinite-Radius Arcs
= number of poles of GH on the jω axis (e.g., integrators at or near origin).

## 8. Number of CCW Encirclements (counting)
- Consider a ray from −1 to ∞ along the real axis.
- Count directed crossings.
- Or use the "point test": number of times the plot rotates around −1.

## 9. Stability Check for Common P Values
| P (open-loop RHP poles) | Required N (CCW encirclements of −1) |
|---|---|
| 0 | 0 (no encirclement) |
| 1 | 1 |
| 2 | 2 |
| P | P |

## 10. Marginal Stability
If Nyquist plot passes exactly through −1: closed loop has poles on imaginary axis → marginally stable / sustained oscillation at that frequency.

## 11. Conditionally Stable System Condition
- Plot crosses negative real axis at TWO (or more) distinct points.
- Stability holds for intermediate gain K but fails for too-high or too-low K.
- Gain range: between two critical gains K1 < K < K2.

## 12. Closed-Loop TF from Open-Loop (Nyquist context)
T(s) = G(s) / [1 + G(s)H(s)]

## 13. Static Error Constants from Nyquist (limiting behavior)
- Type 0: GH(0) = K_p (position constant, finite start on real axis).
- Type 1: approaches −∞ as ω→0 (various).
- Type 2: etc.

## Formula Cheatsheet (Nyquist)
| Quantity | Formula |
|---|---|
| Encirclement | Z = N + P |
| Stable | Z = 0 (N = −P) |
| GM linear | 1/|GH(jω_pc)| |
| GM dB | −20log₁₀|GH(jω_pc)| |
| PM | 180°+∠GH(jω_gc) |
| CL poles | zeros of 1+GH |
| OL poles | poles of GH |

## Relationships
- Gain margin & phase margin both read from Nyquist plot.
- Positive GM/PM → stable (for P=0 systems).
- Crossings of −1 correspond to the stability boundaries.

## 14. Margin Formulae from the Nyquist Plot (Geometric)
- ω_pc: the point where GH(jω) is real and negative.
- ω_gc: the point where |GH(jω)|=1.
- GM = 1/|GH(jω_pc)| — read the real-axis distance.
- PM = 180° + ∠GH(jω_gc) — read at unit-circle intersection.

## 15. Encirclement Counting Method (Routine)
1. Draw a "star" ray from −1 to −∞ along the negative real axis.
2. Count each crossing of the Nyquist plot over that ray with a direction sign.
3. Net directed count = N.

## 16. Effect of a Gain Multiplier K on the Plot
Multiplying GH by K scales the plot radially about origin. Encirclements of −1 change when the plot passes through −1 (marginal). The critical gains are where the plot crosses −1.

## 17. Nyquist Formula for Systems with Delay
G(s)H(s) = GH₀(s)·e^{−sT}
- Magnitude unchanged: |GH| = |GH₀|.
- Phase extra: −ωT (radians) → can drastically change encirclements.
- Analyze with Bode-style phase for margining, still encircle −1.

## 18. Nyquist Loop: Number of Infinite Arcs
= multiplicity of pole at origin (or at any jω location indented). Each pole at origin adds a 180° sweep at infinity.

## 19. Quick Relation of Nyquist to Bode Margins
Both give GM/PM; Nyquist is a single contour, Bode decouples magnitude and phase. Choose Nyquist for delay/non-minimum-phase clarity.

## 20. Encirclement ↔ Sign Change Summary
| Z | Meaning |
|---|---|
| 0 | stable closed loop |
| 1,2,... | that many RHP closed-loop poles (unstable) |
