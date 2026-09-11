# Digital Filter Structures - Practice Questions

---

### Q1. (Easy) Direct Form I IIR:
(A) Zeros then poles (cascaded)  (B) Poles then zeros  (C) Only zeros  (D) None

**Answer: (A) DF-I - all zeros then all poles in cascade, more delay elements**

---

### Q2. (Moderate) Direct Form II:
(A) Poles then zeros, shared delay (canonic)  (B) More delays  (C) Only feedforward  (D) None

**Answer: (A) DF-II - less memory (shares delay, canonic), poles first**

---

### Q3. (Moderate) Canonic structure has minimum number of:
(A) Delay elements (max(m,n))  (B) Multipliers only  (C) Adders  (D) Poles

**Answer: (A) Canonic = minimum delays = max(order numerator, denominator)**

---

### Q4. (Moderate) Cascade form divides transfer function into:
(A) Second-order sections (biquads)  (B) Only first order  (C) One big  (D) None

**Answer: (A) Cascade of 2nd-order (biquad) sections - good coefficient sensitivity**

---

### Q5. (Moderate) Parallel form uses:
(A) Partial fraction (1st/2nd order parallel)  (B) Cascade only  (C) Only delays  (D) None

**Answer: (A) Parallel - partial fraction expansion into parallel sections**

---

### Q6. (Moderate) Advantage of cascade/parallel over direct:
(A) Better sensitivity to coefficient quantization  (B) More noise  (C) Faster only  (D) Simpler

**Answer: (A) Lower coefficient sensitivity & better numerical behavior (for high order)**

---

### Q7. (Moderate) FIR can be realized in:
(A) Direct & transposed (also polyphase/FFT)  (B) Only recursion  (C) No structure  (D) None

**Answer: (A) FIR - direct, transposed, cascade, polyphase, FFT-based structures**

---

### Q8. (Moderate) Transposed structure:
(A) Reversal of signal flow (same transfer fn)  (B) Changes response  (C) Adds poles  (D) unstable

**Answer: (A) Transposed - flow-graph reversal, same TF, sometimes better numerical**

---

### Q9. (Moderate) Coefficient quantization causes:
(A) Pole/zero shift, possible instability (IIR)  (B) No effect  (C) Faster  (D) More bits

**Answer: (A) Quantizing coefficients moves poles/zeros - can make IIR unstable**

---

### Q10. (Moderate) State-space/DF-II advantage:
(A) Lower memory & coefficient sensitivity (via sections)  (B) Slower  (C) More taps  (D) None

**Answer: (A) Section decomposition / canonic reduces memory & sensitivity**
