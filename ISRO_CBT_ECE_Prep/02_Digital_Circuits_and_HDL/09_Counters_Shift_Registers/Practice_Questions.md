# Counters and Shift Registers - Practice Questions

---

### Q1. (Easy) Modulus of 3-bit counter:
(A) 3  (B) 8  (C) 6  (D) 4

**Answer: (B) 8 (2^3 = 8 states, 0-7)**

---

### Q2. (Easy) A modulus-N counter divides input frequency by:
(A) N/2  (B) N  (C) 2N  (D) log N

**Answer: (B) N (f_out = f_clk / N)**

---

### Q3. (Moderate) Number of FFs needed for mod-10 counter:
(A) 3  (B) 4  (C) 5  (D) 10

**Solution:** N = ceil(log2 10) = ceil(3.32) = 4
**Answer: (B) 4**

---

### Q4. (Moderate) Ripple counter drawback vs synchronous:
(A) More power  (B) Slower (carry ripple delay)  (C) Complex  (D) More FFs

**Answer: (B) Slower - propagation delay accumulates across stages**

---

### Q5. (Moderate) N-FF Johnson counter states:
(A) N  (B) 2N  (C) 2^N  (D) N^2

**Answer: (B) 2N states**

---

### Q6. (Moderate) N-FF ring counter states:
(A) N  (B) 2N  (C) 2^N  (D) N/2

**Answer: (A) N states (one-hot)**

---

### Q7. (Moderate) Which shift register shifts data to a register and reads parallel:
(A) SISO  (B) SIPO  (C) PISO  (D) PIPO

**Answer: (B) SIPO (serial in, parallel out)**

---

### Q8. (Moderate) Cascade two divide-by-4 counters: total division:
(A) 4  (B) 8  (C) 16  (D) 2

**Solution:** M_total = 4*4 = 16
**Answer: (C) 16**
