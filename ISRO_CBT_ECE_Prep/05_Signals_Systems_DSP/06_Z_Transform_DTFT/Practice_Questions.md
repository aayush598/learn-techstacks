# Z-Transform and DTFT - Practice Questions

---

### Q1. (Easy) Z-transform converts discrete time to:
(A) Z-domain (complex)  (B) s-domain  (C) jw only  (D) Time

**Answer: (A) Z-domain - X(z) = sum x[n] z^{-n}**

---

### Q2. (Moderate) Z-transform of unit step u[n]:
(A) z/(z-1)  (B) 1  (C) 1/z  (D) z

**Answer: (A) Z{u[n]} = z/(z-1), |z|>1**

---

### Q3. (Moderate) Z-transform of impulse δ[n]:
(A) 1  (B) z/(z-1)  (C) 1/z  (D) z-1

**Answer: (A) Z{δ[n]} = 1**

---

### Q4. (Moderate) Z-transform of a^n u[n]:
(A) z/(z-a)  (B) 1/(z-a)  (C) z/a  (D) a/z

**Answer: (A) Z{a^n u[n]} = z/(z-a), |z|>|a|**

---

### Q5. (Moderate) Time shift property:
(A) x[n-k] <-> z^{-k} X(z)  (B) z^k X  (C) X/z^k  (D) no change

**Answer: (A) Delay by k -> multiply by z^{-k}**

---

### Q6. (Moderate) Difference equation solved using Z:
(A) Taking Z-transform, algebraic solve  (B) Only integration  (C) Only Fourier  (D) no

**Answer: (A) Z-transform converts difference eq to algebraic eq**

---

### Q7. (Moderate) Discrete system stable if poles (in z):
(A) Inside unit circle (|z|<1)  (B) Outside  (C) On unit circle  (D) Any

**Answer: (A) All poles inside unit circle for BIBO stability**

---

### Q8. (Moderate) DTFT is Z-transform evaluated on:
(A) Unit circle (z = e^{jw})  (B) jw axis  (C) Real axis  (D) Whole plane

**Answer: (A) DTFT = X(e^{jw}) = Z-transform on unit circle**

---

### Q9. (Moderate) Z-transform of n a^n u[n]:
(A) a z/(z-a)^2  (B) z/(z-a)  (C) z^2/(z-a)^2  (D) a/z

**Answer: (A) Z{n a^n u[n]} = a z/(z-a)^2**

---

### Q10. (Moderate) Causality: ROC of right-sided sequence:
(A) Exterior of circle (|z|>r)  (B) Interior  (C) Annulus  (D) Any

**Answer: (A) Right-sided/causal -> ROC outside outermost pole (|z| > rmax)**
