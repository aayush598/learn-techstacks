# Bandgap Reference - Practice Questions (ISRO Style)

## Q1. Bandgap Temperature Coefficient
**The temperature coefficient of silicon bandgap energy at 300K is approximately:**

(a) +0.27 meV/K
(b) -0.27 meV/K
(c) -2 mV/K
(d) +2 mV/K

**Answer: (b)**
**Explanation:** dEg/dT ≈ -0.27 meV/K for Si. Bandgap decreases with temperature.

---

## Q2. VBE Temperature Coefficient
**The base-emitter voltage of a BJT has a temperature coefficient of approximately:**

(a) +2 mV/°C
(b) -2 mV/°C
(c) +0.086 mV/°C
(d) -0.086 mV/°C

**Answer: (b)**
**Explanation:** dVBE/dT ≈ -2 mV/°C. VBE has negative temperature coefficient.

---

## Q3. Bandgap Reference Voltage
**The output voltage of a standard bandgap reference is approximately:**

(a) 0.7V
(b) 1.2V
(c) 2.5V
(d) 5.0V

**Answer: (b)**
**Explanation:** VREF = VBE + K×VT ≈ 0.6 + 23×0.026 ≈ 1.2V. Related to Si bandgap extrapolated to 0K.

---

## Q4. K Value
**To cancel VBE temperature dependence in a bandgap reference, the value of K (multiplier of VT) is approximately:**

(a) 2
(b) 10
(c) 23
(d) 100

**Answer: (c)**
**Explanation:** K = |dVBE/dT|/(dV_T/dT) = 2/(0.086) ≈ 23.

---

## Q5. PTAT Current
**A bandgap reference uses two BJTs with current density ratio 10:1 at 300K. The ΔVBE is:**

(a) 26 mV
(b) 52 mV
(c) 60 mV
(d) 120 mV

**Answer: (c)**
**Explanation:** ΔVBE = VT·ln(10) = 25.85 × 2.303 = 59.5 mV ≈ 60 mV

---

## Q6. VT Coefficient
**The temperature coefficient of thermal voltage VT is:**

(a) -2 mV/K
(b) +0.086 mV/K
(c) +2 mV/K
(d) -0.086 mV/K

**Answer: (b)**
**Explanation:** dVT/dT = k/q = 86 μV/K = 0.086 mV/K (positive TC).

---

## Q7. VBE at Temperature
**A BJT has VBE = 0.7V at 300K. At 350K, VBE is approximately:**

(a) 0.6 V
(b) 0.7 V
(c) 0.8 V
(d) 0.75 V

**Answer: (a)**
**Explanation:** ΔVBE = -2 mV/K × 50K = -100 mV. VBE(350) = 0.7 - 0.1 = 0.6V

---

## Q8. Bandgap Formula
**The Varshni equation for bandgap vs temperature is:**

(a) Eg(T) = Eg(0) + αT²/(T+β)
(b) Eg(T) = Eg(0) - αT²/(T+β)
(c) Eg(T) = Eg(0) - αT
(d) Eg(T) = Eg(0) + αT

**Answer: (b)**
**Explanation:** Varshni: Eg(T) = Eg(0) - αT²/(T+β). Bandgap decreases with temperature.

---

## Q9. PTAT Concept
**PTAT refers to:**

(a) Power To Ampere Transfer
(b) Proportional To Absolute Temperature
(c) Positive Temperature Avalanche Threshold
(d) Power Transistor Analysis Test

**Answer: (b)**
**Explanation:** PTAT = Proportional To Absolute Temperature. Current/voltage proportional to T.

---

## Q10. Bandgap from Wavelength
**A semiconductor emits at 600 nm. Its bandgap is approximately:**

(a) 1.0 eV
(b) 1.5 eV
(c) 2.07 eV
(d) 3.0 eV

**Answer: (c)**
**Explanation:** Eg = 1240/λ = 1240/600 = 2.07 eV

---

## Q11. Temperature Compensated Zener
**A 5.6V Zener has near-zero temperature coefficient because:**

(a) Only Zener breakdown
(b) Zener and avalanche mechanisms balance
(c) High doping
(d) Low current

**Answer: (b)**
**Explanation:** At ~5.6V, Zener (negative TC) and avalanche (positive TC) balance → TC ≈ 0.

---

## Q12. dVBE/dT Derivation
**The VBE temperature coefficient is negative because:**

(a) VBE decreases with current
(b) Is increases with temperature
(c) VT increases with temperature
(d) Bandgap increases with temperature

**Answer: (b)**
**Explanation:** Is increases exponentially with T → VBE must decrease to maintain constant IC.

---

## Q13. Bandgap Reference Principle
**A bandgap reference works by:**

