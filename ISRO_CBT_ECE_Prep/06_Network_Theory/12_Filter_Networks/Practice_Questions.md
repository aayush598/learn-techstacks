# Filter Networks - Practice Questions

## Instructions
Each question has one correct option. Magnitudes and powers are referenced to the filter input.

## Questions

### Q1. First-order RC cutoff [Easy]
An RC low-pass filter uses `R=1 kΩ` and `C=50 nF`. Its cutoff frequency is:

A. 1.59 kHz  
B. 3.18 kHz  
C. 6.36 kHz  
D. 10.0 kHz

**Answer:** B  
**Explanation:** `f_c=1/(2πRC)=1/(2π×1000×50 nF)≈3.18 kHz`.

### Q2. Magnitude at cutoff [Easy]
At the cutoff frequency of a first-order filter, the output magnitude is:

A. 1.00 times the input  
B. 0.707 times the input  
C. 0.500 times the input  
D. Zero

**Answer:** B  
**Explanation:** `|H|=1/√2=0.707`, corresponding to −3 dB and half power.

### Q3. First-order roll-off [Easy]
A first-order low-pass filter has an asymptotic slope of:

A. +20 dB/decade  
B. −20 dB/decade  
C. −40 dB/decade  
D. −6 dB/decade

**Answer:** B  
**Explanation:** Each first-order pole contributes approximately −20 dB per decade above cutoff.

### Q4. Order from roll-off [Easy]
A −60 dB/decade low-pass asymptote corresponds to order:

A. 1  
B. 2  
C. 3  
D. 6

**Answer:** C  
**Explanation:** The asymptotic roll-off is `−20n dB/decade`; for `n=3`, it is −60 dB/decade.

### Q5. Butterworth at cutoff [Medium]
A Butterworth low-pass filter has `|H(jω_c)|²`:

A. 1  
B. 1/2  
C. 1/4  
D. Depends on the order only

**Answer:** B  
**Explanation:** Every Butterworth filter satisfies `|H(ω_c)|²=1/(1+1)=1/2`, independent of order.

### Q6. Chebyshev ripple factor [Medium]
A Type-I Chebyshev filter has passband ripple `R=1 dB`. Its ripple factor is:

A. `ε=0.101`  
B. `ε=0.259`  
C. `ε=0.509`  
D. `ε=1.000`

**Answer:** C  
**Explanation:** `ε=√(10^(1/10)−1)=√(1.2589−1)=0.5089`.

### Q7. Passive-filter gain [Easy]
A passive RLC filter can provide voltage gain greater than one in its passband:

A. Yes, because resonance always amplifies  
B. No, a passive network can only attenuate overall  
C. Yes, if the input impedance is low  
D. Only when loaded by a negative resistance

**Answer:** B  
**Explanation:** A passive lossless filter can redistribute voltage, but its loaded transfer magnitude cannot exceed one without active gain or reflection-power considerations.

### Q8. Resonant-filter Q [Medium]
A series filter has `L=100 mH`, `C=1 μF`, and `R=10 Ω`. Its resonant quality factor is approximately:

A. 1.01  
B. 3.16  
C. 10.0  
D. 50.3

**Answer:** D  
**Explanation:** `ω₀≈5033 rad/s`; `Q=ω₀L/R≈503.3/10=50.3`.

### Q9. Bandwidth from Q [Medium]
For the filter in Q8, `f₀≈503.3 Hz` and `Q≈50.33`. Its half-power bandwidth is approximately:

A. 5.00 Hz  
B. 10.0 Hz  
C. 50.3 Hz  
D. 503 Hz

**Answer:** B  
**Explanation:** `BW=f₀/Q=503.3/50.33=10 Hz`.

### Q10. Sallen-Key cutoff [Medium]
A unity-gain Sallen-Key low-pass has equal resistors of 10 kΩ and equal capacitors of 1 nF. Its cutoff is approximately:

A. 1.59 kHz  
B. 15.9 kHz  
C. 25.1 kHz  
D. 159 kHz

**Answer:** B  
**Explanation:** For the balanced unity-gain case, `f_c=1/(2πRC)=1/(2π×10,000×1 nF)=15.9 kHz`.

## Answer Key
1. B  
2. B  
3. B  
4. C  
5. B  
6. C  
7. B  
8. D  
9. B  
10. B
