# Adders and Subtractors - Practice Questions

---

### Q1. (Easy) Half adder has:
(A) 2 inputs 1 output  (B) 2 inputs 2 outputs  (C) 3 inputs 2 outputs  (D) 1 input 1 output

**Answer: (B) 2 inputs (A,B), 2 outputs (Sum, Carry)**

---

### Q2. (Easy) Full adder sum expression:
(A) A AND B  (B) A XOR B XOR Cin  (C) A OR B  (D) A NOR B

**Answer: (B) A XOR B XOR Cin**

---

### Q3. (Moderate) Full adder carry out (majority):
(A) AB  (B) AB + ACin + BCin  (C) A+B+Cin  (D) XOR

**Answer: (B) AB + ACin + BCin (any two 1s)**

---

### Q4. (Moderate) Ripple carry adder main drawback:
(A) Complex  (B) Slow (carry propagates serially)  (C) High power  (D) Low gain

**Answer: (B) Slow - carry delay proportional to number of bits**

---

### Q5. (Moderate) CLA uses generate G and propagate P where:
(A) G=Ai AND Bi, P=Ai XOR Bi  (B) G=Ai XOR Bi, P=Ai AND Bi  (C) G=A+B  (D) none

**Answer: (A) G=A&B (generate), P=A^B (propagate)**

---

### Q6. (Moderate) Carry next in CLA:
(A) G + P C  (B) G P  (C) G XOR P  (D) P + G'

**Answer: (A) Ci+1 = Gi + Pi Ci**

---

### Q7. (Moderate) Subtract A-B using adder:
(A) A+B  (B) A+B'+1  (C) A-B'  (D) A'+B

**Answer: (B) A + (two's complement of B) = A + B' + 1**

---

### Q8. (Moderate) XOR gate is used in adder as:
(A) Carry only  (B) Sum  (C) Both sum and propagate  (D) None

**Answer: (C) Sum (A^B^Cin) and propagate (P=A^B)**
