# Verilog - Practice Questions

---

### Q1. (Easy) Verilog module describes:
(A) Only timing  (B) Interface + behavior  (C) Only power  (D) Only layout

**Answer: (B) Interface (ports) + behavior (like VHDL entity+arch)**

---

### Q2. (Easy) wire is assigned with:
(A) always  (B) assign  (C) reg  (D) initial

**Answer: (B) assign (continuous) or structural - wire made in combinational**

---

### Q3. (Moderate) reg is used:
(A) Outside always  (B) Inside always (procedural)  (C) Only in structural  (D) Only with assign

**Answer: (B) Inside always blocks (stores procedural assignment)**

---

### Q4. (Moderate) For sequential logic (D FF) you use:
(A) assign  (B) always @(posedge clk) with <=  (C) always @(*) with =  (D) gate

**Answer: (B) always @(posedge clk) with non-blocking (<=)**

---

### Q5. (Moderate) Blocking assignment (=) is for:
(A) sequential  (B) combinational  (C) memory  (D) clock

**Answer: (B) Combinational logic (immediate update)**

---

### Q6. (Moderate) Non-blocking (<=) is for:
(A) combinational  (B) sequential/registers  (C) wires  (D) constants

**Answer: (B) Sequential (registers) - samples old values**

---

### Q7. (Moderate) always @(*) is sensitive to:
(A) Only clock  (B) All inputs read  (C) Nothing  (D) Reset only

**Answer: (B) All inputs (combinational awareness)**

---

### Q8. (Moderate) {a, b} is:
(A) XOR  (B) Concatenation  (C) AND  (D) Comparison

**Answer: (B) Concatenation**

---

### Q9. (Moderate) To declare 8-bit register:
(A) reg [7:0] r  (B) wire [7:0] r  (C) integer r  (D) input r

**Answer: (A) reg [7:0] r**

---

### Q10. (Moderate) Which describes a counter structure properly?
(A) always @(posedge clk) cnt <= cnt+1  (B) assign cnt = cnt+1  (C) only gates  (D) initial

**Answer: (A) always @(posedge clk) with non-blocking increment**
