# Sampling and Reconstruction - Practice Questions

---

### Q1. (Easy) Nyquist rate for max freq fm:
(A) 2 fm  (B) fm  (C) fm/2  (D) 4fm

**Answer: (A) Nyquist rate = 2 fm**

---

### Q2. (Moderate) Aliasing occurs when:
(A) fs < 2 fmax  (B) fs = 2fmax exactly ok  (C) fs high  (D) fs > 3fmax

**Answer: (A) Sampling below Nyquist (fs < 2fmax) -> aliasing**

---

### Q3. (Moderate) Anti-aliasing filter is a:
(A) Low-pass before ADC  (B) High-pass  (C) Band-pass after  (D) None

**Answer: (A) Low-pass pre-sampling filter (limit to fs/2 band)**

---

### Q4. (Moderate) Reconstruction (DAC side) uses:
(A) Low-pass interpolation filter  (B) High-pass  (C) Differentiator  (D) No filter

**Answer: (A) Low-pass to smooth samples back to continuous-time signal**

---

### Q5. (Moderate) Ideal sampler output spectrum:
(A) Repeats X(f) shifted by k*fs  (B) Single copy  (C) Zero  (D) DC only

**Answer: (A) Sampling replicates spectrum at multiples of fs (folded with aliasing if undersampled)**

---

### Q6. (Moderate) fmax=4kHz, minimum fs:
(A) 8 kHz  (B) 4 kHz  (C) 16 kHz  (D) 2 kHz

**Solution:** fs = 2*4k = 8 kHz
**Answer: (A) 8 kHz**

---

### Q7. (Moderate) Sample-and-hold circuit:
(A) Holds input constant during ADC conversion  (B) Amplifies only  (C) Filters  (D) Modulates

**Answer: (A) Holds analog value stable during conversion (reduces aperture error)**

---

### Q8. (Moderate) Oversampling benefit:
(A) Relaxes anti-alias & improves resolution  (B) Aliasing  (C) Slower  (D) More noise

**Answer: (A) Oversampling simplifies anti-aliasing & improves effective SNR**

---

### Q9. (Moderate) Signal sampled at Nyquist, to recover use:
(A) Ideal low-pass fc = fs/2  (B) High-pass  (C) Band-pass wide  (D) None

**Answer: (A) Reconstruction low-pass at fc = fs/2 (bandlimited interpolation)**

---

### Q10. (Moderate) Input bandwidth must be limited to ___ before sampling:
(A) fs/2 or less  (B) 2fs  (C) 4fs  (D) fs

**Answer: (A) Input band-limited to fs/2 (<= Nyquist) before sampling**
