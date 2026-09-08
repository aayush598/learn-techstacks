# Gain & Phase Margins - Formulas

## 1. Phase Crossover Frequency (ω_pc)
Solved from:
∠G(jω_pc)H(jω_pc) = −180°

## 2. Gain Crossover Frequency (ω_gc)
Solved from:
|G(jω_gc)H(jω_gc)| = 1  (0 dB)

## 3. Gain Margin
GM (dB) = −20·log₁₀|G(jω_pc)H(jω_pc)|
GM (linear) = 1/|G(jω_pc)H(jω_pc)|

### Interpretation
- GM > 0 dB → stable (for P=0).
- GM < 0 dB → unstable.
- GM = +∞ (no crossing) → phase never reaches −180°.

## 4. Phase Margin
PM = 180° + ∠G(jω_gc)H(jω_gc)

### Interpretation
- PM > 0° → stable (for P=0).
- PM < 0° → unstable.
- PM = 0° → marginal.

## 5. PM ↔ Damping Ratio (Second Order)
PM ≈ 100°·ζ     (approx., 0 ≤ ζ ≤ 0.6)

Exact:
PM = tan⁻¹[ 2ζ / √(√(1+4ζ⁴) − 2ζ²) ]

## 6. ζ from PM (inverse)
Approx: ζ ≈ PM/100 (PM in degrees).
More precise iterative solving of the above.

## 7. Overshoot from PM (via ζ)
%OS = 100·e^{−πζ/√(1−ζ²)}

### Approx
OS ≈ 100·e^{−π·(PM/100)/√(1−(PM/100)²)}

## 8. Delay Reduction of PM
PM_reduced = PM_original − (57.3·ω_gc·τ)
τ = delay (seconds), ω_gc in rad/s. 57.3 converts radians to degrees.

## 9. Maximum Phase Margin & Crossover (for compensation)
The lead compensator adds phase; design formula involves the new gain crossover.

## 10. Second-Order Bandwidth
ω_bw = ω_n·√(1−2ζ²+√(4ζ⁴−4ζ²+2))

## 11. Relationship: Resonance Peak M_r
M_r = 1/(2ζ√(1−ζ²))
Higher M_r → lower PM.

## 12. Recommended Design Values
- PM: 30°–60° (target ~45°).
- GM: ≥ 6 dB (typically 6–12 dB).

## 13. Percent Overshoot as Function of PM (approximate tables)
| ζ | PM (approx) | %OS |
|---|---|---|
| 0.2 | 22° | 52% |
| 0.3 | 30° | 37% |
| 0.4 | 40° | 25% |
| 0.5 | 50° | 16% |
| 0.6 | 60° | 9.5% |
| 0.7 | 65° | 5% |

## Formula Cheatsheet (Margins)
| Quantity | Formula |
|---|---|
| ω_pc | ∠GH = −180° |
| ω_gc | |GH| = 1 |
| GM (dB) | −20log₁₀|GH(jω_pc)| |
| GM (linear) | 1/|GH(jω_pc)| |
| PM | 180° + ∠GH(jω_gc) |
| PM≈ζ | 100·ζ (deg) |
| %OS | 100·e^{−πζ/√(1−ζ²)} |
| Delay dPM | −57.3·ω_gc·τ |
| M_r | 1/(2ζ√(1−ζ²)) |

## Notes
- All margin formulas assume open-loop stable (P=0).
- For systems with multiple −180° crossings, compute GM at the critical one(s) — conditionally stable systems.
- Margins from Bode and Nyquist agree mathematically.

## 14. Computing ω_gc and ω_pc for a Given TF

### Gain crossover ω_gc
Solve |G(jω)H(jω)| = 1.
For type 1 system G=K/[s(1+sT₁)(1+sT₂)...]:
ω_gc satisfies K/[ω·Π√(1+(ωTᵢ)²)] = 1.
If corners are far above crossover (ω<<1/Tᵢ), approximate ω_gc ≈ K.

### Phase crossover ω_pc
Solve ∠GH(jω) = −180°.
For type 1: −90°−Σ atan(ωTᵢ) = −180° → Σ atan(ωTᵢ) = 90°.
Solve for ω_pc.

## 15. Reading Margins Quickly on Bode
- At the 0 dB crossing (gain crossover), the phase above −180° = PM.
- At the −180° phase crossing, the dB value below 0 = GM (positive when below).
- Positive PM & GM → stable.

## 16. Design for Specified PM (analytical)
1. Desired PM given → desired ζ via ζ≈PM/100 (or exact), then desired overshoot known.
2. Find ω where phase = −180° + PM_desired + safety margin.
3. Compute |G| at that ω and set K = 1/|G|.

## 17. Connection Between GM, PM, and Model Uncertainty
- GM ≥ 6 dB ensures gain variations up to ~×2 are tolerated.
- PM ≥ 45° keeps overshoot modest and handles mild delay.
- Design margin rule: "aim PM 45° + 10° buffer, GM ≥ 6 dB."

## 18. Worked Margin Calculation Example
G(s) = 10/[s(1+0.1s)(1+0.01s)]:
- ω_gc: at low freq ≈ 10 rad/s (approx, since corners at 10,100 are ≥ crossover).
- phase at ω=10: −90−atan(1)−atan(0.1) = −90−45−5.7 = −140.7°.
- PM = 180−140.7 = 39.3°.
- ω_pc: −90−atan(0.1ω)−atan(0.01ω) = −180 → atan(0.1ω)+atan(0.01ω)=90 → ω→∞, so no finite crossing → GM=+∞.

## 19. Fast π-rule for PM from ζ
For quick MCQs: **PM ≈ 100·ζ** (degrees) is accurate enough for ζ ≤ 0.6 to identify the right option.
