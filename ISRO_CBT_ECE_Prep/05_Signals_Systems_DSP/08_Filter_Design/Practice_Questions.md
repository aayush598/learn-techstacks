# Filter Design - Practice Questions

---

### Q1. (Easy) FIR filter impulse response:
(A) Finite length  (B) Infinite  (C) Zero  (D) Always IIR

**Answer: (A) FIR - finite impulse response (no feedback)**

---

### Q2. (Moderate) IIR filter has:
(A) Feedback (poles) infinite response  (B) Only zeros  (C) Finite  (D) No poles

**Answer: (A) IIR - recursive, has feedback/poles, infinite response**

---

### Q3. (Moderate) FIR advantage:
(A) Always stable, linear phase possible  (B) Faster  (C) Fewer taps  (D) No delay

**Answer: (A) FIR - guaranteed stable (all zeros), can do exact linear phase**

---

### Q4. (Moderate) IIR advantage:
(A) Fewer coefficients (efficient, sharper)  (B) Stable  (C) Linear phase  (D) Simple

**Answer: (A) IIR - fewer taps for same spec (uses poles) - more efficient**

---

### Q5. (Moderate) Linear phase FIR implies:
(A) Symmetric coefficients  (B) Asymmetric  (C) Random  (D) Zero

**Answer: (A) Symmetric/antisymmetric impulse response -> constant group delay**

---

### Q6. (Moderate) FIR stability is guaranteed because:
(A) No poles (all zeros only)  (B) Poles inside  (C) High order  (D) Feedback

**Answer: (A) FIR has no feedback poles - always stable**

---

### Q7. (Moderate) Cutoff frequency and transition:
(A) Butterworth flat passband, moderate transition  (B) No cutoff  (C) Unlimited  (D) none

**Answer: (A) Filter specs trade rolloff sharpness vs ripple (Butterworth flat, Chebyshev sharp)**

---

### Q8. (Moderate) Decimation involves:
(A) Downsampling (reduce fs, with low-pass first)  (B) Upsample  (C) Only gain  (D) Only noise

**Answer: (A) Decimation = low-pass + downsampling (anti-alias before reducing rate)**

---

### Q9. (Moderate) Interpolation:
(A) Upsampling + low-pass  (B) Downsample  (C) Only delay  (D) Only gain

**Answer: (A) Interpolation = zero-insert (upsample) + low-pass smoothing**

---

### Q10. (Moderate) Bilinear transform maps s to z via:
(A) s = (2/T)(1-z^-1)/(1+z^-1)  (B) s = z  (C) z = e^s only  (D) none

**Answer: (A) Bilinear transform = s=(2/T)(1-z^-1)/(1+z^-1) for IIR design (warps freq)**
