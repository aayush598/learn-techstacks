# PWM Techniques - Practice Questions

## Multiple Choice Questions

### Q1. In SPWM, the modulation index ma = 0.7 means output fundamental is:
(a) 70% of input voltage
(b) 70% of maximum possible
(c) 30% of input voltage
(d) 70% of carrier amplitude

**Answer: (a)**
Vo1(peak) = ma × Vin (full-bridge). At ma = 0.7: Vo1 = 0.7Vin.

---

### Q2. Unipolar PWM has first harmonics at:
(a) fsw
(b) 2fsw
(c) fsw/2
(d) 3fsw

**Answer: (b)**
Unipolar switching doubles effective frequency, pushing first harmonics to 2fsw.

---

### Q3. SHE technique with 5 switching angles can eliminate:
(a) 4 harmonics
(b) 5 harmonics
(c) 3 harmonics
(d) 6 harmonics

**Answer: (a)**
N angles eliminate N-1 harmonics. 5 angles eliminate 4 harmonics (5th, 7th, 11th, 13th).

---

### Q4. SVM provides __________ improvement in DC bus utilization over SPWM:
(a) 15.5%
(b) 50%
(c) 100%
(d) 25%

**Answer: (a)**
SVM: 100% vs SPWM: 78.5%. Improvement = (100-78.5)/78.5 = 27.4%? 

Actually: SVM Vo1(max) = Vin/√3, SPWM Vo1(max) = Vin/2
Ratio = (Vin/√3)/(Vin/2) = 2/√3 = 1.155 → 15.5% improvement

---

### Q5. Bipolar PWM compared to unipolar PWM has:
(a) Lower THD
(b) Higher THD
(c) Same THD
(d) Zero THD

**Answer: (b)**
Bipolar has first harmonics at fsw, unipolar at 2fsw. Higher fsw → lower THD for unipolar.

---

### Q6. The frequency modulation ratio mf = fsw/f1 in SPWM typically ranges from:
(a) 1-5
(b) 15-25
(c) 100-200
(d) 500-1000

**Answer: (b)**
mf = 15-25 is typical for motor drives. Higher mf gives better harmonics but more switching losses.

---

### Q7. In SVM, the reference vector rotates in:
(a) Real-imaginary plane
(b) α-β (stationary) plane
(c) d-q (rotating) plane
(d) r-θ (polar) plane

**Answer: (b)**
SVM operates in stationary α-β frame, representing three-phase quantities as space vectors.

---

### Q8. SHE with N = 3 angles eliminates which harmonics?
(a) 3rd, 5th
(b) 5th, 7th
(c) 7th, 9th
(d) 3rd, 7th

**Answer: (b)**
3 angles eliminate 2 harmonics: 5th and 7th (lowest uneliminated is 11th).

---

### Q9. Overmodulation in SPWM results in:
(a) Lower output voltage
(b) Higher harmonics and output approaching square wave
(c) Constant output
(d) Reduced switching losses only

**Answer: (b)**
ma > 1 pushes toward square wave, increasing fundamental but adding harmonics.

---

### Q10. The main advantage of SVM over SPWM is:
(a) Simpler implementation
(b) 15% higher DC bus utilization
(c) Lower component count
(d) Lower switching frequency

**Answer: (b)**
SVM provides 100% DC utilization vs SPWM's 78.5%, giving higher output from same DC bus.

---

### Q11. For motor drives, the minimum switching frequency is limited by:
(a) Motor inductance
(b) Audible noise (above 20 kHz)
(c) Maximum motor speed
(d) DC bus voltage

**Answer: (b)**
Switching above 20 kHz eliminates audible noise. Below this, motor noise can be objectionable.

---

### Q12. The THD of a six-step inverter output is approximately:
(a) 5%
(b) 31%
(c) 48%
(d) 10%

**Answer: (b)**
Six-step three-phase line voltage THD = 31.1%. Much higher than PWM techniques.

---

### Q13. In SPWM, increasing mf (carrier frequency) while keeping f1 constant:
(a) Increases THD
(b) Decreases THD
(c) No effect on THD
(d) Changes output voltage

**Answer: (b)**
Higher mf pushes harmonics to higher frequencies, easier to filter, lower THD.

---

### Q14. SHE technique requires:
(a) Real-time computation
(b) Pre-calculated look-up table
(c) Analog comparator
(d) No computation

**Answer: (b)**
SHE angles are computed offline and stored. Real-time only requires look-up and comparison.

---

### Q15. The zero vectors in SVM are used to:
(a) Increase output voltage
(b) Fill remaining switching time
(c) Reduce switching losses
(d) Both (b) and (c)

**Answer: (d)**
Zero vectors (all upper or all lower ON) provide freewheeling and reduce switching transitions.

---

### Q16. For high-power applications, SHE is preferred because:
(a) Highest THD
(b) Lowest switching frequency
(c) Simplest control
(d) Highest DC utilization

