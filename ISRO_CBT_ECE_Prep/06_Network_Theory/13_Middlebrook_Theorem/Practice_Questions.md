# Middlebrook Extra Element Theorem - Practice Questions

## Instructions
Each question has one correct option. Here `T(∞)` uses an open extra impedance and `T(0)` uses a short extra impedance.

## Questions

### Q1. Open-reference EET form [Easy]
The Extra Element Theorem can be written as:

A. `T(Z)=T(∞)(1+Z_n/Z)/(1+Z_d/Z)`  
B. `T(Z)=T(0)(1+Z_d/Z)/(1+Z_n/Z)`  
C. `T(Z)=Z_n/Z_d` only  
D. `T(Z)=T(∞)+Z_d−Z_n`

**Answer:** A  
**Explanation:** The standard open-reference form multiplies the reference gain by the null/drive correction factor.

### Q2. Short-reference EET form [Easy]
An equivalent form of the Extra Element Theorem is:

A. `T(Z)=T(0)(1+Z/Z_n)/(1+Z/Z_d)`  
B. `T(Z)=T(0)(1+Z_d/Z)`  
C. `T(Z)=T(∞)(1−Z/Z_d)`  
D. `T(Z)=Z(1+Z_n/Z_d)`

**Answer:** A  
**Explanation:** With the extra impedance shorted as the reference, the impedance ratios are inverted.

### Q3. Meaning of `T(∞)` [Easy]
`T(∞)` is the transfer function when the extra impedance is:

A. Shorted  
B. Open-circuited  
C. Replaced by a resistor of value R  
D. Driven by the output

**Answer:** B  
**Explanation:** `∞` denotes the open/infinite-impedance reference condition.

### Q4. Driving impedance `Z_d` [Medium]
`Z_d` is found at the extra-element terminals with the extra element absent and:

A. The input signal set to zero  
B. The output signal merely disconnected  
C. All capacitors shorted  
D. The extra element still connected

**Answer:** A  
**Explanation:** `Z_d` is the single-injection driving-point impedance under the zero-input condition.

### Q5. Null impedance `Z_n` [Medium]
`Z_n` is obtained through the null double-injection test and is associated with the:

A. Output-null condition  
B. Open-circuit source only  
C. Maximum power load  
D. Series resonance only

**Answer:** A  
**Explanation:** The null impedance uses the output nulling condition and represents the transfer-network contribution seen at the inserted element.

### Q6. Numerical EET correction [Medium]
If `T(∞)=3`, `Z_n=4 Ω`, `Z_d=1 Ω`, and `Z=2 Ω`, then `T(Z)` is:

A. 2  
B. 4  
C. 5  
D. 6

**Answer:** D  
**Explanation:** `T=3(1+4/2)/(1+1/2)=3×3/1.5=6`.

### Q7. Short-reference gain [Medium]
Using the open-reference form, `T(0)` is:

A. `T(∞)Z_d/Z_n`  
B. `T(∞)Z_n/Z_d`  
C. `T(∞)(1+Z_n/Z_d)`  
D. `T(∞)Z_nZ_d`

**Answer:** B  
**Explanation:** Taking `Z→0` gives `T(0)=T(∞)Z_n/Z_d`.

### Q8. Correction factor equal to one [Easy]
The EET correction factor is unity when:

A. `Z=0` only  
B. `Z_n=Z_d`  
C. `T(∞)=0` only  
D. `Z=1 Ω` only

**Answer:** B  
**Explanation:** If `Z_n=Z_d`, the numerator and denominator correction factors are equal.

### Q9. Inserting a capacitor [Medium]
For an extra capacitor with `Z_C=1/(sC)`, the EET correction becomes:

A. `(1+sCZ_n)/(1+sCZ_d)`  
B. `(1+sCZ_d)/(1+sCZ_n)`  
C. `sC(Z_d−Z_n)` only  
D. `1+sC(Z_n+Z_d)`

**Answer:** A  
**Explanation:** Substituting `Z=1/(sC)` into the open-reference formula gives the stated pole-zero correction factor.

### Q10. Main purpose of EET [Easy]
The principal practical benefit of Middlebrook's theorem is:

A. Avoiding full reanalysis when an extra element is added  
B. Replacing all transistor models  
C. Converting every network to a star form  
D. Computing Fourier coefficients

**Answer:** A  
**Explanation:** EET reuses a previously found reference transfer function plus two driving-point impedances to insert an extra element.

## Answer Key
1. A  
2. A  
3. B  
4. A  
5. A  
6. D  
7. B  
8. B  
9. A  
10. A