(a) Using a single Zener diode
(b) Summing VBE (negative TC) with K×VT (positive TC)
(c) Using only PTAT current
(d) Using temperature sensors

**Answer: (b)**
**Explanation:** VREF = VBE + K×VT, combining negative and positive TC components to cancel temperature dependence.

---

## Q14. Reference Accuracy
**The typical accuracy of a precision bandgap reference is:**

(a) ±10%
(b) ±1%
(c) ±0.01%
(d) ±0.001%

**Answer: (c)**
**Explanation:** Precision bandgap references have accuracy ~0.01% (100 ppm) with tuning.

---

## Q15. VT at Different Temperatures
**At T=400K, the thermal voltage VT is:**

(a) 26 mV
(b) 34.5 mV
(c) 40 mV
(d) 43 mV

**Answer: (b)**
**Explanation:** VT = kT/q = 8.617×10⁻⁵ × 400 = 34.5 mV

---

## Q16. Brokaw Reference
**In a Brokaw bandgap reference, the reference voltage is:**

(a) VBE only
(b) VBE + PTAT voltage
(c) PTAT voltage only
(d) Zener voltage

**Answer: (b)**
**Explanation:** VREF = VBE1 + 2×(R2/R1)×VT×ln(N). VBE has negative TC, PTAT has positive TC.

---

## Q17. Curvature
**The curvature in bandgap reference output is due to:**

(a) Linear VBE terms
(b) Non-linear ln(T) terms in VBE
(c) Resistor temperature coefficient
(d) Op-amp offset

**Answer: (b)**
**Explanation:** VBE has (n-1)VT·ln(T/T0) term → non-linear → curvature in reference output.

---

## Q18. Bandgap vs Temperature
**The product hc related to bandgap is:**

(a) hc = E/λ
(b) hc = E×λ
(c) hc = E/λ²
(d) hc = E×λ²

**Answer: (b)**
**Explanation:** E = hc/λ → hc = E×λ = 1240 eV·nm

---

## Q19. Reference Temperature Drift
**A bandgap reference has drift of 10 ppm/°C. Over 50°C range, the total drift is:**

(a) 0.01%
(b) 0.05%
(c) 0.1%
(d) 0.5%

**Answer: (b)**
**Explanation:** Drift = 10 ppm/°C × 50°C = 500 ppm = 0.05%

---

## Q20. Is Temperature Dependence
**The reverse saturation current Is of a BJT varies with temperature as:**

(a) Is ∝ T
(b) Is ∝ T³
(c) Is ∝ T³·exp(-Eg/kT)
(d) Is ∝ exp(-Eg/kT)

**Answer: (c)**
**Explanation:** Is ∝ T³·exp(-Eg/kT). Strong temperature dependence drives VBE negative TC.

---

## Q21. Bandgap from ni
**At 300K, if ni = 1.5×10¹⁰ cm⁻³ for Si, the bandgap can be found from:**

(a) ni = √NcNv·exp(-Eg/2kT)
(b) ni = NcNv·exp(-Eg/kT)
(c) ni = √(NcNv)·exp(-Eg/kT)
(d) ni = Nc·exp(-Eg/2kT)

**Answer: (a)**
**Explanation:** ni = √(NcNv)·exp(-Eg/2kT). Bandgap can be extracted from ni measurements.

---

## Q22. Temperature Reference Need
**Accurate voltage references are needed in:**

(a) ADCs and DACs
(b) Amplifiers
(c) Power supplies
(d) All of the above

**Answer: (d)**
**Explanation:** References required in data converters, regulators, comparators, instrumentation.

---

## Q23. VG0 Value
**The value of VG0 (bandgap voltage extrapolated to 0K) for Si is approximately:**

(a) 0.7V
(b) 1.2V
(c) 1.5V
(d) 2.0V

**Answer: (b)**
**Explanation:** VG0 ≈ 1.21V for Si. This is why bandgap references produce ~1.2V.

---

## Q24. Two BJT Rule
**If the emitter area ratio of two BJTs in a bandgap is N, the ΔVBE is:**

(a) VT·N
(b) VT·ln(N)
(c) N·VT
(d) VT/N

**Answer: (b)**
**Explanation:** ΔVBE = VT·ln(N). Area ratio creates current density ratio N.

---

## Q25. Reference Temperature Dependence
**After proper trimming, a good bandgap reference has temperature coefficient of:**

(a) 1000 ppm/°C
(b) 100 ppm/°C
(c) 1 ppm/°C
(d) 10000 ppm/°C

**Answer: (c)**
**Explanation:** Precision curvature-compensated bandgap references can achieve TC ≈ 1-5 ppm/°C.
