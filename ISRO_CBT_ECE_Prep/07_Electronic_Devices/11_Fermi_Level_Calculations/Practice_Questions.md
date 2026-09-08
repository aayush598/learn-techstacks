# Fermi Level Calculations - Practice Questions (ISRO Style)

## Q1. Fermi Function Value
**The Fermi-Dirac distribution at E = EF is:**

(a) 1
(b) 0.5
(c) 0
(d) 0.7

**Answer: (b)**
**Explanation:** f(EF) = 1/(1+exp(0)) = 1/2 = 0.5. Always 0.5 at EF regardless of temperature.

---

## Q2. Fermi Level Position N-type
**In N-type silicon with ND = 10¹⁶ cm⁻³ at 300K, EF - Ei is:**

(a) 0.21 eV
(b) 0.35 eV
(c) 0.47 eV
(d) 0.12 eV

**Answer: (b)**
**Explanation:** EF - Ei = kT·ln(ND/ni) = 0.026 × ln(10¹⁶/1.5×10¹⁰) = 0.026 × ln(6.67×10⁵) = 0.026 × 13.41 = 0.349 eV ≈ 0.35 eV

---

## Q3. Electron Concentration
**If EF - Ei = 0.35 eV in silicon at 300K, the electron concentration is:**

(a) 1.5 × 10¹⁰ cm⁻³
(b) 10¹⁶ cm⁻³
(c) 10¹⁵ cm⁻³
(d) 10¹⁷ cm⁻³

**Answer: (b)**
**Explanation:** n = ni·exp((EF-Ei)/kT) = 1.5×10¹⁰ × exp(0.35/0.026) = 1.5×10¹⁰ × exp(13.46) = 1.5×10¹⁰ × 7×10⁵ = 10¹⁶ cm⁻³

---

## Q4. Degenerate Semiconductor
**Silicon with ND = 10¹⁹ cm⁻³ at 300K is:**

(a) Non-degenerate
(b) Degenerate
(c) Intrinsic
(d) Compensated

**Answer: (b)**
**Explanation:** Degenerate if ND > 0.135×Nc = 0.135×2.8×10¹⁹ = 3.8×10¹⁸ cm⁻³. 10¹⁹ > 3.8×10¹⁸ → degenerate.

---

## Q5. Fermi Level P-type
**In P-type silicon with NA = 10¹⁷ cm⁻³ at 300K, Ei - EF is:**

(a) 0.35 eV
(b) 0.41 eV
(c) 0.29 eV
(d) 0.12 eV

**Answer: (b)**
**Explanation:** Ei - EF = kT·ln(NA/ni) = 0.026 × ln(10¹⁷/1.5×10¹⁰) = 0.026 × ln(6.67×10⁶) = 0.026 × 15.7 = 0.408 eV ≈ 0.41 eV

---

## Q6. Mass Action Law
**In a silicon sample at 300K, n = 2 × 10¹⁶ cm⁻³. The hole concentration is:**

(a) 1.5 × 10¹⁰ cm⁻³
(b) 1.1 × 10⁴ cm⁻³
(c) 7.5 × 10³ cm⁻³
(d) 2 × 10¹⁶ cm⁻³

**Answer: (b)**
**Explanation:** p = ni²/n = (1.5×10¹⁰)²/(2×10¹⁶) = 2.25×10²⁰/2×10¹⁶ = 1.125×10⁴ cm⁻³ ≈ 1.1×10⁴

---

## Q7. Fermi Function at kT
**At E = EF + kT, the Fermi function value is:**

(a) 0.5
(b) 0.269
(c) 0.731
(d) 0.1

**Answer: (b)**
**Explanation:** f(E) = 1/(1+exp(1)) = 1/(1+2.718) = 1/3.718 = 0.269

---

## Q8. Boltzmann Approximation
**The Boltzmann approximation is valid when:**

(a) E - EF > 2kT
(b) E - EF < kT
(c) E = EF
(d) E - EF = 0

**Answer: (a)**
**Explanation:** Boltzmann approximation valid when (E-EF) >> kT, typically (E-EF) > 2kT → error < 1%.

