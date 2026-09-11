# Signals and Systems - Practice Questions

---

### Q1. (Easy) Convolution x(t)*delta(t-2):
(A) x(t)  (B) x(t-2)  (C) x(t+2)  (D) delta(t-2)

**Answer: (B) x(t-2) (time shift)**

---

### Q2. (Easy) Period of x(t)=cos(2t)+sin(t):
(A) pi  (B) 2pi  (C) 4pi  (D) Not periodic

**Solution:** Periods: cos2t->pi, sint->2pi. LCM = 2pi
**Answer: (B) 2pi**

---

### Q3. (Moderate) y(t) = x(t)+c (constant offset). Is system linear?
(A) Yes  (B) No  (C) Sometimes  (D) Only if c=0

**Answer: (D) Only if c=0 (linear requires homogeneity & superposition; constant breaks it)**

---

### Q4. (Moderate) LTI system h(t)=u(t). Stability:
(A) BIBO stable  (B) Marginal  (C) Unstable  (D) Cannot tell

**Solution:** integral|u|dt = integral dt -> infinite -> unstable
**Answer: (C) Unstable**

---

### Q5. (Moderate) DFT of length N requires how many complex multiply (direct):
(A) N  (B) N^2  (C) N log N  (D) (N/2)logN

**Answer: (B) N^2**

---

### Q6. (Moderate) FFT of N=1024 stages:
(A) 8  (B) 9  (C) 10  (D) 11

**Answer: (C) 10 (log2 1024)**

---

### Q7. (Moderate) ISI is reduced by:
(A) Raised cosine filtering  (B) Wider pulse  (C) More power  (D) Lower freq

**Answer: (A) Raised cosine (Nyquist pulse shaping)**

---

### Q8. (Moderate) Z-transform of a^n u[n]:
(A) z/(z-a)  (B) 1/(z-a)  (C) z/(z+a)  (D) 1/z-a

**Answer: (A) z/(z-a)**

---

### Q9. (Moderate) FIR filter is stable because:
(A) Poles at origin  (B) No poles  (C) Zeros at origin  (D) Feedback

**Answer: (A) Poles at z=0 (inside unit circle) -> always stable**

---

### Q10. (Moderate) For a causal IIR to be stable, all poles must be:
(A) In LHP (s-plane)  (B) Inside unit circle (z-plane)  (C) On unit circle  (D) At origin only

**Answer: (B) Inside unit circle (z-plane, discrete)**

---

### Q11. (Moderate) Nyquist rate of 6 kHz signal:
(A) 3 kHz  (B) 6 kHz  (C) 12 kHz  (D) 24 kHz

**Answer: (C) 12 kHz (2*fmax)**

---

### Q12. (Moderate) Signals with finite total energy:
(A) Power signal  (B) Energy signal  (C) Both  (D) Neither
