# Drift & Diffusion - Practice Questions (ISRO Style)

## Q1. Drift Current Density
**In Si with n = 10¹⁶ cm⁻³, μn = 1350 cm²/V·s, and E = 100 V/cm, the electron drift current is:**

(a) 216 A/cm²
(b) 2.16 A/cm²
(c) 21.6 A/cm²
(d) 2160 A/cm²

**Answer: (a)**
**Explanation:** J = qnμnE = 1.6×10⁻¹⁹ × 10¹⁶ × 1350 × 100 = 0.216 A/cm² × 1000 = 216 A/cm². Let me verify: 1.6×10⁻¹⁹×10¹⁶ = 1.6×10⁻³. ×1350 = 2.16. ×100 = 216 A/cm². Yes.

---

## Q2. Diffusion Current
**Given Dn = 35 cm²/s, dn/dx = 10²⁰ cm⁻⁴, the electron diffusion current density is:**

(a) 560 A/cm²
(b) 56 A/cm²
(b) 5.6 A/cm²
(d) 5600 A/cm²

**Answer: (a)**
**Explanation:** J = qDn(dn/dx) = 1.6×10⁻¹⁹ × 35 × 10²⁰ = 1.6×35×10 = 560 A/cm²

---

## Q3. Einstein Relation
**The diffusion coefficient of holes in Si (μp = 480 cm²/V·s) at 300K is:**

(a) 12.5 cm²/s
(b) 24 cm²/s
(c) 35 cm²/s
(d) 48 cm²/s

**Answer: (a)**
**Explanation:** Dp = μpVT = 480 × 0.026 = 12.48 cm²/s ≈ 12.5 cm²/s

---

## Q4. Diffusion Length
**Given Dp = 12.5 cm²/s and τp = 100 μs, the hole diffusion length is:**

(a) 35 μm
(b) 354 μm
(c) 112 μm
(d) 125 μm

**Answer: (b)**
**Explanation:** Lp = √(Dpτp) = √(12.5 × 100×10⁻⁶) = √(1.25×10⁻³) = 0.0354 cm = 354 μm

---

## Q5. Excess Carrier Decay
**The excess minority carrier concentration decays with distance according to:**

(a) Δp(x) = Δp(0)·sin(x/L)
(b) Δp(x) = Δp(0)·exp(-x/L)
(c) Δp(x) = Δp(0)·(1-x/L)
(d) Δp(x) = Δp(0)/x²

**Answer: (b)**
**Explanation:** Δp(x) = Δp(0)·exp(-x/L). Exponential decay with diffusion length L.

---

## Q6. Total Current
**The total current density in a semiconductor is:**

(a) Jdrift + Jdiff
(b) Jdrift - Jdiff
(c) |Jdrift| - |Jdiff|
(d) Jdrift × Jdiff

**Answer: (a)**
**Explanation:** J = Jdrift + Jdiff = σE + qDn(dn/dx) - qDp(dp/dx)

---

## Q7. Drift Velocity
**The drift velocity of electrons in Si with μn = 1350 cm²/V·s and E = 1000 V/cm is:**

(a) 1.35 × 10⁶ cm/s
(b) 1.35 × 10⁵ cm/s
(c) 1.35 × 10⁷ cm/s
(d) 1.35 × 10⁴ cm/s

**Answer: (a)**
**Explanation:** vd = μnE = 1350 × 1000 = 1.35 × 10⁶ cm/s

---

## Q8. Diffusion Current Sign
**When holes diffuse from high to low concentration along +x direction, the hole diffusion current is:**

(a) Positive
(b) Negative
(c) Zero
(d) Depends on field

**Answer: (b)**
**Explanation:** Jp,diff = -qDp(dp/dx). Since dp/dx < 0 (decreasing), Jp > 0, but for x increasing... Actually current due to holes moving +x is positive (treating holes as positive charges). Jp,diff = -qDp(dp/dx), with dp/dx negative → positive current.

---

## Q9. Conductivity
**The conductivity of Si with n = 10¹⁶, p = 10⁴, μn = 1350, μp = 480 at 300K is:**

(a) 2.16 S/cm
(b) 0.216 S/cm
(c) 21.6 S/cm
(d) 0.0216 S/cm

**Answer: (a)**
**Explanation:** σ = q(nμn + pμp) = 1.6×10⁻¹⁹ × (10¹⁶×1350 + 10⁴×480) ≈ 1.6×10⁻¹⁹ × 1.35×10¹⁹ = 2.16 S/cm

---

## Q10. Einstein Relation Temperature
**At 400K, the value of kT/q is:**

(a) 26 mV
(b) 34.5 mV
(c) 30 mV
(d) 40 mV

**Answer: (b)**
**Explanation:** VT = kT/q = 25.85 × (400/300) = 34.5 mV

---

## Q11. Recombination Rate
**The recombination rate for excess carriers is given by:**

(a) R = Δp·τ
(b) R = Δp/τ
(c) R = τ/Δp
(d) R = Δp²/τ

**Answer: (b)**
**Explanation:** R = Δp/τ. Proportional to excess concentration, inversely to lifetime.