---

## Q9. n_i Temperature Dependence
**The intrinsic carrier concentration ni at 300K for Si is 1.5×10¹⁰. At 400K, ni is approximately:**

(a) 3 × 10¹⁰ cm⁻³
(b) 1.5 × 10¹¹ cm⁻³
(c) 4.5 × 10¹² cm⁻³
(d) 10¹³ cm⁻³

**Answer: (c)**
**Explanation:** ni ∝ exp(-Eg/2kT). Using formula with Eg = 1.12 eV: ni(400)/ni(300) ≈ exp[(1.12/2k)(1/300 - 1/400)] ≈ exp(5.4) ≈ 220, × T^1.5 factor. Result ≈ 4.5×10¹² cm⁻³

---

## Q10. Bandgap from Un
**In the equation n = Nc·exp(-(EC-EF)/kT), if n = 10¹⁶ cm⁻³ and Nc = 2.8×10¹⁹ cm⁻³, the value of (EC - EF) is:**

(a) 0.1 eV
(b) 0.2 eV
(c) 0.3 eV
(d) 0.5 eV

**Answer: (b)**
**Explanation:** EC - EF = kT·ln(Nc/n) = 0.026 × ln(2.8×10¹⁹/10¹⁶) = 0.026 × ln(2800) = 0.026 × 7.94 = 0.206 eV ≈ 0.2 eV

---

## Q11. Fermi Level Temperature
**At T = 0K, the Fermi function f(E):**

(a) Is 0.5 at all energies
(b) Is 1 for E < EF and 0 for E > EF
(c) Is a smooth curve
(d) Depends on doping

**Answer: (b)**
**Explanation:** At T=0K: f(E) = 1 for E < EF (all filled), f(E) = 0 for E > EF (all empty). Sharp step.

---

## Q12. Carrier Type Determination
**If EF is 0.2 eV above Ei in silicon at 300K, the semiconductor is:**

(a) N-type
(b) P-type
(c) Intrinsic
(d) Compensated

**Answer: (a)**
**Explanation:** EF > Ei → N-type. n = ni·exp(0.2/0.026) = ni × 2200 ≈ 3.3×10¹³ cm⁻³

---

## Q13. Effective Density of States
**The effective density of states Nc at 300K for Si is:**

(a) 1.04 × 10¹⁹ cm⁻³
(b) 2.8 × 10¹⁹ cm⁻³
(c) 1.5 × 10¹⁰ cm⁻³
(d) 10¹⁶ cm⁻³

**Answer: (b)**
**Explanation:** Nc = 2.8 × 10¹⁹ cm⁻³ at 300K for Si. Nv = 1.04 × 10¹⁹ cm⁻³.

---

## Q14. Fermi Integral
**For a degenerate semiconductor, carrier concentration is calculated using:**

(a) Boltzmann approximation
(b) Fermi integral
(c) Mass action law only
(d) Einstein relation

**Answer: (b)**
**Explanation:** Degenerate: EF in band → Fermi statistics needed → F_{1/2} Fermi integral.

---

## Q15. Intrinsic Fermi Level
**The intrinsic Fermi level Ei in Si at 300K is:**

(a) Exactly at midgap
(b) Slightly above midgap
(c) Slightly below midgap
(d) At conduction band

**Answer: (b)**
**Explanation:** Ei = (EC+EV)/2 + (3/4)kT·ln(mp*/mn*). Since mn* > mp* for Si, Ei is slightly above midgap.

---

## Q16. Charge Neutrality
**The charge neutrality condition in a semiconductor is:**

(a) n = p
(b) n + NA = p + ND
(c) n + ND = p + NA
(d) n = ni

**Answer: (b)**
**Explanation:** Charge neutrality: n + NA⁻ = p + ND⁺. For complete ionization: n + NA = p + ND.

---

## Q17. Fermi Level in Intrinsic
**At 300K, the Fermi level in intrinsic silicon is approximately:**

(a) 0.55 eV below EC
(b) 0.56 eV above EC
(c) At EC
(d) At EV

