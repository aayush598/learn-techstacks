# Subject-Wise Test - Digital Circuits and HDL

## 20 Questions, 25 Minutes, +1/−0.33

## Questions

**Q1.** By De Morgan's theorem, `(A+B)′` equals:

A. `A′+B′`  
B. `A′B′`  
C. `A+B`  
D. `AB`

**Q2.** A full adder requires how many input bits?

A. 2  
B. 3  
C. 4  
D. 5

**Q3.** A 4-bit ripple-carry adder consists of how many full adders?

A. 2  
B. 3  
C. 4  
D. 8

**Q4.** The minimum number of flip-flops needed for a modulo-13 counter is:

A. 2  
B. 3  
C. 4  
D. 13

**Q5.** A 4:1 multiplexer has how many select lines?

A. 1  
B. 2  
C. 3  
D. 4

**Q6.** A conventional 6-transistor SRAM cell stores one bit using:

A. One capacitor and one transistor  
B. Cross-coupled inverter latches  
C. A magnetic core only  
D. A floating-gate charge

**Q7.** Unlike SRAM, ordinary DRAM requires periodic:

A. Refresh  
B. Recalibration only  
C. Analog-to-digital conversion  
D. Clock multiplication

**Q8.** In VHDL, a concurrent signal assignment uses:

A. `:=`  
B. `<=`  
C. `==`  
D. `=>`

**Q9.** A nonblocking assignment in synthesizable Verilog uses:

A. `:=`  
B. `<=`  
C. `==`  
D. `===`

**Q10.** In a Moore finite-state machine, the output depends on:

A. Present state only  
B. Present state and next input  
C. Input only  
D. Past outputs

**Q11.** Metastability is most likely when:

A. Setup and hold times are comfortably met  
B. A flip-flop input changes near its active clock edge  
C. The clock is stopped far from the edge  
D. Reset is active

**Q12.** A memory with 2¹⁶ addressable words needs at least:

A. 8 address lines  
B. 16 address lines  
C. 32 address lines  
D. 64 address lines

**Q13.** The 4-bit Gray code corresponding to binary 1010 is:

A. 1100  
B. 1110  
C. 1111  
D. 1011

**Q14.** A 16×8 RAM has:

A. 4 address and 8 data lines  
B. 8 address and 4 data lines  
C. 16 address and 8 data lines  
D. 24 address and 8 data lines

**Q15.** UART is fundamentally:

A. A synchronous parallel protocol  
B. An asynchronous serial communication method  
C. A memory technology  
D. A clocking PLL

**Q16.** An ideal 8-bit ADC has:

A. 128 levels  
B. 256 levels  
C. 512 levels  
D. Unbounded levels

**Q17.** A monotonic DAC is characterized by output never:

A. Increasing  
B. Decreasing as the code increases  
C. Staying finite  
D. Using binary input

**Q18.** Pipelining primarily improves:

A. Input latency only  
B. Maximum throughput  
C. Gate count only  
D. Fan-out

**Q19.** VHDL processes are sensitive to all signals listed in the:

A. Port map only  
B. Sensitivity list  
C. Architecture name only  
D. End package

**Q20.** Safe transfer of one bit between unrelated clock domains commonly uses:

A. A direct combinational path  
B. A synchronizer, often two flip-flops  
C. An analog ground  
D. Combinational feedback

## Answer Key

| Question | Answer | Question | Answer |
|---:|:---:|---:|:---:|
| 1 | B | 11 | B |
| 2 | B | 12 | B |
| 3 | C | 13 | C |
| 4 | C | 14 | A |
| 5 | B | 15 | B |
| 6 | B | 16 | B |
| 7 | A | 17 | B |
| 8 | B | 18 | B |
| 9 | B | 19 | B |
| 10 | A | 20 | B |

## Quick Solutions

4. `2³<13≤2⁴`, so four flip-flops are required.  
6. The 6T cell uses two cross-coupled inverters and two access transistors.  
13. Gray bits are adjacent binary XORs: `1,1,1,1`.  
16. An `n`-bit ADC has `2ⁿ=256` ideal levels.
