# Gain & Phase Margins - Concepts

## 1. Definitions

### Gain Margin (GM)
- The amount by which the open-loop gain can be **increased** before the closed-loop system becomes unstable (for stable systems).
- Evaluated at the **phase crossover frequency** (where phase = −180°).
- GM = −20log₁₀|G(jω_pc)H(jω_pc)|.

### Phase Margin (PM)
- The amount of additional **phase lag** that can be added to the open-loop before the system becomes unstable.
- Evaluated at the **gain crossover frequency** (where |GH| = 1, i.e., 0 dB).
- PM = 180° + ∠G(jω_gc)H(jω_gc).

## 2. Interpretation

### Gain Margin
- GM > 0 dB → stable (for P=0 systems).
- GM = 0 dB → marginally stable.
- GM < 0 dB → unstable.
- GM (linear) = 1/|GH(jω_pc)|.

### Phase Margin
- PM > 0° → stable (for P=0).
- PM = 0° → marginally stable.
- PM < 0° → unstable.
- PM directly relates to damping ratio and transient overshoot.

## 3. Computing from Bode Plot
- Find phase crossover ω_pc (phase = −180°), read magnitude → GM.
- Find gain crossover ω_gc (magnitude = 0 dB), read phase → PM.
- Both read directly off the Bode plot.

## 4. Computing from Nyquist Plot
- GM: reciprocal of the distance from origin to the point where plot crosses negative real axis.
- PM: angle from −180° to the point where the plot's unit-circle crossing lies.

## 5. Typical Values for Good Design
- **Phase margin**: 30° to 60° is the sweet spot (commonly 45°).
  - PM < 30° → too oscillatory / near instability.
  - PM ≈ 45° → good trade-off.
  - PM > 60° → more sluggish but robust.
- **Gain margin**: commonly 6 to 12 dB (allows for parameter variation).
  - GM ≥ 6 dB typical.
- Both should be positive with a safety margin for robustness.

## 6. Relationship Between PM and Damping Ratio (Second-Order)
For a standard second-order closed-loop system with dominant poles:
PM ≈ 100·ζ   (approximately, PM in degrees, for 0 ≤ ζ ≤ 0.6)

More exact:
PM = tan⁻¹[ 2ζ / √(√(1+4ζ⁴) − 2ζ²) ]

### Consequences
- ζ=0.707 → PM ≈ 65° (approx).
- ζ=0.5 → PM ≈ 50°.
- ζ=0.3 → PM ≈ 30°.
- Lower ζ → lower PM → more oscillation/overshoot.

### Overshoot-PM Relation
% Overshoot ≈ 100·e^{−πζ/√(1−ζ²)} (via ζ from PM).
Higher PM → lower overshoot.

## 7. Relationship GM ↔ Stability
For type 1 systems and above, GM gives the factor by which gain must be reduced for marginal stability. GM also relates to how close poles are to the jω axis.

## 8. Effect of Gain Change
- Increasing gain: reduces PM (phase margin drops), may reduce GM.
- Decreasing gain: increases margins but slows response.

## 9. Delay Effect
- Transport delay adds phase lag without changing magnitude.
- Reduces the phase margin significantly → destabilizing.
- Delay τ reduces PM by (57.3·ω_gc·τ) degrees.

## 10. Non-minimum phase
- RHP zeros add phase lag; reduce PM.
- Minus sign / RHP poles alter base phase.

## 11. Margin Robustness in Design
- Good design accounts for model uncertainty via adequate GM & PM.
- Higher PM → more robust but slower tracking.

## 12. Typical Margins by Application
- Process control: PM 30–45°, GM 6 dB.
- Servo systems: PM 40–60°, GM 8–12 dB.
- Aerospace: often higher margins (PM 45–60°) for safety.

## 13. ISRO Commonly Tests
- Compute PM from Bode with given magnitude/phase.
- Determine GM from phase-crossover magnitude.
- Given ζ → estimate PM, or vice versa.
- Identify good-margin design choices.

## 14. Margin Caveats
- Margins assume P=0 (open-loop stable); for P>0 apply Nyquist encirclements.
- Margins only valid for the gain/frequency evaluated — multiple crossings give multiple margins (conditionally stable).
- For non-minimum phase systems, positive margins don't guarantee stability.

## 15. Why Both Margins Matter Together
- A system can have good PM but poor GM (e.g., resonant peaks) and vice versa.
- Heresies: large PM does not guarantee large GM — assess both.
- Typical acceptance: PM≥45° AND GM≥6 dB.

## 16. Physical Interpretation Quick-Revision
- GM answers: "How much gain can I add before oscillating?" (gain robustness)
- PM answers: "How much lag/time delay can I tolerate before oscillating?" (delay robustness)
- Both relate distance of the loop to the −1 point on the Nyquist contour.

## 17. Margin → Delay Tolerable (approx)
Max tolerable delay ≈ PM(rad)/ω_gc.
- Directly derived from delay phase = ω·T.
- Quick design guide: T_max ≈ (PM in rad)/ω_gc.

## 18. Reshaping Margins (what moves them)
- Increasing low-frequency gain (lag) → raises error constants, lowers PM a little if done carefully.
- Adding lead → raises PM & crossover.
- Increasing overall gain → lowers PM & GM.
- Reducing gain → raises margins but slows response.

## 19. Typical Graphical Reasoning from Bode
- The more negative the phase at 0 dB, the lower the PM.
- The higher the magnitude at −180°, the smaller (more negative) the GM.
- Slopes near crossover: −20 dB/dec crossing → acceptable; −40 dB/dec or steeper → poor margins.

## 20. Margin Values to Memorize
- PM < 30°: oscillatory, poor.
- PM ≈ 45°: balanced (industry default).
- PM > 60°: sluggish.
- GM < 6 dB: too close to instability for comfort.
- GM 6–12 dB: typical good design.

## 21. Connecting to Time-Domain Specs
- Higher PM → lower overshoot (via ζ ≈ PM/100).
- Higher ω_gc → faster response (lower rise/settling times).
- Thus margins connect frequency-domain design to time-domain specifications.