**Answer: (a)**
**Explanation:** Ei ≈ EC - Eg/2 = EC - 0.56 eV (midgap). Slightly lower due to mass ratio.

---

## Q18. Compensated Doping
**Si has ND = 5×10¹⁶ and NA = 2×10¹⁶ cm⁻³. The effective Fermi level (EF - Ei) is:**

(a) 0.29 eV
(b) 0.38 eV
(c) 0.41 eV
(d) 0.35 eV

**Answer: (b)**
**Explanation:** Net doping = 3×10¹⁶. EF - Ei = 0.026 × ln(3×10¹⁶/1.5×10¹⁰) = 0.026 × ln(2×10⁶) = 0.026 × 14.5 = 0.377 eV ≈ 0.38 eV

---

## Q19. Degeneracy Threshold
**Beyond which doping concentration does Si become degenerate at 300K?**

(a) 10¹⁷ cm⁻³
(b) 3.8 × 10¹⁸ cm⁻³
(c) 10¹⁶ cm⁻³
(d) 10¹⁵ cm⁻³

**Answer: (b)**
**Explanation:** Degenerate when ND > 0.135×Nc = 0.135 × 2.8×10¹⁹ ≈ 3.8 × 10¹⁸ cm⁻³

---

## Q20. EF and Carrier Type
**If EF is below EV (in valence band), the semiconductor is:**

(a) N-type
(b) P-type (degenerate)
(c) Intrinsic
(d) Impossible

**Answer: (b)**
**Explanation:** EF below EV → heavily doped P-type → degenerate (holes fill valence band states).

---

## Q21. Carrier Ratio
**The ratio of electron to hole concentration in N-type with ND = 10¹⁶ is:**

(a) 10¹⁶
(b) 6.7 × 10¹¹
(c) 10⁴
(d) 2.25 × 10⁶

**Answer: (b)**
**Explanation:** n/p = ND/(ni²/ND) = ND²/ni² = (10¹⁶)²/(1.5×10¹⁰)² = 10³²/2.25×10²⁰ = 4.4×10¹¹ ≈ 6.7×10¹¹

---

## Q22. Temperature Effect on EF
**In the extrinsic range (room T), increasing temperature of N-type Si:**

(a) Moves EF toward EC
(b) Moves EF toward midgap
(c) No effect on EF
(d) Moves EF into VC

**Answer: (b)**
**Explanation:** As T increases, ni increases → semiconductor approaches intrinsic → EF moves toward Ei (midgap).

---

## Q23. Fermi Function at 3kT
**At E = EF + 3kT, the Fermi function is approximately:**

(a) 0.5
(b) 0.047
(c) 0.27
(d) 0.01

**Answer: (b)**
**Explanation:** f = 1/(1+exp(3)) = 1/(1+20.1) = 1/21.1 = 0.047

---

## Q24. Minority Carrier
**The minority carrier concentration in N-type Si with ND = 10¹⁶ is:**

(a) 2.25 × 10⁴ cm⁻³
(b) 1.5 × 10¹⁰ cm⁻³
(c) 10¹⁶ cm⁻³
(d) 6.7 × 10⁵ cm⁻³

**Answer: (a)**
**Explanation:** p = ni²/ND = (1.5×10¹⁰)²/10¹⁶ = 2.25×10²⁰/10¹⁶ = 2.25 × 10⁴ cm⁻³

---

## Q25. Bandgap from Intrinsic Density
**Given ni = 1.5×10¹⁰ cm⁻³, NcNv = 2.9×10³⁸ cm⁻⁶ at 300K, the bandgap of Si is:**

(a) 1.0 eV
(b) 1.12 eV
(c) 1.43 eV
(d) 0.67 eV

**Answer: (b)**
**Explanation:** ni² = NcNv·exp(-Eg/kT) → exp(-Eg/0.052) = (1.5×10¹⁰)²/(2.9×10³⁸) = 2.25×10²⁰/2.9×10³⁸ = 7.76×10⁻¹⁹ → ln = -41.7 → Eg = 0.052 × 41.7/2 → Eg/(2kT) = 21.7 → Eg = 1.13 eV ≈ 1.12 eV
