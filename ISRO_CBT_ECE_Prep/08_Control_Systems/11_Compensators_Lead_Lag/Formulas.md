# Compensators (Lead, Lag) - Formulas

## 1. Lead Compensator Transfer Function
G_c(s) = K_c·(1+αTs)/(1+Ts),   α > 1

Or:
G_c(s) = K_c·(s + 1/αT)/(s + 1/T)

- Zero at s = −1/αT.
- Pole at s = −1/T.
- Since α>1, zero is closer to origin.

## 2. Maximum Phase Lead
φ_max = sin⁻¹[ (α−1) / (α+1) ]

### Inverse (find α for given φ_max)
α = (1 + sinφ_max) / (1 − sinφ_max)

## 3. Frequency of Maximum Phase Lead
ω_max = 1 / (T·√α)

## 4. Magnitude Boost at ω_max
|G_c(jω_max)| = √α
20·log₁₀|G_c(jω_max)| = 10·log₁₀(α)  [dB]

## 5. Zero & Pole Locations (Lead)
- Zero: ω_z = 1/(αT)
- Pole: ω_p = 1/T
- Zero is lower frequency than pole (α>1 → ω_z < ω_p → the zero is BEFORE the pole → phase lead).

## 6. Lag Compensator Transfer Function
G_c(s) = K_c·(1+Ts)/(1+βTs),   0 < β < 1

Or:
G_c(s) = (1 + Ts)/(1 + αTs),  α>1 (this α plays ratio role)

Using convention with β<1:
- Zero: s = −1/T (higher frequency).
- Pole: s = −1/(βT) (lower frequency, closer to origin).
- Pole closer to origin than zero → phase lag.

## 7. Low-Frequency Gain Boost (Lag)
At DC: G_c(0) = 1 (for the (1+Ts)/(1+βTs) normalized form). To boost K, include gain factor.

## 8. Lag Design Frequencies (rule of thumb)
Place pole/zero one decade below crossover:
ω_z = ω_gc/10 (zero at ~1 decade below crossover)
ω_p = ω_z/10 or at 1/(βT) appropriately.

## 9. Lead-Lag Compensator
G_c(s) = K·[(1+αT₁s)/(1+T₁s)]·[(1+T₂s)/(1+βT₂s)]

- First factor: lead (α>1).
- Second factor: lag (β<1).

## 10. Effect on Static Error Constants
- Lead: ±14 K_p/K_v unchanged (mainly transient).
- Lag: increases K_p or K_v → reduces steady-state error.

## 11. Phase Margin Increase from Lead
New PM = old PM + φ_max (adjusting for ω_gc shift) + small safety margin (5–12°).

## 12. Gain Crossover Shift with Lead
The lead raises magnitude by ~10log₁₀(α) dB at ω_max, shifting crossover higher.

## 13. Bandwidth Formulas
Adding lead increases ω_bw (bandwidth) → faster response.
Bandwidth approx rela to ω_gc for type 1 systems.

## Formula Cheatsheet (Compensators)
| Item | Lead | Lag |
|---|---|---|
| TF | (1+αTs)/(1+Ts), α>1 | (1+Ts)/(1+βTs), β<1 |
| φ_max | sin⁻¹(α−1)/(α+1) | negative (lag) |
| ω_max | 1/(T√α) | at low freq |
| Bandwidth | increases | decreases |
| Accuracy | little effect | improves |
| Boost at ω_max | 10log₁₀α dB | ~ none |
| Zero location | closer to origin (lead) | further (lag gives lag) |

## Key Derivations
- To get φ_max: differentiate phase of lead transfer function set tangent condition, giving cosφ = ...
- α from desired φ_max: α = (1+sinφ)/(1−sinφ).

## Design Tip
- Add ~5-10° margin to φ_max to account for crossover shift when computing required α.

## 14. Understanding the Lead Pole-Zero Geometry
- Zero z₀ = −1/(αT), pole p₀ = −1/T.
- Since α>1, |z₀| < |p₀| → zero is closer to origin.
- The zero "pulls" the root-locus/bode phase up (adds +phase between the two corners).
- Net high-frequency gain boost = α (magnitude rises by 20log₁₀α at high freq).

## 15. Understanding the Lag Pole-Zero Geometry
- Zero z₀ = −1/T, pole p₀ = −1/(βT), with β<1 → |p₀| < |z₀| (pole closer to origin).
- Adds negative phase between the two low-frequency corners, but if both are placed far below crossover, the phase lag at crossover is negligible.
- Increases the DC/low-frequency gain (improves K_p/K_v).

## 16. Phase Contribution at a Given ω
For a single factor (jωT + 1):
∠(1+jωT) = atan(ωT).

For lead (1+αTs)/(1+Ts) at ω (mid-band):
Phase = atan(αωT) − atan(ωT) → ranges 0 to φ_max.

## 17. Amplitude at ω for lead
25|G_c(jω)| = √[(1+(αωT)²)/(1+(ωT)²)].
At ω_max, this equals √α.

## 18. Choosing α and T for a Lead (numerical recipe)
1. Pick φ_max (needed + buffer).
2. α = (1+sinφ_max)/(1−sinφ_max).
3. Find the ω_max where the uncompensated |G| equals −10log₁₀α dB, set 1/(T√α)=ω_max → T=1/(ω_max√α).
4. Verify new PM.

## 19. Choosing the Lag parameters (numerical recipe)
1. Determine needed low-freq gain increase β_gain (e.g., to raise K_v).
2. Pick T (or position zero well below ω_gc, e.g., ω_z = ω_gc/10).
3. Place pole at ω_p = ω_z/β ratio to get the gain.
4. Keep the zero at least a decade below crossover to limit PM loss.

## 20. Compensator Selection Quick Table
| Requirement | Compensator |
|---|---|
| Raise PM (lower overshoot) | Lead |
| Raise accuracy (lower e_ss) | Lag |
| Both | Lead-lag |
| PD ≈ lead, PI ≈ lag | circuit equivalents |
