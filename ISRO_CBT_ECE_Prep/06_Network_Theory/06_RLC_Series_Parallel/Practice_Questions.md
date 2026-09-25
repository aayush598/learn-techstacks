# Series and Parallel RLC Circuits - Practice Questions

## Instructions
Each question has one correct option. For parallel RLC, assume the practical circuit containing ideal `R`, `L`, and `C` in parallel.

## Questions

### Q1. Series resonant frequency [Easy]
A series RLC circuit has `L=100 mH` and `C=1 μF`. Its resonant frequency is approximately:

A. 50.3 Hz  
B. 159 Hz  
C. 503 Hz  
D. 1,590 Hz

**Answer:** C  
**Explanation:** `f₀=1/(2π√LC)=1/(2π√(0.1×1 μF))≈503 Hz`.

### Q2. Impedance at series resonance [Easy]
At series resonance, the net reactance is zero. The input impedance is:

A. Zero for every R  
B. Equal to R  
C. Equal to `X_L`  
D. Infinite

**Answer:** B  
**Explanation:** `Z(jω₀)=R+j(ω₀L−1/(ω₀C))=R`.

### Q3. Series quality factor [Easy]
For a series RLC circuit, the quality factor is:

A. `Q=R/(ω₀L)`  
B. `Q=ω₀L/R`  
C. `Q=ω₀RC`  
D. `Q=R√(L/C)`

**Answer:** B  
**Explanation:** `Q=ω₀L/R=1/(ω₀CR)` for a series circuit.

### Q4. Numerical Q and bandwidth [Medium]
A series RLC has `L=100 mH`, `C=25 μF`, and `R=10 Ω`. Find `Q` and the half-power bandwidth.

A. `Q=1.00`, `BW=101 Hz`  
B. `Q=6.32`, `BW=15.9 Hz`  
C. `Q=6.32`, `BW=63.2 Hz`  
D. `Q=10.0`, `BW=10.1 Hz`

**Answer:** B  
**Explanation:** `ω₀≈632.5 rad/s`, so `Q=ω₀L/R≈6.32`; `f₀≈100.7 Hz` and `BW=f₀/Q≈15.9 Hz`.

### Q5. Practical parallel resonance [Easy]
At resonance of a practical parallel RLC with `R`, `L`, and `C` in parallel, the input impedance is:

A. Zero  
B. Equal to R  
C. Equal to `ω₀L`  
D. Infinite

**Answer:** B  
**Explanation:** The susceptances of the ideal L and C cancel, leaving only the parallel resistance `R`.

### Q6. Half-power frequencies [Medium]
The exact series-resonant half-power frequencies are `f₁` and `f₂`. Which relation is valid?

A. `f₀=(f₁+f₂)/2` always  
B. `f₁f₂=f₀²`  
C. `f₂−f₁=Qf₀`  
D. `f₁f₂=1`

**Answer:** B  
**Explanation:** For a series RLC, `f₀²=f₁f₂`; bandwidth is `f₂−f₁=f₀/Q`.

### Q7. Voltage magnification [Medium]
A series RLC at resonance is supplied by 1 V RMS. If `Q=10`, the capacitor voltage magnitude is approximately:

A. 0.1 V  
B. 1 V  
C. 10 V  
D. 100 V

**Answer:** C  
**Explanation:** At resonance, reactive voltage is `Q` times the applied voltage: `V_C=QV=10 V`.

### Q8. Band-edge phase [Medium]
At the exact lower and upper half-power frequencies of a series RLC circuit, the impedance phase magnitudes are approximately:

A. 0° at both  
B. 45° at both  
C. 90° and 0°  
D. ±90°

**Answer:** B  
**Explanation:** `|X_L−X_C|=R` at each band edge, so `|∠Z|=tan⁻¹(1)=45°`; the lower edge is capacitive and the upper edge inductive.

### Q9. Series damping ratio [Medium]
For a series RLC circuit, the damping ratio is:

A. `ζ=(R/2)√(C/L)`  
B. `ζ=(2R)√(L/C)`  
C. `ζ=R√(LC)`  
D. `ζ=1/(2R)√(L/C)`

**Answer:** A  
**Explanation:** `ζ=α/ω₀`, with `α=R/(2L)` and `ω₀=1/√LC`; therefore `ζ=(R/2)√(C/L)`.

### Q10. Overdamped poles [Medium]
A natural response has `α=6 s⁻¹` and `ω₀=3 s⁻¹`. Its pole locations are:

A. `−6±j3`  
B. `−3±j√27`  
C. `−3, −9`  
D. `−6, 0`

**Answer:** C  
**Explanation:** `s=−α±√(α²−ω₀²)=−6±√27=−3,−9`; the response is overdamped.

## Answer Key
1. C  
2. B  
3. B  
4. B  
5. B  
6. B  
7. C  
8. B  
9. A  
10. C
