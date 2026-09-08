# ISRO-Specific Shortcuts - Control Systems

## Why These Matter (ISRO Weightage ~8.1%)
ISRO's CBT for ECE repeatedly tests four themes:
1. **Routh array for stability limits** (find K range).
2. **Bode plot → transfer function identification** (from slope/corners).
3. **State-space A/B matrices** (write from TF, controllability).
4. **PID characteristics** (effects of each term + Ziegler-Nichols).

Master these first — they are the highest-yield for the marks.

---

## 1. Routh Hurwitz Fast Hacks

### Third-order shortcut (always test first!)
For s³ + a₂s² + a₁s + a₀ = 0:
**Stable ⇔ a₂·a₁ > a₀** (and all coeffs positive).
- Avoids building the whole array for 90% of 3rd-order questions.

### Second-order
s² + a₁s + a₀ = 0: always stable if a₁,a₀>0. No work needed.

### First-order
s + a = 0: stable if a>0.

### Gain range in 30 seconds
For unity-feedback G(s)=K/[s(s+p₁)(s+p₂)]:
- Product of even-poly terms and check: K_max = p₁·p₂·(sum of other coeffs relationship).
- Char eq = s³+(p₁+p₂)s²+p₁p₂s+K.
- From third-order rule: stable ⇔ (p₁+p₂)·p₁p₂ > K → **K_max = (p₁+p₂)p₁p₂**.
- E.g., G(s)=K/[s(s+2)(s+4)]: K_max = (2+4)·(2·4) = 6·8 = 48 ✓.

### Marginal oscillation frequency
From auxiliary equation (s²-row): ω = √(a₀ of that row).

### Number of RHP roots
= number of sign changes in first column. Highlight first column only.

---

## 2. Bode Plot → Transfer Function Identification

### Reading the slope (bottom-up)
| Starting slope | Means |
|---|---|
| −20 dB/dec | 1 integrator (type 1) |
| −40 dB/dec | 2 integrators (type 2) |
| +20 dB/dec | 1 differentiator |
| 0 dB/dec | type 0 |

### At each corner (slope change)
- Slope decreases by 20 dB/dec → +1 real pole (T=1/ω_corner).
- Slope decreases by 40 dB/dec → complex pole pair (ω_n=ω_corner) OR two coincident real poles.
- Slope increases by 20 dB/dec → +1 real zero.

### Gain K quick estimate
- Type 0: K = 10^(dB₁/20) where dB₁ = flat low-freq magnitude.
- Type 1: read magnitude at ω=1 (or extend −20dB/dec line); K = ω where line crosses 0 dB on the −20 line (if the first decade is pure integrator).
- Two quick relations: on −20N line, |G| at ω=1 = K (approximately) in dB.

### Corner ordering trick
Write T = 1/ω_c in ascending order of ω_c; assign smallest-corner pole first etc.

---

## 3. State-Space Fast Construction

### Controllable canonical (phase-variable) from G(s)
G(s)= (b_{n-1}s^{n-1}+...+b₀)/(s^n + a_{n-1}s^{n-1}+...+a₀):

**A** = companion:
```
[0  1  0 ... 0]
[0  0  1 ... 0]
[  ...       ]
[−a₀ −a₁ −a₂ ... −a_{n-1}]
```
**B** = [0,0,...,1]ᵀ
**C** = [b₀, b₁, ..., b_{n-1}]
**D** = 0 (strictly proper)

Last row of A = negative of denominator coefficients (in order). B final element 1. C = numerator coefficients. Nail this and 90% of matrix questions are solved.

### Controllability (SISO) quick check
det[B AB A²B ...] ≠ 0 → controllable.
For 2×2: det given by easy 2×2.

### Observability quick check
det[C;CA]≠0 → observable.

---

## 4. PID Quick Facts (memorize the table)

| Term | Best for | Harm | Formula |
|---|---|---|---|
| P | fast | offset | K_p·e |
| I | remove offset | oscillation/windup | K_i·∫e |
| D | reduce overshoot | noise | K_d·ė |

### Ziegler-Nichols closed-loop tables (memorize)
| | K_p | T_i | T_d |
|---|---|---|---|
| P | 0.5 K_u | — | — |
| PI | 0.45 K_u | P_u/1.2 | — |
| PID | 0.6 K_u | P_u/2 | P_u/8 |

Memorize PD: 0.6, /2, /8.

---

## 5. Time-Domain Specs Rapid Values (ζ → %OS)
| ζ | %OS |
|---|---|
| 0.2 | ~52% |
| 0.3 | ~37% |
| 0.4 | ~25% |
| 0.5 | ~16% |
| 0.7 | ~4.3% |
| 0.9 | ~0.2% |

Also memorize: **%OS=100·e^{−πζ/√(1−ζ²)}**, t_s=4/(ζω_n), t_p=π/ω_d.

---

## 6. Phase/Gain Margin → ζ maps
PM ≈ 100·ζ (degrees). So ζ=0.5 → PM≈50°, ζ=0.7→70°... gives instant checks.

---

## 7. Quickly Recognizing Lead vs Lag
- Lead: zero closer to origin → (s+a)/(s+b) with a<b → phase lead, α=(b/a).
- Lag: pole closer to origin → (s+a)/(s+b) with a>b → lag.
- φ_max = sin⁻¹((α−1)/(α+1)).

---

## 8. Block-Transfer Quick Links
- Parallel: add.
- Series: multiply.
- Negative feedback: G/(1+GH); positive: G/(1−GH).
- Type number = # poles at origin.

---

## 9. Sampled Data Core
- Stability: poles inside unit circle.
- Tustin: s=(2/T)(z−1)/(z+1).
- ZOH: (1−e^{−sT})/s.
- Nyquist: f_s ≥ 2 f_max.

---

## 10. Exam Time Management
- Numericals worth most: identify the theme instantly (Routh/Bode/State-space/PID).
- Write the standard form first; formulas flow from it.
- Use first-column-only shortcut for Routh to save minutes.
