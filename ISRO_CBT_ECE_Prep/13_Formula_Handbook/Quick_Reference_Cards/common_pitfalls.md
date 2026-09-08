# Quick Reference Card - ISRO Common Pitfalls

## Traps That ISRO Sets

---

## Analog Circuits Pitfalls
1. **Forgetting virtual ground requires negative feedback**
   - If positive feedback: V+ != V- (comparator, not amp)

2. **Using wrong gain formula**
   - Inverting: Av = -Rf/R1 (NOT 1+Rf/R1)
   - Non-inverting: Av = 1+Rf/R1 (NOT -Rf/R1)

3. **Class B efficiency confusion**
   - pi/4 = 78.5% (NOT pi/2)
   - Class A = 25% (resistive), 50% (transformer)

4. **Oscillator gain requirement**
   - Wien bridge: gain >= 3 (NOT 2)
   - RC phase shift: gain >= 29 (NOT 3)

## Digital Circuits Pitfalls
5. **K-map Gray code ordering**
   - MUST be: 00,01,11,10
   - NEVER: 00,01,10,11

6. **Signal vs Variable in VHDL**
   - Signal: delayed assignment (after delta)
   - Variable: immediate assignment

7. **Blocking vs Non-blocking**
   - Sequential logic: always @(posedge clk) with <=
   - Combinational: always @(*) with =

8. **ADC resolution**
   - Resolution = Vref/2^n (NOT Vref/n)

## EM/Microwaves Pitfalls
9. **Waveguide phase/group velocity**
   - vp > c (NOT < c)
   - vg < c (NOT > c)
   - vp*vg = c^2

10. **Smith chart movement**
    - Toward generator: clockwise (NOT counter-clockwise)

11. **Quarter-wave transformer**
    - Zin = Z0^2/ZL (NOT Z0*ZL)

## Communication Pitfalls
12. **AM power formula**
    - Ptotal = Pc(1+mu^2/2) (NOT Pc(1+mu^2))

13. **PCM SQNR**
    - 6.02n + 1.76 dB (NOT 6n or 6.02n + 2)

14. **Nyquist rate**
    - fs >= 2*fmax (NOT fs >= fmax)

15. **Noise figure cascading**
    - F = F1+(F2-1)/G1 (NOT F1+F2)

## Control Systems Pitfalls
16. **Phase margin sign**
    - PM = 180 + angle(G) at gain crossover
    - Positive PM = stable

17. **Bode plot initial slope**
    - -20 dB/dec = pole at origin (NOT zero)

18. **State-space dimension**
    - n states = n first-order differential equations
    - NOT n = order of transfer function denominator always

## Network Theory Pitfalls
19. **Capacitor initial condition**
    - Vc(0+) = Vc(0-) (voltage continuity)
    - NOT current continuity for capacitor

20. **Inductor initial condition**
    - iL(0+) = iL(0-) (current continuity)
    - NOT voltage continuity for inductor

## General Exam Pitfalls
21. **Reading "NOT" and "EXCEPT"**
    - Double-check every question for these words

22. **Units mismatch**
    - Always write units in intermediate calculations

23. **dB conversion**
    - Power: 10*log10(P1/P2)
    - Voltage: 20*log10(V1/V2)

24. **Negative sign in feedback**
    - Negative feedback: A*beta positive
    - Positive feedback: A*beta negative (if A is negative)
