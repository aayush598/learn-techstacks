# Network Theorems - Practice Questions

## Instructions
Each question has one correct option. For superposition, retain only the source being considered active.

## Questions

### Q1. Superposition [Medium]
A node is fed by a 10 V source through 2 Ω and a 4 V source through 4 Ω. A 6 Ω resistor connects the node to ground. The node voltage is:

A. 5 V  
B. 6 V  
C. 7 V  
D. 9 V

**Answer:** C  
**Explanation:** The 10 V contribution is `10×6/(2+4+6)=5 V`; the 4 V contribution is `4×6/(4+2+6)=2 V`; total is 7 V.

### Q2. Thevenin current [Medium]
A 12 V source with 3 Ω series resistance supplies a 1 kΩ load. The load current is approximately:

A. 3.00 mA  
B. 11.96 mA  
C. 12.00 mA  
D. 15.00 mA

**Answer:** B  
**Explanation:** `I_L=12/(3+1000)=0.01196 A`.

### Q3. Norton equivalent [Easy]
A 10 V source in series with 2.5 kΩ is the Thevenin equivalent of a Norton circuit. The Norton current is:

A. 1 mA  
B. 2 mA  
C. 4 mA  
D. 5 mA

**Answer:** C  
**Explanation:** `I_N=V_th/R_th=10/2.5 kΩ=4 mA`.

### Q4. Maximum power [Easy]
If a source has Thevenin resistance 50 Ω, the load resistance for maximum received power is:

A. 10 Ω  
B. 25 Ω  
C. 50 Ω  
D. 100 Ω

**Answer:** C  
**Explanation:** For a purely resistive source and load, maximum power occurs at `R_L=R_th=50 Ω`.

### Q5. Star-to-delta conversion [Medium]
Three equal star-connected resistors are each 3 Ω. Each equivalent delta resistor is:

A. 1 Ω  
B. 3 Ω  
C. 6 Ω  
D. 9 Ω

**Answer:** D  
**Explanation:** For equal star resistors, `R_delta=3R_Y=9 Ω`.

### Q6. Source transformation [Easy]
A 10 V voltage source in series with 2 kΩ is equivalent to:

A. 2 mA in parallel with 2 kΩ  
B. 5 mA in parallel with 2 kΩ  
C. 5 mA in series with 2 kΩ  
D. 10 mA in parallel with 200 Ω

**Answer:** B  
**Explanation:** `I_N=10/2 kΩ=5 mA`, while the parallel resistance remains 2 kΩ.

### Q7. Reciprocity theorem [Medium]
A reciprocal linear bilateral network is driven at port A, producing a current at port B. When the same source is moved to port B, the corresponding current at A:

A. Is always zero  
B. Has the same value when the loading conditions are interchanged correctly  
C. Is always doubled  
D. Is independent of network elements

**Answer:** B  
**Explanation:** Reciprocity states that the transfer response is unchanged when the source and response positions are interchanged, with the measurement conditions interchanged appropriately.

### Q8. Compensation theorem [Medium]
To find the change in a branch current caused by a source-voltage change `ΔV`, the compensating source used in the compensation theorem has:

A. Voltage `ΔV` with the original polarity  
B. Voltage `−ΔV` in the changed branch  
C. Current `ΔV/R` in series with the branch  
D. Infinite current

**Answer:** B  
**Explanation:** The compensating voltage opposes the imposed change and is introduced in the affected branch to calculate its incremental current.

### Q9. Millman's theorem [Medium]
Two 10 V sources feed a node through 1 kΩ each, and a third 2 kΩ resistor connects the node to ground. The source current from each 10 V branch is approximately:

A. 2.5 mA  
B. 3.3 mA  
C. 5.0 mA  
D. 10.0 mA

**Answer:** C  
**Explanation:** The node voltage is `(10+10)/(1+1+2) kΩ=5 V`; each source supplies `(10−5)/1 kΩ=5 mA`.

### Q10. Norton maximum-power result [Medium]
A Norton source has `I_N=2 A` and `R_N=50 Ω`. The maximum load power is:

A. 25 W  
B. 50 W  
C. 100 W  
D. 200 W

**Answer:** B  
**Explanation:** At maximum power, `R_L=R_N=50 Ω`; `P_max=I_N²R_N/4=4×50/4=50 W`.

## Answer Key
1. C  
2. B  
3. C  
4. C  
5. D  
6. B  
7. B  
8. B  
9. C  
10. B
