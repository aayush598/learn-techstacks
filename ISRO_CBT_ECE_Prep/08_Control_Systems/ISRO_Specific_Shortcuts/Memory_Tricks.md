# ISRO-Specific Memory Tricks - Control Systems

## Mnemonics & Memory Aids for Fast Recall

---

## 1. Feedback Formula

**"Speak -AGE":**
- Negative feedback → **A**dds in denominator: G/(1+AGH)... Actually:
- Negative: G/(1+**+**GH)
- Positive: G/(1**−**GH)

**Trick:** Negative feedback contributes a + sign in the denominator. Remember: "Negative = + in denominator" (they pair up: the word **negative** has a + vibe... just memorize):
> **Neg = plus in denom, Pos = minus in denom.**
> Think: "To cancel an error (negative), ADD to denominator."

---

## 2. Lead vs Lag (Zero/Pole position)

**"LEAD ahead, LAG behind"**
- **Lead**: ZERO is closer to origin (ahead of the pole) → adds phase + (leads).
- **Lag**: POLE is closer to origin (behind) → phase −.

**Alternative:** "Zero in front = phase leads" — zero comes first rhythm (Z before P = Lead).

For (s+a)/(s+b): if a<b → lead; if a>b → lag.

---

## 3. Routh Third-Order Condition

**"a₂ a₁ beats a₀"** (twice the middle beats the edge):
Stable ⇔ a₂·a₁ > a₀.
> "2 middles time > last" — like "two friends (a₁,a₂) beat the stranger (a₀)."

---

## 4. Time Constants (τ)

**t_s = 4/(ζω_n) (2%) — "four settling"**
- Settling time "4" (four times constant).
- Peak "π" (π/ω_d) — "pie at peak."
- Rise "(π−angle)" — pi minus angle.

Memorize: **"4 settle, π peak, 3 settle-5%"**

---

## 5. Ziegler-Nichols Numbers

**PID values: "0.6, half, eighth"**
- K_p = 0.6 K_u
- T_i = P_u/2 (half)
- T_d = P_u/8 (eighth)

**PI: "0.45, divide by 1.2"**
**P: "0.5" (half the ultimate)**

Remember: "PID looks at **6**, cuts integral in **half**, derivative in **eighth**."

---

## 6. Overshoot formula

**%OS = 100 e^{−πζ/√(1−ζ²)}**

Mnemonic: "**OverShot** — the exponent is minus **Pi-Jones / root-1-minus-jones²**" e.g., the exponent ∝ ζ.
Visual: "high ζ → small overshoot (large negative exponent)."

Quick memory: "**Ω**vershoot depends on **ζ** only (not ω_n)."

---

## 7. Error Constants

- **K_p** (position): limit of GH.
- **K_v** (velocity): limit of s·GH.
- **K_a** (acceleration): limit of s²·GH.

**"Each step adds an s (order of s)".**
Position=p (power 0), Velocity=v (s¹), Acceleration=a (s²).

**e_ss**: Step→1/(1+K_p), Ramp→1/K_v, Parabolic→1/K_a.
Match "1/K for each except step adds +1."

---

## 8. Type Number → Error

**"Type beats input order":**
If Type ≥ input order, error = 0.
- Step (order 0): Type≥0 → 0 error for Type≥1.
- Ramp (order 1): Type≥1 → 0 error.
- Parabolic (order 2): Type≥2 → 0 error.

Mnemonic: "Type overwhelms the input order → zero error."

---

## 9. Bode Slope Change

**"-20 per real pole, +20 per real zero, -40 per complex pair"**

Mnemonic: **"Pole = 20 (minus), Zero = 20 (plus), Pair = 40 (minus)."**
Double letters: PP(olar) = 40.

---

## 10. Nyquist: Z = N + P

**"Zed is Nope plus Poles"** → Z = N + P.
Stable ⇔ Z=0.
"Encircle the **minus-one** point" (−1,0).

---

## 11. State Space Controllability/Observability

- **Controllability** Qc = [B AB A²B...]: "**C-on = B first** (it's B, AB, ...)."
- **Observability** Qo = [C; CA;...]: "**O-bserve = C first** (C on top)."

Mnemonic: "**C**ontrollability = **B**-matrix first; **O**bservability = **C**-matrix first."
Also: "Controllable = can **C**hange via **B** input; Observable = can **O**bserve via **C** output."

---

## 12. z-Plane Stability

**"Inside the unit circle = safe (stable)."**
z = e^{sT}: LHP (Re s<0) → |z|<1 inside.
"Left side maps Inside" (L → I, both letters).

---

## 13. Lead φ_max formula

φ_max = sin⁻¹[(α−1)/(α+1)],  α=(1+sinφ)/(1−sinφ)

Mnemonic: "**α from φ**: add and minus sine" (1⊕sin over 1⊖sin).

---

## 14. Peak/Corner frequency

- Lead ω_max = 1/(T√α) — "lead peaks at T-root-alpha."
- Pole corner = 1/T.

---

## 15. Frequency → pole map quick values

- Real pole T → corner 1/T.
- Complex pair → ω_n.
- Memory "TIDY": T → I/T... "corner is 1-over-T."

---

## 16. Compensator choice

- Overshoot high (PM low) → **Lead**.
- Steady-state error high → **Lag**.
- Both → **Lead-Lag**.

**"Lead for liveliness, Lag for leeway (accuracy)."**

---

## 17. GM/PM typical values

**"30-60 PM, 6-12 dB GM"** — memorize: PM ~45°, GM ≥6 dB.

---

## 18. Damping relationship to pole geometry

ζ = cos(angle of pole from negative real axis).
Pole at 45° → ζ=0.707 → 4.3% overshoot.
Pole at 60° → ζ=0.5 → 16% OS.
"This is the 45-60-70 triangle of damping."

---

## 19. Root locus asymptotes

Asymptote angles = (2k+1)·180°/(n−m).
- n−m = 2 → ±90°.
- n−m = 3 → 60°,180°,300°.
- n−m = 4 → 45°,135°,225°,315°.
Memorize with mnemonic: "**2→90, 3→60, 4→45**" (angle=180/(n−m) degrees offset).

---

## 20. Final Memory Strips (Top-10 for last-minute)

1. Neg fb: G/(1+GH); Pos: G/(1−GH).
2. Lead=s+a,s+b a<b; Lag a>b.
3. Routh: a₂a₁>a₀.
4. Z-N PID: 0.6, /2, /8.
5. %OS only from ζ.
6. ts=4/(ζωn); tp=π/ωd.
7. Stable z: |z|<1.
8. ZOH: (1−e^{−sT})/s; Tustin s=(2/T)(z−1)/(z+1).
9. Controllable=B-first; Observable=C-first.
10. Type≥input-order → zero error.
