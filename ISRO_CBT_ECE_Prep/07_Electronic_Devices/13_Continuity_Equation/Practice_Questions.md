# Continuity Equation - Practice Questions (ISRO Style)

## Q1. Continuity Equation Form
**The continuity equation for holes (1D) is:**

(a) ∂p/∂t = (1/q)∂Jp/∂x + G - R
(b) ∂p/∂t = -(1/q)∂Jp/∂x + G - R
(c) ∂p/∂t = -(1/q)∂Jp/∂x - G + R
(d) ∂p/∂t = (1/q)∂Jp/∂x

**Answer: (b)**
**Explanation:** For holes: ∂p/∂t = -(1/q)∂Jp/∂x + G - R. Negative sign for holes.

---

## Q2. Transient Decay
**After removing the source, the excess carrier concentration decays as:**

(a) Δp(t) = Δp(0)(1 - t/τ)
(b) Δp(t) = Δp(0)·exp(-t/τ)
(c) Δp(t) = Δp(0)·exp(t/τ)
(d) Δp(t) = Δp(0)·τ/t

**Answer: (b)**
**Explanation:** dΔp/dt = -Δp/τ → Δp(t) = Δp(0)exp(-t/τ). Exponential decay with lifetime.

---

## Q3. Steady State
**In steady state (no generation), the minority carrier diffusion equation is:**

(a) Dp·d²Δp/dx² = Δp/τ
(b) Dp·dΔp/dx = Δp/τ
(c) Dp·d²Δp/dx² = 0
(d) Δp = constant

**Answer: (a)**
**Explanation:** Steady state, no field, no generation: Dp·d²Δp/dx² - Δp/τp = 0 → Dp·d²Δp/dx² = Δp/τp

---

## Q4. Excess Carrier Distribution
**The excess hole concentration in a semi-infinite n-region decays as:**

(a) Δp(x) = Δp(0)(1 - x/L)
(b) Δp(x) = Δp(0)·exp(-x/L)
(c) Δp(x) = Δp(0)sin(x/L)
(d) Δp(x) = Δp(0)·L/x

**Answer: (b)**
**Explanation:** Δp(x) = Δp(0)·exp(-x/Lp). Exponential decay with diffusion length.

---

## Q5. Diffusion Current
**The hole diffusion current at the injection point (x=0) of a semi-infinite region is:**

(a) Jp(0) = qDpΔp(0)/L
(b) Jp(0) = qDpΔp(0)L
(c) Jp(0) = qΔp(0)/L
(d) Jp(0) = DpΔp(0)/L

**Answer: (a)**
**Explanation:** Jp(0) = qDpΔp(0)/Lp. From derivative of exponential at x=0.

---

## Q6. Recombination Rate
**The recombination rate with excess concentration Δp and lifetime τ is:**

(a) Δp·τ
(b) Δp/τ
(c) τ/Δp
(d) Δp²/τ

**Answer: (b)**
**Explanation:** R = Δp/τ. Proportional to excess, inversely to lifetime.

---

## Q7. Uniform Generation
**With uniform optical generation G under steady state, Δp is:**

(a) Gτ
(b) G/τ
(c) Gτ²
(d) G²τ

**Answer: (a)**
**Explanation:** Steady state: G = R = Δp/τ → Δp = Gτ

---

## Q8. Lifetime Effect
**If the minority carrier lifetime is halved, the diffusion length:**

(a) Halves
(b) Decreases by √2
(c) Doubles
(d) Quadruples

**Answer: (b)**
**Explanation:** L = √(Dτ). If τ halves, L decreases by √2.

---

## Q9. Surface Recombination
**Surface recombination velocity reduces:**

(a) Bulk lifetime
(b) Effective lifetime
(c) Mobility
(d) Diffusion constant

**Answer: (b)**
**Explanation:** 1/τeff = 1/τbulk + 1/τsurface. Surface recombination reduces effective lifetime.

---

## Q10. Collector Current
**The collector current of a BJT is related to minority carriers by:**

(a) IC = qADn·np0/Ln·exp(VBE/VT)
(b) IC = qADn·np0·exp(VBE/VT)
(c) IC = qADn/Ln·exp(VBE/VT)
(d) IC = qADn·np0/Ln·VBE

**Answer: (a)**
**Explanation:** IC = qADn·np0/Ln·[exp(VBE/VT) - 1]. Driven by minority carrier diffusion in base.

---

## Q11. Delta p at x=L
**At x = L (diffusion length), the excess carrier concentration is:**

(a) Δp(0)/2
(b) Δp(0)/e
(c) Δp(0)/e²
(d) Δp(0)/√2

**Answer: (b)**
**Explanation:** Δp(L) = Δp(0)·exp(-1) = Δp(0)/e ≈ 0.368Δp(0)

