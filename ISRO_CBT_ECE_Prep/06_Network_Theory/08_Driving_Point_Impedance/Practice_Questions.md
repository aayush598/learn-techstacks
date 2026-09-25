# Driving-Point Impedance - Practice Questions

## Instructions
Each question has one correct option. Passive RLC driving-point functions must satisfy the positive-real property.

## Questions

### Q1. Driving-point impedance definition [Easy]
The driving-point impedance at a port is:

A. `I(s)/V(s)`  
B. `V(s)/I(s)`  
C. `Z(s)=R+sL` always  
D. `Y(s)/V(s)`

**Answer:** B  
**Explanation:** By definition, `Z(s)=V(s)/I(s)` at the single-port terminals.

### Q2. Passive-network property [Easy]
For a passive RLC one-port, the real part of its impedance on the right-half-plane frequency axis satisfies:

A. `Re{Z(jω)}<0`  
B. `Re{Z(jω)}≥0`  
C. `Re{Z(jω)}=1`  
D. `Re{Z(jω)}<1`

**Answer:** B  
**Explanation:** A passive driving-point impedance is a positive-real function, so it cannot supply real power and has nonnegative real part where defined.

### Q3. Coefficient property [Easy]
A positive-real rational impedance must have:

A. Complex coefficients only  
B. Real coefficients  
C. Only odd powers of `s`  
D. A zero constant term

**Answer:** B  
**Explanation:** Physical R, L, and C elements produce a real rational function with real coefficients.

### Q4. Pole restriction [Medium]
Which pole location is impossible for a passive RLC driving-point impedance?

A. `−2` on the negative real axis  
B. `−1+j2` in the left half-plane  
C. `+1` in the right half-plane  
D. A simple pole at `j5`

**Answer:** C  
**Explanation:** A positive-real function cannot have a right-half-plane pole.

### Q5. Zero location [Medium]
Which statement about zeros of a passive driving-point impedance is correct?

A. Every zero must lie in the left half-plane  
B. Every zero must lie on the imaginary axis  
C. A right-half-plane zero is allowed  
D. Zeros are unrestricted, including repeated nonconjugate imaginary poles

**Answer:** C  
**Explanation:** Positive-real functions have no right-half-plane poles, but their zeros may lie in the right half-plane.

### Q6. Degree restriction [Medium]
A passive RLC driving-point impedance `Z=N(s)/D(s)` after cancellation normally satisfies:

A. `deg(N)−deg(D)>1`  
B. `deg(N)−deg(D)≤1`  
C. `deg(N)=deg(D)+2` only  
D. `deg(D)=0` always

**Answer:** B  
**Explanation:** A rational positive-real function is proper and, after common factors are removed, normally has numerator degree no greater than denominator degree.

### Q7. Series RLC impedance [Easy]
A series `R`, `L`, and `C` one-port has:

A. `Z(s)=1/(R+sL+sC)`  
B. `Z(s)=R+sL+1/(sC)`  
C. `Z(s)=R/(s²LC)`  
D. `Z(s)=1/(1/R+sL+1/C)`

**Answer:** B  
**Explanation:** Series element impedances add directly.

### Q8. Practical parallel resonance [Medium]
For a practical parallel RLC with `R`, `L`, and `C` in parallel, the impedance at resonance is:

A. 0 Ω  
B. R  
C. `1/(RC)`  
D. Infinite because the parallel branch is lossless

**Answer:** B  
**Explanation:** The L and C susceptances cancel at resonance; the finite parallel resistance remains.

### Q9. Foster and Cauer synthesis [Medium]
Foster and Cauer are primarily:

A. Fourier-transform methods  
B. Driving-point impedance realization methods  
C. Transient integration methods  
D. Noise analysis methods

**Answer:** B  
**Explanation:** Foster and Cauer forms provide canonical LC or RLC ladder realizations of a specified driving-point impedance.

### Q10. Network-synthesis sequence [Medium]
Before realizing a rational function as a passive RLC network, the standard first test is:

A. Compute its Fourier transform  
B. Check the positive-real property  
C. Convert it to polar form  
D. Assume a Cauer realization exists

**Answer:** B  
**Explanation:** Positive-real behavior is a necessary condition for passive realization; decomposition and ladder construction follow after the test.

## Answer Key
1. B  
2. B  
3. B  
4. C  
5. C  
6. B  
7. B  
8. B  
9. B  
10. B
