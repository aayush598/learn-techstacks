# VHDL - Practice Questions

---

### Q1. (Easy) In VHDL, interface is described by:
(A) Architecture  (B) Entity  (C) Package  (D) Configuration

**Answer: (B) Entity**

---

### Q2. (Easy) Implementation behavior is in:
(A) Entity  (B) Architecture  (C) Port  (D) Process

**Answer: (B) Architecture**

---

### Q3. (Moderate) Which signal assignment is for concurrent (dataflow)?
(A) :=  (B) <=  (C) =  (D) ==

**Answer: (B) <= (signal assignment, concurrent/process)**

---

### Q4. (Moderate) std_logic has how many logic values?
(A) 2  (B) 4  (C) 9  (D) 16

**Answer: (C) 9 values (U,X,0,1,Z,W,L,H,-)**

---

### Q5. (Moderate) Sequential statements in VHDL are inside:
(A) assign  (B) process  (C) with-select  (D) entity

**Answer: (B) process**

---

### Q6. (Moderate) Package for signed/unsigned arithmetic:
(A) std_logic_1164  (B) numeric_std  (C) standard  (D) arithmetic

**Answer: (B) ieee.numeric_std**

---

### Q7. (Moderate) Signal vs variable assignment:
(A) Both <=  (B) signal <=, variable :=  (C) signal :=, variable <=  (D) both :=

**Answer: (B) Signal uses <=, variable uses :=**

---

### Q8. (Moderate) Generate statement is used for:
(A) Simulation  (B) Repeated structure creation  (C) Delay  (D) Assertion

**Answer: (B) Repeated structure (for generate replicating instances)**

---

### Q9. (Moderate) Non-blocking drawing equivalent in VHDL for D FF:
(A) always  (B) rising_edge(clk) process  (C) assign  (D) select

**Answer: (B) Process with if rising_edge(clk) then q<=d**

---

### Q10. (Moderate) Which is synthesizable?
(A) after  (B) process  (C) wait  (D) file I/O

**Answer: (B) process (after/wait/file are simulation-only)**
