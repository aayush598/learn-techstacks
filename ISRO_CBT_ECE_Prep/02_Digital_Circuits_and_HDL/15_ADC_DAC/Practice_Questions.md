# ADC and DAC - Practice Questions

---

### Q1. (Easy) 8-bit DAC resolution (step) with Vref=5V:
(A) 5V  (B) ~19.5 mV  (C) 0.5V  (D) 1V

**Solution:** Vref/2^8 = 5/256 = 0.01953 V = 19.5 mV
**Answer: (B) ~19.5 mV**

---

### Q2. (Easy) Flash ADC with N bits uses ___ comparators:
(A) N  (B) 2^N-1  (C) 2N  (D) N^2

**Answer: (B) 2^N-1 comparators (fastest)**

---

### Q3. (Moderate) SAR ADC converts in:
(A) 1 clock  (B) N clock cycles  (C) 2N clocks  (D) 1/N

**Answer: (B) N clock cycles (one per bit, binary search)**

---

### Q4. (Moderate) Which DAC uses only 2 resistor values?
(A) Binary-weighted  (B) R-2R ladder  (C) Delta-sigma  (D) PWM

**Answer: (B) R-2R ladder (R and 2R only, better accuracy)**

---

### Q5. (Moderate) Quantization error max:
(A) +/- 0.5 LSB  (B) +1 LSB  (C) -1 LSB  (D) +/- LSB

**Answer: (A) +/- 0.5 LSB**

---

### Q6. (Moderate) SQNR for 12-bit ADC:
(A) 72 dB  (B) 74 dB  (C) 6 dB  (D) 24 dB

**Solution:** SQNR = 6.02*12 + 1.76 = 72.24 + 1.76 = 74 dB
**Answer: (B) ~74 dB**

---

### Q7. (Moderate) Which ADC is slowest but most accurate?
(A) Flash  (B) SAR  (C) Dual-slope  (D) none

**Answer: (C) Dual-slope (integrating) - high accuracy, slow**

---

### Q8. (Moderate) To avoid aliasing, sample at:
(A) fs < fmax  (B) fs >= 2*fmax  (C) fs = fmax  (D) fs = fmax/2

**Answer: (B) fs >= 2*fmax (Nyquist rate)**

---

### Q9. (Moderate) DAC Vout for code D (N-bit, Vref):
(A) Vref*D/2^N  (B) Vref/D  (C) Vref*2^N/D  (D) Vref*(2^N-D)

**Answer: (A) Vout = Vref * D / 2^N**

---

### Q10. (Moderate) Advantage of delta-sigma ADC:
(A) Speed  (B) Very high resolution  (C) Cheap  (D) No reference

**Answer: (B) Very high resolution (oversampling + noise shaping, audio)**
