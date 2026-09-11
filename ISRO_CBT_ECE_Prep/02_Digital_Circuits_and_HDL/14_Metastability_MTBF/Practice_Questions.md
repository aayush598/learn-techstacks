# Metastability and MTBF - Practice Questions

---

### Q1. (Easy) Metastability occurs when:
(A) Setup/hold violated -> FF settles unpredictably  (B) Normal operation  (C) Always  (D) Never

**Answer: (A) Violation of setup/hold timing - flip-flop output uncertain state**

---

### Q2. (Moderate) Metastable state resolves:
(A) After some finite settling time (unbounded)  (B) Instantly  (C) Never  (D) Same as clock

**Answer: (A) Output eventually settles to 0 or 1 after variable time (probabilistic)**

---

### Q3. (Moderate) Common remedy for metastability:
(A) Synchronizer (2 FF cascade)  (B) Remove clock  (C) More logic  (D) No FFs

**Answer: (A) Two-flip-flop synchronizer - gives FF time to settle before use**

---

### Q4. (Moderate) Async inputs to a clocked system risk:
(A) Metastability  (B) Only noise  (C) Only power  (D) Nothing

**Answer: (A) Asynchronous input changing near clock edge can cause metastability**

---

### Q5. (Moderate) MTBF (mean time between failures):
(A) Average time between metastability events  (B) Lifetime  (C) Clock period  (D) Reset time

**Answer: (A) MTBF - average time between metastability-induced failures**

---

### Q6. (Moderate) Increasing settling time of synchronizer:
(A) Increases MTBF  (B) Decreases  (C) No effect  (D) Reduces clock

**Answer: (A) More settling time (adding FF stages) increases MTBF exponentially**

---

### Q7. (Moderate) Metastability resolution time:
(A) Probabilistic, can exceed clock period  (B) Fixed one gate delay  (C) Zero  (D) Always settle

**Answer: (A) Resolution time is random - may take longer than the clock period (hence failure risk)**

---

### Q8. (Moderate) Two-FF synchronizer works because:
(A) Gives extra full cycle for settling  (B) Removes clock  (C) Adds gates  (D) No FFs

**Answer: (A) The cascaded FF gives an entire clock period for the first FF to settle**
