# Finite State Machines - Practice Questions

---

### Q1. (Easy) FSM is a:
(A) Sequential circuit with defined states  (B) Combinational only  (C) Memory only  (D) No clock

**Answer: (A) Sequential machine - states + transitions based on inputs/clock**

---

### Q2. (Moderate) Moore machine output depends on:
(A) Only present state  (B) Inputs only  (C) Both  (D) Clock edge only

**Answer: (A) Moore - output = f(present state only)**

---

### Q3. (Moderate) Mealy machine output depends on:
(A) Present state AND input  (B) State only  (C) Input only  (D) None

**Answer: (A) Mealy - output = f(state, input); can respond faster to input**

---

### Q4. (Moderate) Mealy vs Moore: Mealy has:
(A) Fewer states (uses input in output)  (B) More states  (C) No states  (D) Same always

**Answer: (A) Mealy often fewer states; Moore outputs change on clock (safer)**

---

### Q5. (Moderate) Number of FFs for N states:
(A) ceil(log2 N)  (B) N  (C) 2N  (D) N/2

**Answer: (A) ceil(log2 N) flip-flops (binary encoding)**

---

### Q6. (Moderate) One-hot encoding uses:
(A) N FFs for N states (one active)  (B) log N  (C) 2N  (D) N/2

**Answer: (A) One-hot = N flip-flops for N states (simpler decode, more FFs)**

---

### Q7. (Moderate) A 4-state FSM binary-coded needs:
(A) 2 FFs  (B) 4  (C) 8  (D) 1

**Solution:** log2(4) = 2
**Answer: (A) 2 flip-flops**

---

### Q8. (Moderate) Sequence detector is a:
(A) FSM (recognizes pattern in bit stream)  (B) Combinational  (C) ONLY MUX  (D) No clock

**Answer: (A) FSM that detects a specific input sequence (state machine)**

---

### Q9. (Moderate) In a Moore machine, output timing:
(A) Synchronized to clock (state change)  (B) Instant on input  (C) Random  (D) No clock

**Answer: (A) Moore outputs change only on clock edge (synchronous, no glitches from input)**

---

### Q10. (Moderate) Clock is essential in FSM for:
(A) Sequencing state transitions  (B) Only power  (C) Only output  (D) Nothing

**Answer: (A) Clock controls state transitions (synchronous sequential logic)**
