# First- and Second-Order Transient Analysis - Practice Questions

## Instructions
Each question has one correct option. Assume zero initial energy unless stated otherwise.

## Questions

### Q1. RC time constant [Easy]
A 10 kΩ resistor is in series with a 1 μF capacitor. The time constant is:

A. 1 ms  
B. 10 ms  
C. 100 ms  
D. 1 s

**Answer:** B  
**Explanation:** `τ = RC = 10,000×1×10⁻⁶ = 0.01 s = 10 ms`.

### Q2. RC charging at one time constant [Easy]
A 5 V RC circuit has reached `t=τ` from a zero initial voltage. The capacitor voltage is approximately:

A. 1.58 V  
B. 3.16 V  
C. 3.68 V  
D. 5.00 V

**Answer:** C  
**Explanation:** `v_C(τ)=V_f(1−e⁻¹)=5×0.632=3.16 V`. This is the 63.2% point.

### Q3. RL time constant [Easy]
A 0.1 H inductor is connected to a 20 Ω resistor. Its time constant is:

A. 2 ms  
B. 5 ms  
C. 20 ms  
D. 200 ms

**Answer:** B  
**Explanation:** `τ=L/R=0.1/20=0.005 s=5 ms`.

### Q4. Damping ratio [Medium]
A second-order characteristic polynomial is `s²+12s+64`. Its damping ratio and damping type are:

A. `ζ=0.75`, underdamped  
B. `ζ=1.50`, underdamped  
C. `ζ=0.75`, overdamped  
D. `ζ=8.00`, undamped

**Answer:** A  
**Explanation:** Comparing with `s²+2ζω₀s+ω₀²`, `ω₀=8` and `2ζω₀=12`, so `ζ=12/16=0.75<1`.

### Q5. Overdamped roots [Medium]
The characteristic equation is `s²+7s+12=0`. Its roots are:

A. `−1, −4`  
B. `1, 4`  
C. `−3±j√3`  
D. `−10, +3`

**Answer:** A  
**Explanation:** `s²+7s+12=(s+3)(s+4)`, giving `s=−3` and `s=−4`.

### Q6. Critically damped response [Medium]
A system has repeated poles at `s=−10`. Its characteristic polynomial is:

A. `(s−10)²`  
B. `(s+10)²`  
C. `s(s+10)`  
D. `s²−20s+100`

**Answer:** B  
**Explanation:** Repeated stable poles at `−10` give `(s+10)²=s²+20s+100`; this is critically damped.

### Q7. Initial-value theorem [Medium]
For `X(s)=s/(s+4)`, find `x(0⁺)` using the initial-value theorem.

A. 0  
B. 0.25  
C. 1  
D. Undefined

**Answer:** C  
**Explanation:** `x(0⁺)=lim(s→∞)[sX(s)]=lim[s²/(s+4)]=1`.

### Q8. First-order homogeneous response [Easy]
A state variable has `x(t)=5e⁻²⁰ᵗ u(t)`. Find `x(0⁺)`.

A. 0  
B. 5  
C. 20  
D. 100

**Answer:** B  
**Explanation:** At zero time, `u(0⁺)=1`, so `x(0⁺)=5e⁰=5`.

### Q9. Initial RL slope [Medium]
A 10 V source is applied to an unenergized 0.2 H inductor. What is the initial current slope `di/dt(0⁺)`?

A. 0 A/s  
B. 20 A/s  
C. 50 A/s  
D. 200 A/s

**Answer:** C  
**Explanation:** `v=L di/dt`; therefore `di/dt(0⁺)=V/L=10/0.2=50 A/s`.

### Q10. Capacitor voltage continuity [Easy]
A finite voltage cannot be applied instantaneously across an ideal capacitor without an impulse current. For ordinary finite excitation:

A. `v_C` may jump arbitrarily  
B. `i_C` must be constant  
C. `v_C(0⁺)=v_C(0⁻)`  
D. `v_C(0⁺)=0` always

**Answer:** C  
**Explanation:** Since `i_C=C dv_C/dt`, a finite current cannot change the capacitor voltage instantaneously.

## Answer Key
1. B  
2. C  
3. B  
4. A  
5. A  
6. B  
7. C  
8. B  
9. C  
10. C
