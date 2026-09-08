# System Modeling - Practice Questions

## Section A: Conceptual Questions

**Q1.** What is the transfer function of a system defined as?
**A1.** The ratio of the Laplace transform of the output to the Laplace transform of the input, with all initial conditions assumed zero.

**Q2.** Under what condition is the final value theorem valid?
**A2.** It is valid only when all poles of s·F(s) lie in the left half of the s-plane (stable system), i.e., the final value exists and is finite.

**Q3.** State the condition for a system to be 'proper'.
**A3.** A system is proper if the degree of the numerator polynomial is less than or equal to the degree of the denominator polynomial (m ≤ n).

**Q4.** What does the order of a system represent?
**A4.** The order equals the highest power of s in the denominator polynomial of the transfer function (or characteristic equation), and equals the number of state variables.

## Section B: Laplace Transform Problems

**Q5.** Find L{e^{-3t}·sin(2t)}.
**A5.** Using frequency shift: L{sin(2t)} = 2/(s²+4), so L{e^{-3t}·sin(2t)} = 2/((s+3)²+4) = 2/(s²+6s+13).

**Q6.** Find the inverse Laplace transform of F(s) = 1/(s(s+2)).
**A6.** Partial fractions: 1/(s(s+2)) = (1/2)/s - (1/2)/(s+2). Inverse: f(t) = (1/2) - (1/2)e^{-2t} = (1/2)(1-e^{-2t})·u(t).

**Q7.** Find the final value of a system with Y(s) = 5/(s(s²+s+2)).
**A7.** y(∞) = lim(s→0) s·Y(s) = lim(s→0) 5/(s²+s+2) = 5/2 = 2.5.

**Q8.** If L{f(t)} = F(s), find L{∫₀ᵗ f(τ)dτ}.
**A8.** L{∫₀ᵗ f(τ)dτ} = F(s)/s (integration property).

## Section C: Transfer Function Derivation

**Q9.** For a series RLC circuit with R=2Ω, L=1H, C=0.5F (output across capacitor), find G(s) = Vc(s)/V(s).
**A9.** G(s) = (1/LC)/(s² + (R/L)s + 1/LC) = (1/0.5)/(s² + 2s + 2) = 2/(s²+2s+2).

**Q10.** A mechanical system has m=2kg, b=4 N·s/m, k=6 N/m. Find G(s) = X(s)/F(s).
**A10.** G(s) = 1/(ms²+bs+k) = 1/(2s²+4s+6).

**Q11.** Find the transfer function of G(s) = Vout/Vin for a simple low-pass RC filter (R=1kΩ, C=1µF).
**A11.** G(s) = (1/Cs)/(R + 1/Cs) = 1/(RCs + 1) = 1/(0.001s + 1).

**Q12.** Find the transfer function of an op-amp integrator.
**A12.** Vout/Vin = -Zf/Zin = -(1/Cs)/R = -1/(RCs).

## Section D: Block Diagram Algebra

**Q13.** Two blocks in series: G₁(s) = 1/(s+1), G₂(s) = 2/s. Find total transfer function.
**A13.** G_total = G₁·G₂ = 2/(s(s+1)).

**Q14.** Unity feedback system with open-loop G(s) = 10/(s+5). Find closed-loop transfer function.
**A14.** T(s) = G/(1+G) = [10/(s+5)]/[1+10/(s+5)] = 10/(s+15).

**Q15.** Non-unity feedback: G(s) = 4/s, H(s) = 2. Find closed-loop transfer function.
**A15.** T(s) = G/(1+GH) = [4/s]/[1+(4/s)(2)] = 4/(s+8).

**Q16.** System with G(s) = 5/(s(s+2)) in feedback with H(s) = 1. Find closed-loop and the characteristic equation.
**A16.** T(s) = 5/(s(s+2)+5) = 5/(s²+2s+5). Characteristic equation: s²+2s+5 = 0.

## Section E: State-Space Modeling

**Q17.** Given G(s) = (s+3)/(s²+4s+7), find the controllable canonical state-space form.
**A17.** a₀=7, a₁=4; b₀=3, b₁=1, b₂=0.
A = [[0,1],[-7,-4]], B = [[0],[1]], C = [3,1], D = 0.

**Q18.** How many state variables are needed for a third-order system?
**A18.** Three state variables (order = number of state variables).

**Q19.** Given the state-space, how is the transfer function obtained?
**A19.** G(s) = C(sI - A)⁻¹B + D.

**Q20.** Write the state and output equations for a system described by ẋ = Ax + Bu, y = Cx + Du.
**A20.** State equation: ẋ = Ax + Bu (vector differential equation). Output equation: y = Cx + Du (algebraic equation).

## Section F: ISRO-Style Problems

**Q21.** A spring-mass-damper has mass 1 kg, damping 2 N·s/m, spring constant 1 N/m. Determine damping ratio and natural frequency.
**A21.** ω_n = √(k/m) = √1 = 1 rad/s. ζ = b/(2√(km)) = 2/(2·1) = 1 (critically damped).

**Q22.** For the transfer function G(s) = 3/(s²+2s+4), identify the system type based on the denominator form.
**A22.** It is a second-order system (denominator is quadratic). Natural frequency ω_n = √4 = 2, damping ratio ζ = 2/(2·√4) = 0.5.

**Q23.** A unity feedback system has open-loop transfer function G(s) = K/(s(s+4)). Write the closed-loop transfer function and characteristic equation.
**A23.** T(s) = K/(s²+4s+K). Characteristic equation: s²+4s+K = 0.

**Q24.** Find the DC gain of G(s) = 10(s+2)/((s+5)(s+10)).
**A24.** DC gain = G(0) = 10(2)/(5·10) = 20/50 = 0.4.

**Q25.** For a system with G(s) = 1/(s+1), if the input is a unit step, find the output y(t).
**A25.** Y(s) = G(s)·(1/s) = 1/(s(s+1)) = 1/s - 1/(s+1). y(t) = (1 - e^{-t})·u(t).

## Section G: Match the Following

**Q26.** Match the analogy:
(a) Inductance L ↔ (i) Damping b
(b) Resistance R ↔ (ii) Compliance 1/k
(c) Capacitance C ↔ (iii) Mass m
**A26.** (a)-iii, (b)-i, (c)-ii.

## Summary of Common Mistakes
1. Forgetting zero initial conditions in transfer function definition.
2. Applying final value theorem to unstable systems.
3. Sign errors in feedback loop formulas (negative vs positive feedback).
4. Confusing open-loop transfer function (GH) with closed-loop (G/(1+GH)).
5. Incorrect partial fraction decomposition for repeated roots.
