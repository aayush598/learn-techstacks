# VHDL Advanced - Practice Questions

---

### Q1. (Easy) Generic in VHDL is used for:
(A) Parameterizing module (width, size)  (B) Delaying  (C) Power  (D) Assertion

**Answer: (A) Generics - parameterize component (e.g., width N) at instantiation**

---

### Q2. (Moderate) Generate statement:
(A) Creates repeated structures  (B) Simulation delay  (C) Only RTL  (D) Assertion

**Answer: (A) FOR/IF generate replicates instantiations (hierarchical build)**

---

### Q3. (Moderate) Signal vs variable: signal update is:
(A) Delta deferred (end of process)  (B) Immediate  (C) Never  (D) Always zero

**Answer: (A) Signal assignment takes effect after delta (end of the process)**

---

### Q4. (Moderate) Variable assignment:
(A) := immediate  (B) <= deferred  (C) Never  (D) only bit

**Answer: (A) Variable uses := and updates immediately (within process)**

---

### Q5. (Moderate) Package is for:
(A) Reusable declarations (functions, types, consts)  (B) Only components  (C) Timing  (D) Power

**Answer: (A) Package - shared function/type/constant declarations across designs**

---

### Q6. (Moderate) Which process form for Moore FSM state register:
(A) Process(clk) with rising_edge  (B) Process(*) only  (C) assign  (D) select

**Answer: (A) Clocked process (posedge/reset) stores state**

---

### Q7. (Moderate) Synthesizable construct:
(A) process with if/case  (B) after  (C) wait  (D) file

**Answer: (A) Process (if/case/assignments) - after/wait/file not synthesizable**

---

### Q8. (Moderate) Record type is:
(A) User composite type (fields)  (B) Only single bit  (C) Only std logic  (D) Memory

**Answer: (A) Record - composite with named fields (like struct)**

---

### Q9. (Moderate) Function vs procedure difference:
(A) Function returns value, procedure may not  (B) Same  (C) Procedure returns  (D) None

**Answer: (A) Function returns a value; procedure is a statement (may not return)**

---

### Q10. (Moderate) Attribute 'event used for:
(A) Detecting signal change (clock edge)  (B) Power  (C) Delay only  (D) Area

**Answer: (A) 'event - detect change; clk'event and clk='1' = rising edge**
