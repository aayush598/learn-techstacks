# LTI Systems - Practice Questions

---

### Q1. (Easy) LTI system = linear and:
(A) Time-invariant  (B) Time-varying  (C) Memoryless  (D) Nonlinear

**Answer: (A) Linear + Time-Invariant (key: input shift -> output shift)**

---

### Q2. (Moderate) Linearity means:
(A) Superposition (addition & scaling)  (B) Only scaling  (C) Only addition  (D) None

**Answer: (A) Superposition: T{ax1+bx2} = aT{x1} + bT{x2}**

---

### Q3. (Moderate) Time-invariant: x(t-T) input gives:
(A) y(t-T) output  (B) y(t+T)  (C) Different  (D) No relation

**Answer: (A) Same output shifted by T (delay preserved)**

---

### Q4. (Moderate) LTI system characterized by:
(A) Impulse response h(t) (or h[n])  (B) Only DC  (C) Only power  (D) only phase

**Answer: (A) Impulse response completely characterizes an LTI system**

---

### Q5. (Moderate) Causality: output depends only on:
(A) Present/past inputs  (B) Future  (C) All  (D) None

**Answer: (A) Causal - no dependence on future (h(t)=0 for t<0)**

---

### Q6. (Moderate) Stability (BIBO): bounded input produces:
(A) Bounded output (h absolutely summable/integrable)  (B) Unbounded  (C) Zero  (D) No output

**Answer: (A) Bounded-in-bounded-out - |h| integrable (CT) / summable (DT)**

---

### Q7. (Moderate) Output y(t) for input x(t), impulse h(t):
(A) y = x * h (convolution)  (B) x*h always  (C) Product  (D) Ratio

**Answer: (A) y(t) = x(t) * h(t) (convolution integral)**

---

### Q8. (Moderate) Frequency response H(jw):
(A) Fourier transform of h(t)  (B) h(t)  (C) 1/h  (D) None

**Answer: (A) H(jω) = FT of impulse response (eigenvalue, gain vs freq)**

---

### Q9. (Moderate) Sinusoid into LTI gives:
(A) Same sinusoid, scaled + phased  (B) Distorted  (C) DC  (D) Noise

**Answer: (A) Sinusoidal steady state - same freq, amplitude*|H|, phase*arg H**

---

### Q10. (Moderate) The memoryless LTI system has impulse response:
(A) h(t) = K δ(t)  (B) h(t)=u(t)  (C) h(t)=e^-t  (D) any h

**Answer: (A) Memoryless LTI -> h(t) = constant * δ(t) (no history)**
