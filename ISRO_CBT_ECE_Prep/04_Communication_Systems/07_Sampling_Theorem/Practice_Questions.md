# Sampling Theorem - Practice Questions

---

### Q1. (Easy) Nyquist rate for band-limited signal with max freq fm:
(A) fs = 2 fm  (B) fs = fm  (C) fs = fm/2  (D) fs = 4fm

**Answer: (A) Nyquist rate = 2fm (sampling)**

---

### Q2. (Moderate) Sampling below Nyquist causes:
(A) Aliasing (foldover)  (B) Amplification  (C) Filtering  (D) Phasing

**Answer: (A) Aliasing - high frequencies fold into lower; distortion**

---

### Q3. (Moderate) To avoid aliasing, use:
(A) Low-pass anti-aliasing filter before sampler  (B) High-pass  (C) No filter  (D) Only after

**Answer: (A) Anti-aliasing low-pass filter (limit bandwidth to < fs/2)**

---

### Q4. (Moderate) Reconstruction of signal from samples uses:
(A) Low-pass filter  (B) High-pass  (C) Band-pass  (D) Differentiator

**Answer: (A) Low-pass interpolation filter**

---

### Q5. (Moderate) Signal max freq 5 kHz, min sampling rate:
(A) 10 kHz  (B) 5 kHz  (C) 20 kHz  (D) 2.5 kHz

**Solution:** fs = 2*5k = 10 kHz
**Answer: (A) 10 kHz**

---

### Q6. (Moderate) Sampling theorem applies to:
(A) Band-limited signals  (B) Any  (C) Only periodic  (D) Only DC

**Answer: (A) Band-limited signals (finite max frequency)**

---

### Q7. (Moderate) Sampling at exactly 2fm:
(A) Marginal - ideal low-pass needed  (B) Easy  (C) Oversampling  (D) Undersampling

**Answer: (A) Nyquist at 2fm requires ideal (unrealizable) brick-wall filter - marginal**

---

### Q8. (Moderate) Oversampling (fs >> 2fm):
(A) Easier anti-alias + better SNR  (B) Aliasing  (C) Wastes only  (D) No benefit

**Answer: (A) Oversampling relaxes filter requirement & improves resolution/SNR**

---

### Q9. (Moderate) Aliased frequency for original f with fs low:
(A) Appears as falias = |f - k fs|  (B) Same  (C) Higher  (D) Zero

**Answer: (A) Redirected to |f - k*fs| (folded into baseband)**

---

### Q10. (Moderate) Interpolation (reconstruction) formula uses:
(A) sinc functions  (B) Only rectangles  (C) Noise  (D) DC

**Answer: (A) sinc (bandlimited) interpolation to reconstruct continuous signal**
