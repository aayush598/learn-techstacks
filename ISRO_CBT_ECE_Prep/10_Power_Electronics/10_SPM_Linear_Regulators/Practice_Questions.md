# SMPS and Linear Regulators - Practice Questions

## Multiple Choice Questions

### Q1. A 7805 regulator has Vin = 9V, Io = 500mA. The power dissipation is:
(a) 2W
(b) 4.5W
(c) 2.5W
(d) 1W

**Answer: (a)**
Pd = (Vin - Vo) × Io = (9-5) × 0.5 = 2W

---

### Q2. The efficiency of a linear regulator with Vin = 12V, Vo = 5V is:
(a) 41.7%
(b) 58.3%
(c) 100%
(d) 80%

**Answer: (a)**
η = Vo/Vin = 5/12 = 0.417 = 41.7%

---

### Q3. LDO stands for:
(a) Low Drop-Out
(b) Linear Drop-Out
(c) Low Dissipation Output
(d) Linear DC Output

**Answer: (a)**
LDO = Low Dropout, meaning very small voltage difference between input and output.

---

### Q4. A flyback converter is best suited for power levels up to:
(a) 10W
(b) 50W
(c) 150W
(d) 500W

**Answer: (c)**
Flyback is commonly used for up to 150W. Beyond this, forward converters are preferred.

---

### Q5. The dropout voltage of 78xx regulators is typically:
(a) 0.3V
(b) 2V
(c) 5V
(d) 10V

**Answer: (b)**
78xx regulators require about 2V headroom (Vin - Vo ≥ 2V) for proper regulation.

---

### Q6. PSRR of 60 dB means the output ripple is:
(a) 1/1000 of input ripple
(b) 1/100 of input ripple
(c) 1/10 of input ripple
(d) Same as input ripple

**Answer: (b)**
PSRR = 20 log(ΔVin/ΔVo) → 60 = 20 log(x) → x = 1000? 

Let me recalculate: 60/20 = 3, so 10³ = 1000.
Output ripple = input ripple / 1000

Answer should be (a) 1/1000.

---

### Q7. In a forward converter, the reset winding is used to:
(a) Increase output voltage
(b) Reset transformer core flux to zero
(c) Provide feedback
(d) Limit current

**Answer: (b)**
Reset winding provides path for magnetizing current to reset core flux during OFF time.

---

### Q8. The main disadvantage of linear regulators is:
(a) High output noise
(b) Poor efficiency for large Vin-Vo difference
(c) Complex circuit
(d) Cannot regulate voltage

**Answer: (b)**
Efficiency = Vo/Vin, which becomes very poor for large voltage drops.

---

### Q9. A switching regulator typically achieves efficiency of:
(a) 30-50%
(b) 50-70%
(c) 85-95%
(d) 99-100%

**Answer: (c)**
Switching regulators achieve 85-95% efficiency due to low-loss switching operation.

---

### Q10. The 7812 regulator outputs:
(a) +5V
(b) +8V
(c) +12V
(d) +15V

**Answer: (c)**
78xx: last two digits indicate output voltage. 7812 = +12V.

---

### Q11. For a flyback converter, the voltage stress on the primary switch is:
(a) Vin
(b) Vin + Vo × (N1/N2)
(c) 2Vin
(d) Vo

**Answer: (b)**
Reflected voltage adds to input: VDS(max) = Vin + Vo × (N1/N2).

---

### Q12. The quiescent current of a typical LDO is:
(a) 1-10 μA
(b) 1-10 mA
(c) 100 mA
(d) 1A

**Answer: (a)**
LDOs have very low quiescent current (1-100 μA), important for battery applications.

---

### Q13. To improve ripple rejection, add:
(a) Larger output resistor
(b) Input capacitor at regulator
(c) Series inductor only
(d) Parallel resistor

**Answer: (b)**
Input capacitor reduces source impedance and ripple at regulator input.

---

### Q14. A 7805 with heat sink has Rth(j-a) = 10°C/W. Max power dissipation for Ta = 50°C:
(a) 10W
(b) 7.5W
(c) 15W
(d) 5W

**Answer: (a)**
Pd(max) = (Tj(max) - Ta) / Rth(j-a) = (150 - 50) / 10 = 10W

---

### Q15. SMPS output noise is primarily due to:
(a) Thermal noise
(b) Switching transitions
(c) 1/f noise
(d) Shot noise

**Answer: (b)**
Switching transitions create high-frequency noise that appears at output.

---

