# Op-Amp Basics - Practice Questions

---

### Q1. (Easy) Under negative feedback and linear operation, the ideal op-amp conditions are:
(A) V+ = V- and input currents are zero  (B) V+ = -V- and input currents are equal to output current  (C) V- = 0 always  (D) The output is always saturated

**Answer: (A) V+ approximately equals V- and no current enters either input.**

---

### Q2. (Easy) The virtual-ground condition is valid when:
(A) The op-amp is in a comparator with positive feedback  (B) The non-inverting input is grounded and negative feedback keeps the op-amp linear  (C) The output is at a supply rail  (D) The input bias current is large

**Answer: (B) A virtual ground requires linear operation under negative feedback.**

---

### Q3. (Moderate) An inverting amplifier has Rin = 4 kohm and Rf = 20 kohm. Its ideal voltage gain is:
(A) +5  (B) -5  (C) +6  (D) -0.2

**Answer: (B) A_v = -Rf/Rin = -20/4 = -5.**

---

### Q4. (Moderate) A non-inverting amplifier has R1 = 10 kohm and Rf = 40 kohm. Its ideal voltage gain is:
(A) 3  (B) 4  (C) 5  (D) -5

**Answer: (C) A_v = 1 + Rf/R1 = 1 + 4 = 5.**

---

### Q5. (Moderate) For an inverting op-amp with R1 = 8 kohm and Rf = 24 kohm, the resistor used to compensate input bias current is:
(A) 8 kohm  (B) 24 kohm  (C) 6 kohm  (D) 32 kohm

**Solution:** Rcomp = R1 || Rf = (8 x 24)/(8 + 24) = 6 kohm.
**Answer: (C) 6 kohm**

---

### Q6. (Moderate) An op-amp with GBW = 2 MHz is used at a closed-loop gain of 20. Its approximate bandwidth is:
(A) 100 kHz  (B) 20 kHz  (C) 10 kHz  (D) 2 MHz

**Solution:** BW = GBW/A_v = 2 MHz/20 = 100 kHz.
**Answer: (A) 100 kHz**

---

### Q7. (Moderate) The minimum required slew rate for a 2 V peak, 50 kHz sinusoidal output is approximately:
(A) 0.63 V/us  (B) 6.28 V/us  (C) 0.10 V/us  (D) 2 V/us

**Solution:** SR = 2 pi f Vp = 2 pi x 50,000 x 2 = 628,319 V/s = 0.628 V/us.
**Answer: (A) 0.63 V/us**

---

### Q8. (Moderate) An op-amp with a 0.5 V/us slew rate drives a 1 V peak sine wave. The maximum undistorted frequency is approximately:
(A) 7.96 kHz  (B) 79.6 kHz  (C) 7.96 MHz  (D) 159 kHz

**Solution:** fmax = SR/(2 pi Vp) = 0.5 x 10^6/(2 pi) = 79.6 kHz.
**Answer: (B) 79.6 kHz**

---

### Q9. (Moderate) A CMRR of 100 dB corresponds to a differential-to-common-mode gain ratio of:
(A) 100  (B) 1,000  (C) 10,000  (D) 100,000

**Answer: (D) 10^(100/20) = 100,000.**

---

### Q10. (Moderate) An inverting amplifier has noise gain 101 and an input offset voltage of 2 mV. The output offset due to VOS is approximately:
(A) 2 mV  (B) 202 mV  (C) 20.2 V  (D) 101 mV

**Solution:** Vout = Vos(1 + Rf/R1) = 2 mV x 101 = 202 mV.
**Answer: (B) 202 mV**

---

### Q11. (Moderate) The output of an op-amp saturates at a positive rail. Which assumption is no longer valid?
(A) The output impedance is low  (B) The virtual-short condition  (C) The input impedance is high  (D) The circuit is powered

**Answer: (B) The virtual-short condition requires linear operation.**

---

### Q12. (Moderate) Negative feedback in an op-amp generally:
(A) Reduces bandwidth and increases distortion  (B) Stabilizes gain and lowers output impedance  (C) Eliminates all noise  (D) Makes positive-feedback oscillation more likely

**Answer: (B) Stabilizes gain and lowers output impedance.**