---

## Q12. Diffusion from Junction
**At the edge of a forward-biased junction, the minority carrier concentration is:**

(a) np0
(b) np0·exp(V/VT)
(c) ni
(d) ND

**Answer: (b)**
**Explanation:** np(0) = np0·exp(V/VT). Injection increases minority concentration exponentially.

---

## Q13. Continuity Equation
**The continuity equation relates:**

(a) Current and voltage
(b) Charge accumulation to current flow, generation, and recombination
(c) Drift and diffusion
(d) Mobility and diffusion

**Answer: (b)**
**Explanation:** ∂n/∂t = (1/q)∂Jn/∂x + G - R. Relates carrier accumulation to current divergence, generation, and recombination.

---

## Q14. Steady State
**In steady state, ∂p/∂t = 0. The minority carrier diffusion equation becomes:**

(a) Dp·d²Δp/dx² = Δp/τ
(b) Dp·d²Δp/dx² = 0
(c) dΔp/dx = 0
(d) Δp = constant

**Answer: (a)**
**Explanation:** Steady state: Dp·d²Δp/dx² - Δp/τp = 0 → diffusion balances recombination.

---

## Q15. Junction Current
**The reverse saturation current Is of a Si diode is proportional to:**

(a) ni
(b) ni²
(c) ni³
(d) √ni

**Answer: (b)**
**Explanation:** Is ∝ n_i² (from pn0 = ni²/ND and np0 = ni²/NA).

---

## Q16. Drift vs Diffusion Region
**In a forward-biased PN junction, the current is dominated by:**

(a) Drift in neutral regions
(b) Diffusion of minority carriers
(c) Both equally
(d) Neither

**Answer: (b)**
**Explanation:** Minority carrier diffusion in neutral regions dominates forward current.

---

## Q17. Fick's Law
**Diffusion current follows which law?**

(a) Ohm's law
(b) Fick's law
(c) Kirchhoff's law
(d) Joule's law

**Answer: (b)**
**Explanation:** Fick's first law relates flux to concentration gradient. Diffusion current follows this.

---

## Q18. High-Level Injection
**In high-level injection in N-type Si:**

(a) Δp << ND
(b) Δp ≈ ND
(c) Δp >> ND
(d) Δp = 0

**Answer: (b)**
**Explanation:** High-level injection: Δp comparable to/decreases ND. Majority carrier concentration changes.

---

## Q19. Auger Recombination
**Auger recombination is important at:**

(a) Low doping
(b) High carrier concentrations
(c) Low temperature
(d) High field only

**Answer: (b)**
**Explanation:** R_Aug = Cn·n²p + Cp·p²n. Proportional to n²p, significant at high concentrations.

---

## Q20. Diffusion Current Equation
**The electron diffusion current density is:**

(a) Jn = qDn(dn/dx)
(b) Jn = -qDn(dn/dx)
(c) Jn = qnDnE
(d) Jn = qnμnE

**Answer: (a)**
**Explanation:** Jn,diff = qDn(dn/dx). Positive sign for electrons (opposite to holes).

---

## Q21. Majority Carrier Current
**In a uniformly doped N-type resistor with applied voltage, current is dominated by:**

(a) Electron drift
(b) Hole drift
(c) Electron diffusion
(d) Hole diffusion

**Answer: (a)**
**Explanation:** Uniform doping → no gradient → no diffusion. Electron drift dominates.

---

## Q22. Transit Time
**The transit time for carriers crossing a 1 μm base with velocity 10⁶ cm/s is:**

(a) 1 ps
(b) 10 ps
(c) 100 ps
(d) 1 ns

**Answer: (c)**
**Explanation:** t = distance/velocity = 1×10⁻⁴ cm/10⁶ cm/s = 10⁻¹⁰ s = 100 ps

---

## Q23. Einstein Relation Validity
**The Einstein relation is strictly valid for:**

(a) Degenerate semiconductors
(b) Non-degenerate semiconductors
(c) Metallic conductors
(d) All materials

**Answer: (b)**
**Explanation:** Einstein relation assumes Boltzmann statistics → valid for non-degenerate semiconductors.

---

## Q24. Diffusion Capacitance
**The diffusion capacitance of a diode is proportional to:**

(a) Forward current
(b) Reverse current
(c) Junction area
(d) Reverse voltage

**Answer: (a)**
**Explanation:** Cd = τ·I/VT. Proportional to forward current (stored minority charge).

---

## Q25. Drift Current in Depletion
**In the depletion region of a reverse-biased diode:**

(a) Only diffusion current
(b) Only drift current
(c) Both drift and diffusion
(d) No current

**Answer: (b)**
**Explanation:** Depletion region has high field → carriers swept by drift (generation current).

---

## Q26. Optical Generation
**If optical generation G is uniform and steady, the excess carrier concentration is:**

(a) Δp = G/τ
(b) Δp = Gτ
(c) Δp = Gτ²
(d) Δp = G²τ

**Answer: (b)**
**Explanation:** Steady state: G = R = Δp/τ → Δp = Gτ