### Q16. LM317 output voltage is set by:
(a) Internal fixed reference only
(b) External resistor divider
(c) Input voltage
(d) Load current

**Answer: (b)**
Vo = 1.25 × (1 + R2/R1), adjustable via external resistors.

---

### Q17. Half-bridge converter switches have voltage stress of:
(a) Vin
(b) 2Vin
(c) Vin/2
(d) 3Vin

**Answer: (a)**
Half-bridge switches see full Vin (not 2Vin like push-pull).

---

### Q18. For battery-powered applications, LDO is preferred over standard linear regulator because:
(a) Lower cost
(b) Lower dropout allows operation near battery end-of-life
(c) Higher efficiency always
(d) Lower noise always

**Answer: (b)**
LDO's 0.1-0.5V dropout vs 2V for 78xx means more usable battery voltage range.

---

### Q19. ESR of output capacitor affects:
(a) Only efficiency
(b) Output ripple and control loop stability
(c) Only input current
(d) Only voltage regulation

**Answer: (b)**
ESR contributes to output ripple and affects control loop compensation/stability.

---

### Q20. The primary purpose of input EMI filter in SMPS is to:
(a) Increase efficiency
(b) Meet conducted emissions standards
(c) Increase output voltage
(d) Reduce component count

**Answer: (b)**
EMI filter prevents switching noise from conducted back to power line.

---

## Numerical Problems

### N1. A 7805 has Vin = 8V, Io = 300mA. Find power dissipation and efficiency.
**Solution:**
Pd = (8-5) × 0.3 = 0.9W
η = 5/8 = 62.5%

---

### N2. Flyback converter: Vin = 48V, N1/N2 = 4, D = 0.4. Find Vo.
**Solution:**
Vo = Vin × (N2/N1) × D/(1-D) = 48 × (1/4) × 0.4/0.6 = 48 × 0.25 × 0.667 = 8V

---

### N3. LDO with Vin = 3.3V, Vo = 3.0V, Io = 100mA. Find efficiency and dropout margin.
**Solution:**
η = 3.0/3.3 = 90.9%
Dropout margin = Vin - Vo = 0.3V (just meets typical LDO dropout spec)

---

### N4. 7812 with Rth(j-a) = 15°C/W, Ta = 40°C. Find maximum load current if Vin = 15V.
**Solution:**
Pd(max) = (150-40)/15 = 7.33W
Io(max) = Pd(max)/(Vin-Vo) = 7.33/(15-12) = 2.44A
With heatsink, can handle reasonable current.

---

### N5. PSRR = 70 dB at 120 Hz. If input ripple is 200 mV, find output ripple.
**Solution:**
70 = 20 log(ΔVin/ΔVo)
3.5 = log(ΔVin/ΔVo)
ΔVin/ΔVo = 10^3.5 = 3162
ΔVo = 200/3162 = 63.3 mV

Wait: ΔVo = ΔVin / 3162 = 200×10⁻³/3162 = 63.3 μV

---

## Assertion-Reason Type

### AR1. Assertion: Linear regulators are preferred for noise-sensitive circuits.
### Reason: Linear regulators have no switching noise and very low output ripple.

**Answer: Both true, R is correct explanation.**
Linear regulators (especially LDOs) provide very clean output without switching artifacts.

---

### AR2. Assertion: SMPS efficiency remains high across load range.
### Reason: Switching losses are proportional to load current.

**Answer: First true, R not exactly correct.**
SMPS efficiency does drop at light loads because fixed losses (gate drive, core) become significant relative to output power.

---

## True/False

1. **T/F: 7805 can output 5V with Vin = 5.5V.**
**Answer: False.** 7805 needs Vin ≥ Vo + 2V = 7V minimum.

2. **T/F: Flyback converter provides galvanic isolation.**
**Answer: True.** Coupled inductor separates input and output.

3. **T/F: LDO always has better efficiency than standard linear regulator.**
**Answer: False.** Same efficiency η = Vo/Vin; LDO just needs less headroom.

---

## Fill in the Blanks

1. A __________ regulator provides fixed output voltage with minimal external components.
**Answer: linear (or 78xx)**

2. The __________ of an SMPS measures output voltage variation with load change.
**Answer: load regulation**

3. LDO's main advantage over standard linear regulator is lower __________ voltage.
**Answer: dropout**

4. __________ converter is most common topology for low-power isolated supplies.
**Answer: Flyback**

5. PSRR measures a regulator's ability to reject __________ from input to output.
**Answer: input ripple (or power supply noise)**
