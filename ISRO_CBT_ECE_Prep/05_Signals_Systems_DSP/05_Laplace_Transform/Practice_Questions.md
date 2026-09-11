# Laplace Transform - Practice Questions

---

### Q1. (Easy) Laplace transform converts time to:
(A) Complex frequency (s-domain)  (B) Real frequency only  (C) Z-domain  (D) Time domain

**Answer: (A) s-domain (Laplace), s = σ + jω**

---

### Q2. (Moderate) Laplace of unit step u(t):
(A) 1/s  (B) 1  (C) 1/s^2  (D) s

**Answer: (A) L{u(t)} = 1/s**

---

### Q3. (Moderate) Laplace of impulse δ(t):
(A) 1  (B) 1/s  (C) 0  (D) s

**Answer: (A) L{δ(t)} = 1**

---

### Q4. (Moderate) Laplace of e^{-at}u(t):
(A) 1/(s+a)  (B) 1/s  (C) 1/(s-a)  (D) s/(s+a)

**Answer: (A) L{e^{-at}u(t)} = 1/(s+a)**

---

### Q5. (Moderate) Differentiation property:
(A) dx/dt <-> s X(s) - x(0)  (B) X(s)/s  (C) s X(s)  (D) X(s)/s^2

**Answer: (A) L{dx/dt} = sX(s) - x(0) (accounts initial condition)**

---

### Q6. (Moderate) Poles of H(s)=1/(s+2) gives:
(A) Exponential e^{-2t} (decaying)  (B) Growing  (C) Sinusoid  (D) DC

**Answer: (A) Pole at s=-2 -> e^{-2t} decaying (stable if real part <0)**

---

### Q7. (Moderate) System stability: all poles must be:
(A) In left-half s-plane (real part < 0)  (B) Right  (C) On jw axis only  (D) None

**Answer: (A) All poles in left half plane (negative real parts) for BIBO stability**

---

### Q8. (Moderate) Final value theorem:
(A) lim t->inf x(t) = lim s->0 s X(s)  (B) =X(0)  (C) =X(inf)  (D) none

**Answer: (A) f(∞) = lim_{s→0} s X(s) (if poles in LHP)**

---

### Q9. (Moderate) Laplace of t^n u(t):
(A) n!/s^(n+1)  (B) 1/s^n  (C) n/s  (D) (n!/s^n)

**Answer: (A) L{t^n} = n!/s^(n+1)**

---

### Q10. (Moderate) For causal system ROC is:
(A) To right of rightmost pole  (B) Left  (C) Anywhere  (D) Between poles

**Answer: (A) Causal -> ROC right of rightmost pole (Re(s) > pole)**