---

## Q12. Continuity for Electrons
**For electrons, the continuity equation has which sign on Jn term?**

(a) Positive
(b) Negative
(c) Zero
(d) Depends on field

**Answer: (a)**
**Explanation:** ∂n/∂t = (1/q)∂Jn/∂x + G - R. Positive sign for electrons.

---

## Q13. Generation-Recombination Balance
**The generation-recombination lifetime τ is defined when:**

(a) G > R
(b) G = R
(c) G < R
(d) G = 0

**Answer: (b)**
**Explanation:** At equilibrium, G = R = n_i/τ. Net generation when perturbed.

---

## Q14. Thin Sample Approximation
**For a thin sample (W << L), the excess carrier distribution is:**

(a) Exponential
(b) Linear
(c) Sinusoidal
(d) Constant

**Answer: (b)**
**Explanation:** Δp(x) ≈ Δp(0)(1 - x/W). Linear approximation for W << L.

---

## Q15. Surface Recombination Boundary
**The boundary condition at a surface for minority carriers includes:**

(a) Dp·dΔp/dx = s·Δp
(b) Δp = 0 always
(c) dΔp/dx = 0 always
(d) Δp = Δp(0)

**Answer: (a)**
**Explanation:** Dp·dΔp/dx|x=W = -s·Δp(W). Surface recombination velocity boundary condition.

---

## Q16. Effective Lifetime
**If τbulk = 10 μs and τsurface = 5 μs, the effective lifetime is:**

(a) 15 μs
(b) 3.3 μs
(c) 7.5 μs
(d) 5 μs

**Answer: (b)**
**Explanation:** 1/τeff = 1/10 + 1/5 = 0.1 + 0.2 = 0.3 → τeff = 3.33 μs

---

## Q17. Recombination in Depletion
**In the depletion region of a reverse-biased diode, the dominant process is:**

(a) Recombination
(b) Generation
(c) Both
(d) Neither

**Answer: (b)**
**Explanation:** Carriers swept out → generation of EHPs dominates → contributes to reverse current.

---

## Q18. Shockley-Read-Hall
**SRH recombination is also called:**

(a) Band-to-band
(b) Trap-assisted
(c) Auger
(d) Radiative

**Answer: (b)**
**Explanation:** SRH recombination occurs via trap levels in the bandgap (trap-assisted).

---

## Q19. Optical Generation
**The optical generation rate must balance which process at steady state?**

(a) Drift
(b) Diffusion
(c) Recombination
(d) Generation

**Answer: (c)**
**Explanation:** At steady state, optical generation rate = recombination rate → G = Δp/τ.

---

## Q20. Diffusion Length from Data
**If Dn = 35 cm²/s and Ln = 10 μm, the electron lifetime is:**

(a) 3.5 ns
(b) 28.6 ns
(c) 286 ns
(d) 2.86 μs

**Answer: (b)**
**Explanation:** τ = L²/D = (10×10⁻⁴)²/35 = 10⁻⁶/35 = 2.86×10⁻⁸ s = 28.6 ns

---

## Q21. Majority Carrier Effect
**In low-level injection in N-type Si:**

(a) Majority carrier concentration changes significantly
(b) Minority concentration increases but majority unchanged
(c) Both change equally
(d) Both unchanged

**Answer: (b)**
**Explanation:** Δp << ND: majority carrier concentration essentially unchanged; minority carriers injected.

---

## Q22. Storage Time
**The storage time in a switch is related to:**

(a) Diffusion length
(b) Recombination lifetime
(c) Mobility
(d) Conductivity

**Answer: (b)**
**Explanation:** Storage time depends on recombination lifetime: ts = τ·ln(1 + IF/IR).

---

## Q23. Delta p at Surface
**For high surface recombination velocity (s → ∞), the boundary condition gives:**

(a) Δp(W) = Δp(0)
(b) Δp(W) ≈ 0
(c) dΔp/dx = 0
(d) Δp(W) = ∞

**Answer: (b)**
**Explanation:** For s → ∞: Δp(W) → 0. Carriers at surface recombine instantly.

---

## Q24. Continuity in Steady State
**In steady state with generation and recombination balanced, Δp is:**

(a) Time-dependent
(b) Constant in time
(c) Always zero
(d) Infinite

**Answer: (b)**
**Explanation:** ∂p/∂t = 0 → steady state. Δp constant in time (may vary in space).

---

## Q25. Time Constant Measurement
**The minority carrier lifetime can be measured from:**

(a) The decay of excess carrier concentration
(b) The rise time only
(c) The AC resistance
(d) The breakdown voltage

**Answer: (a)**
**Explanation:** Measure Δp(t) decay after source removal → extract τ from exponential decay.
