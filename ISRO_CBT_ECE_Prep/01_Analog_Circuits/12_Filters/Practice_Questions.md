# Analog Filters - Practice Questions

---

### Q1. (Easy) First-order active LPF cutoff with R=10k, C=10nF:
(A) 159 Hz  (B) 1.59 kHz  (C) 15.9 kHz  (D) 159 kHz

**Solution:** fc = 1/(2pi*10k*10n) = 1/(6.28e-4) = 1592 Hz
**Answer: (B) 1.59 kHz**

---

### Q2. (Easy) Butterworth filter characteristic:
(A) Ripple in passband  (B) Maximally flat  (C) Ripple in stopband  (D) Linear phase

**Answer: (B) Maximally flat (no ripple, monotonic)**

---

### Q3. (Moderate) Rolloff of 2nd-order filter:
(A) -20 dB/dec  (B) -40 dB/dec  (C) -6 dB/dec  (D) -60 dB/dec

**Answer: (B) -40 dB/decade**

---

### Q4. (Moderate) Chebyshev I filter has:
(A) Flat passband  (B) Ripple in passband  (C) No rolloff  (D) No cutoff

**Answer: (B) Ripple in passband (sharper cutoff)**

---

### Q5. (Moderate) Which can amplify?
(A) Passive RC filter  (B) Active filter (op-amp)  (C) Both  (D) Neither

**Answer: (B) Active filter (has gain)**

---

### Q6. (Moderate) Anti-aliasing filter is typically:
(A) Low-pass before ADC  (B) High-pass  (C) Band-pass  (D) None

**Answer: (A) Low-pass before ADC (limit bandwidth, avoid foldover)**

---

### Q7. (Moderate) For equal R,C in Sallen-Key, fc=1/(2piRC). With R=1k C=0.1uF:
(A) 1.59 kHz  (B) 15.9 kHz  (C) 159 kHz  (D) 159 Hz

**Solution:** 1/(2pi*1e3*0.1e-6) = 1/(6.28e-4) = 1592 Hz
**Answer: (A) 1.59 kHz**

---

### Q8. (Moderate) Higher filter order gives:
(A) Less rolloff  (B) Steeper rolloff  (C) More ripple only  (D) Less delay

**Answer: (B) Steeper rolloff (20n dB/dec)**
