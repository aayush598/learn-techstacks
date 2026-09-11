# Sequential Circuits - Practice Questions

---

### Q1. (Easy) D flip-flop next state:
(A) Q  (B) D  (C) D'  (D) indeterminate

**Answer: (B) Q+ = D**

---

### Q2. (Easy) SR FF invalid state:
(A) S=0,R=0  (B) S=0,R=1  (C) S=1,R=0  (D) S=1,R=1

**Answer: (D) S=R=1 (ambiguous/race)**

---

### Q3. (Moderate) JK FF with J=K=1:
(A) Hold  (B) Set  (C) Toggle  (D) Reset

**Answer: (C) Toggle (Q+ = Q')**

---

### Q4. (Moderate) T FF with T=1 divides frequency by:
(A) 1  (B) 2  (C) 3  (D) 4

**Answer: (B) 2 (toggles once per 2 clocks)**

---

### Q5. (Moderate) Characteristic equation of JK FF:
(A) Q+=S+R'Q  (B) Q+=J Q'+K'Q  (C) Q+=D  (D) Q+=TQ'+T'Q

**Answer: (B) Q+ = J Q' + K' Q**

---

### Q6. (Moderate) Edge-triggered FF preferred over latch because:
(A) Cheaper  (B) Synchronous (defined capture at edge)  (C) Faster only  (D) No clock

**Answer: (B) Well-defined capture on clock edge (proper synchronous design)**

---

### Q7. (Moderate) Setup time is:
(A) Output delay after clock  (B) Min time data before clock edge  (C) Clock period  (D) Hold after

**Answer: (B) Minimum time data must be stable BEFORE the clock edge**

---

### Q8. (Moderate) D to T conversion: D =
(A) Q  (B) T XOR Q  (C) T  (D) T'

**Answer: (B) D = T XOR Q**
