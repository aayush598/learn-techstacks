# Two-Port Networks - Practice Questions

## Instructions
Each question has one correct option. For Z and Y parameters, use the common convention that both port currents are referenced into the network.

## Questions

### Q1. Open-circuit input impedance [Easy]
The parameter `Z₁₁` is measured with:

A. Port 1 shorted  
B. Port 1 open  
C. `V₂=0`  
D. `I₂=0`

**Answer:** D  
**Explanation:** Z parameters are open-circuit parameters, so `Z₁₁=V₁/I₁` with `I₂=0`.

### Q2. Short-circuit input admittance [Easy]
The parameter `Y₁₁` is measured with:

A. `I₂=0`  
B. `V₂=0`  
C. `I₁=0`  
D. Both ports open

**Answer:** B  
**Explanation:** Y parameters are short-circuit parameters, so `Y₁₁=I₁/V₁` with `V₂=0`.

### Q3. Z-to-Y conversion [Medium]
A two-port has `[Z]=[[4,2],[2,6]] Ω`. What is `Y₁₁`?

A. `0.20 S`  
B. `0.25 S`  
C. `0.30 S`  
D. `0.40 S`  

**Answer:** C  
**Explanation:** `Δ_Z=4×6−2×2=20`; `Y₁₁=Z₂₂/Δ_Z=6/20=0.30 S`.

### Q4. Reciprocity [Easy]
A passive reciprocal two-port satisfies:

A. `Z₁₁=Z₂₂` only  
B. `Z₁₂=Z₂₁`  
C. `Z₁₁Z₂₂=0`  
D. `A=D` only

**Answer:** B  
**Explanation:** Reciprocity requires equal off-diagonal Z parameters, equivalently `Y₁₂=Y₂₁` or `AD−BC=1`.

### Q5. Symmetry [Easy]
A two-port is symmetric if:

A. `Z₁₂=Z₂₁`  
B. `Z₁₁=Z₂₂`  
C. `Y₁₁+Y₂₂=0`  
D. `A=1/D` only

**Answer:** B  
**Explanation:** Symmetry means its two port sides are mirror-equivalent; for a reciprocal network, it also satisfies `Z₁₂=Z₂₁`.

### Q6. Series impedance matrix [Medium]
A series impedance `Z` connects the two ports, with both port currents referenced into the network. Its Z-parameter matrix is:

A. `[[Z,Z],[Z,Z]]`  
B. `[[Z,−Z],[−Z,Z]]`  
C. `[[0,Z],[Z,0]]`  
D. `[[1/Z,0],[0,1/Z]]`

**Answer:** B  
**Explanation:** The internal node obeys `V₁=Z(I₁−I₂)` and `V₂=Z(I₂−I₁)`, giving the stated matrix.

### Q7. ABCD cascade [Medium]
For `[ABCD]₁=[[1,2],[0.5,1]]` and `[ABCD]₂=[[1,4],[0.25,1]]`, the cascade parameter `C_total` is:

A. 0.5  
B. 0.75  
C. 1.00  
D. 1.25

**Answer:** B  
**Explanation:** Cascade matrices multiply in signal-flow order: `C_total=0.5×1+1×0.25=0.75`.

### Q8. Input impedance from ABCD [Medium]
A two-port has `A=2`, `B=0`, `C=0`, and `D=0.5`, with a `Z_L=8 Ω` load. Its input impedance is:

A. 2 Ω  
B. 4 Ω  
C. 16 Ω  
D. 32 Ω

**Answer:** D  
**Explanation:** `Z_in=(AZ_L+B)/(CZ_L+D)=16/4=32 Ω`.

### Q9. Ideal transformer loading [Medium]
An ideal 2:1 step-up transformer has `N₁/N₂=2` and a secondary load of 8 Ω. The impedance reflected to the primary is:

A. 2 Ω  
B. 4 Ω  
C. 16 Ω  
D. 32 Ω

**Answer:** D  
**Explanation:** `Z_in=(N₁/N₂)²Z_L=2²×8=32 Ω`.

### Q10. Lossless transmission line [Medium]
A lossless line of length `l`, characteristic impedance `Z₀`, and propagation constant `γ` has ABCD matrix:

A. `[[cosh(γl),Z₀sinh(γl)],[sinh(γl)/Z₀,cosh(γl)]]`  
B. `[[sinh(γl),Z₀cosh(γl)],[cosh(γl)/Z₀,sinh(γl)]]`  
C. `[[Z₀cosh(γl),sinh(γl)],[cosh(γl)/Z₀,Z₀sinh(γl)]]`  
D. `[[1,γl],[γl,1]]`

**Answer:** A  
**Explanation:** This is the standard ABCD matrix for a uniform line section.

## Answer Key
1. D  
2. B  
3. C  
4. B  
5. B  
6. B  
7. B  
8. D  
9. D  
10. A