**Answer: (b)**
SHE uses few switchings (N angles), reducing switching losses at high power.

---

### Q17. The carrier signal in SPWM is typically:
(a) Sine wave
(b) Square wave
(c) Triangle/sawtooth wave
(d) Exponential wave

**Answer: (c)**
Triangle or sawtooth carrier compared with sine reference generates PWM pulses.

---

### Q18. SVM eliminates which type of harmonics naturally?
(a) Even harmonics
(b) Triplen harmonics
(c) All harmonics
(d) No harmonics

**Answer: (b)**
Three-phase SVM naturally eliminates triplen harmonics (3rd, 9th, 15th...).

---

### Q19. The output filter for PWM inverter should have cutoff:
(a) Below f1
(b) Between f1 and fsw
(c) Above fsw
(d) At f1

**Answer: (b)**
Filter passes f1 (low) and blocks fsw harmonics (high).

---

### Q20. SPWM at ma = 1 gives output fundamental of:
(a) Vin (full-bridge)
(b) Vin/2 (half-bridge)
(c) Both (a) and (b)
(d) 0

**Answer: (c)**
Full-bridge: Vo1 = ma × Vin = Vin
Half-bridge: Vo1 = ma × Vin/2 = Vin/2

---

## Numerical Problems

### N1. SPWM inverter has Vin = 400V, ma = 0.85, full-bridge. Find fundamental output RMS.
**Solution:**
Vo1(peak) = ma × Vin = 0.85 × 400 = 340V
Vo1(rms) = 340/√2 = 240.4V

---

### N2. SHE with 5 angles at M = 0.9. Find approximate fundamental voltage if Vin = 300V.
**Solution:**
Vo1(peak) = (4/π) × Vin × M/2 = (4/π) × 300 × 0.45 = 171.9V
More accurately: Vo1(peak) = ma × Vin = 0.9 × 300 = 270V

---

### N3. SVM has |Vref| = 150V, Vin = 400V, Ts = 100 μs, θ = 30°. Find T1 and T2.
**Solution:**
T1 = (√3 × Ts × |Vref|/Vin) × sin(60° - 30°) = (1.732 × 100×10⁻⁶ × 150/400) × sin 30°
= (1.732 × 100×10⁻⁶ × 0.375) × 0.5 = 64.95 × 10⁻⁶ × 0.5 = 32.5 μs

T2 = (√3 × Ts × |Vref|/Vin) × sin(30°) = 64.95 × 10⁻⁶ × 0.5 = 32.5 μs

T0 = Ts - T1 - T2 = 100 - 32.5 - 32.5 = 35 μs

---

### N4. SPWM has f1 = 50 Hz, mf = 21. Find switching frequency.
**Solution:**
fsw = mf × f1 = 21 × 50 = 1050 Hz = 1.05 kHz

---

### N5. Compare THD: SPWM (4%), Unipolar (2.5%), SVM (2%), SHE (1%). Which is best for motor drive?
**Solution:**
All acceptable for motor drives (<5%). SVM best balance of THD and implementation ease. SHE best THD but complex. For industrial drives: SVM preferred.

---

## Assertion-Reason Type

### AR1. Assertion: SVM provides higher output voltage than SPWM for same DC bus.
### Reason: SVM achieves 100% DC bus utilization vs SPWM's 78.5%.

**Answer: Both true, R is correct explanation.**
SVM exploits full DC bus: Vo1(max) = Vin/√3 vs SPWM's Vin/2.

---

### AR2. Assertion: SHE has lowest switching losses among PWM techniques.
### Reason: SHE uses pre-calculated angles with minimal switchings.

**Answer: Both true, R is correct explanation.**
SHE uses N angles for N-1 harmonic elimination, far fewer switchings than SPWM/SVM.

---

## True/False

1. **T/F: Bipolar PWM has better harmonic performance than unipolar.**
**Answer: False.** Unipolar has first harmonics at 2fsw vs bipolar's fsw, giving lower THD.

2. **T/F: SPWM at ma > 1 still gives linear voltage control.**
**Answer: False.** ma > 1 is overmodulation, entering non-linear region.

3. **T/F: SVM eliminates triplen harmonics naturally.**
**Answer: True.** Three-phase SVM output has no triplen harmonics.

---

## Fill in the Blanks

1. The ratio of carrier frequency to reference frequency is called __________.
**Answer: frequency modulation ratio (mf)**

2. __________ PWM technique provides 15% higher DC bus utilization than SPWM.
**Answer: Space vector (SVM)**

3. SHE with N switching angles eliminates __________ harmonics.
**Answer: N-1**

4. Unipolar switching has first harmonics at __________.
**Answer: 2fsw (twice switching frequency)**

5. The __________ of an inverter measures how close the output is to a pure sine wave.
**Answer: THD (Total Harmonic Distortion)**
